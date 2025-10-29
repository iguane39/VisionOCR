#!/usr/bin/env python3
# main.py
"""
Application CLI pour convertir des PDFs scannés en documents Word
avec Google Cloud Vision API
"""

import click
from pathlib import Path
from loguru import logger
import sys
from tqdm import tqdm

from modules.pdf_processor import PDFProcessor
from modules.vision_api_client import VisionAPIClient
from modules.format_analyzer import FormatAnalyzer
from modules.docx_builder import DocxBuilder
from modules.utils import validate_pdf_path, get_output_path
from config import Config

# Configuration du logger
logger.remove()
logger.add(sys.stderr, level="INFO", format="<level>{message}</level>")
logger.add(
    "logs/ocr_vision_{time}.log",
    rotation="10 MB",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Application OCR PDF vers Word avec Google Cloud Vision API

    Convertit des PDFs scannés en documents Word avec préservation du formatage.
    """
    pass


@cli.command()
@click.argument('input_pdf', type=click.Path(exists=True))
@click.option('--output', '-o', default=None,
              help='Chemin du fichier Word de sortie (défaut: <input>_ocr.docx)')
@click.option('--pages', '-p', default='all',
              help='Pages à traiter (ex: 1-10, 5,7,9, all)')
@click.option('--dpi', default=300, type=int,
              help='Résolution DPI pour la conversion (défaut: 300)')
@click.option('--credentials', '-c', default=None,
              help='Chemin vers le fichier credentials.json Google Cloud')
@click.option('--no-cache', is_flag=True,
              help='Désactiver le cache API (force de nouveaux appels)')
@click.option('--create-styles/--no-create-styles', default=True,
              help='Créer des styles Word réutilisables')
@click.option('--verbose', '-v', count=True,
              help='Niveau de verbosité (-v, -vv, -vvv)')
@click.option('--show-stats', is_flag=True,
              help='Afficher les statistiques d\'utilisation de l\'API')
def convert(input_pdf, output, pages, dpi, credentials,
           no_cache, create_styles, verbose, show_stats):
    """
    Convertit un PDF scanné en document Word avec Google Cloud Vision API.

    Nécessite :
    - Un compte Google Cloud avec Vision API activé
    - Un fichier credentials.json de compte de service

    Exemples:

        # Conversion basique
        python main.py convert livre.pdf

        # Conversion avec options
        python main.py convert livre.pdf -o sortie.docx --pages 1-50 --dpi 300 -vv

        # Sans cache (forcer nouvel OCR)
        python main.py convert livre.pdf --no-cache

        # Afficher les stats d'utilisation API
        python main.py convert livre.pdf --show-stats
    """
    # Configuration du niveau de log
    logger.remove()
    if verbose == 0:
        logger.add(sys.stderr, level="INFO", format="<level>{message}</level>")
    elif verbose == 1:
        logger.add(sys.stderr, level="INFO", format="<level>{level}: {message}</level>")
    elif verbose >= 2:
        logger.add(sys.stderr, level="DEBUG", format="<level>{level}: {message}</level>")

    # Valider le PDF d'entrée
    if not validate_pdf_path(input_pdf):
        sys.exit(1)

    # Déterminer le chemin de sortie
    output = get_output_path(input_pdf, output)

    # Déterminer le chemin des credentials
    creds_path = credentials or Config.GOOGLE_CREDENTIALS_PATH
    if not Path(creds_path).exists():
        logger.error(f"Fichier credentials non trouvé : {creds_path}")
        logger.info("Créez un compte de service Google Cloud et téléchargez credentials.json")
        logger.info("Pour obtenir de l'aide : python main.py setup")
        sys.exit(1)

    try:
        logger.info(f"📄 Traitement de : {input_pdf}")
        logger.info(f"📝 Sortie vers : {output}")

        # Étape 1: Conversion PDF en images
        logger.info("🔄 Étape 1/4 : Conversion PDF → Images")
        pdf_processor = PDFProcessor(dpi=dpi, parallel=True)
        image_paths = pdf_processor.convert_to_images(input_pdf, pages=pages)
        logger.success(f"✓ {len(image_paths)} images créées")

        # Étape 2: OCR avec Google Vision API
        logger.info("🔍 Étape 2/4 : OCR avec Google Vision API")
        vision_client = VisionAPIClient(
            credentials_path=creds_path,
            cache_enabled=not no_cache
        )

        pages_data = []
        with tqdm(total=len(image_paths), desc="OCR en cours", disable=verbose >= 2) as pbar:
            for img_path in image_paths:
                response = vision_client.detect_document_text(img_path)
                annotations = vision_client.extract_text_annotations(response)
                pages_data.append(annotations)
                pbar.update(1)

        logger.success(f"✓ OCR complété pour {len(pages_data)} pages")

        # Étape 3: Analyse du formatage
        logger.info("🎨 Étape 3/4 : Analyse du formatage")
        for page_data in tqdm(pages_data, desc="Analyse du formatage", disable=verbose >= 2):
            if not page_data['pages']:
                continue

            page = page_data['pages'][0]
            analyzer = FormatAnalyzer(page['width'], page['height'])

            # Analyser chaque paragraphe
            previous_para = None
            for block in page['blocks']:
                for para in block['paragraphs']:
                    formatting = analyzer.analyze_paragraph_formatting(para)
                    spacing = analyzer.calculate_spacing(formatting, previous_para)

                    # Enrichir les données du paragraphe
                    para.update(formatting)
                    para.update(spacing)

                    previous_para = formatting

        logger.success("✓ Analyse du formatage terminée")

        # Étape 4: Construction du document Word
        logger.info("📝 Étape 4/4 : Construction du document Word")
        docx_builder = DocxBuilder(create_styles=create_styles)

        # Extraire les pages pour le builder
        formatted_pages = [pd['pages'][0] if pd['pages'] else {}
                          for pd in pages_data]

        document = docx_builder.create_document_from_vision_data(formatted_pages)
        docx_builder.save(output)

        logger.success(f"✅ Document créé avec succès : {output}")

        # Afficher les statistiques
        if show_stats:
            stats = vision_client.get_api_usage_stats()
            logger.info("📊 Statistiques d'utilisation de l'API :")
            logger.info(f"   - Taille du cache : {stats.get('cache_size', 0)} entrées")
            logger.info(f"   - Cache hits : {stats.get('cache_hits', 0)}")
            logger.info(f"   - Cache misses : {stats.get('cache_misses', 0)}")

            # Estimation du coût
            api_calls = len(image_paths) - stats.get('cache_hits', 0)
            cost_per_1000 = 1.50  # Prix Google Vision API
            estimated_cost = (api_calls / 1000) * cost_per_1000
            logger.info(f"   - Appels API effectués : {api_calls}")
            logger.info(f"   - Coût estimé : ${estimated_cost:.4f} USD")

        # Nettoyer les fichiers temporaires
        pdf_processor.cleanup_temp_files()

    except Exception as e:
        logger.error(f"❌ Erreur : {e}")
        if verbose >= 2:
            logger.exception("Détails de l'erreur :")
        sys.exit(1)


@cli.command()
def setup():
    """
    Affiche les instructions pour configurer Google Cloud Vision API
    """
    print("""
╔════════════════════════════════════════════════════════════════╗
║          Configuration Google Cloud Vision API                  ║
╚════════════════════════════════════════════════════════════════╝

Étapes de configuration :

1. Créer un compte Google Cloud
   → https://console.cloud.google.com/

2. Créer un nouveau projet
   → Navigation menu → IAM & Admin → Create Project

3. Activer Cloud Vision API
   → Navigation menu → APIs & Services → Library
   → Rechercher "Cloud Vision API"
   → Cliquer sur "Enable"

4. Créer un compte de service
   → IAM & Admin → Service Accounts
   → Create Service Account
   → Nom : "ocr-pdf-service"
   → Rôle : "Cloud Vision API User"

5. Créer une clé JSON
   → Cliquer sur le compte de service créé
   → Keys → Add Key → Create New Key → JSON
   → Télécharger le fichier credentials.json

6. Configurer l'application
   → Placer credentials.json dans le dossier credentials/
   → Ou définir : export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

7. Installer les dépendances
   pip install -r requirements.txt

8. Tester l'installation
   python main.py convert --help

📊 Tarification :
   - 1000 premières pages/mois : GRATUIT
   - Pages suivantes : $1.50 / 1000 pages

💡 Conseil : Utilisez le cache pour économiser les appels API !

Pour plus d'informations :
https://cloud.google.com/vision/docs/setup
    """)


@cli.command()
def version():
    """Affiche la version de l'application"""
    print("VisionOCR v1.0.0")
    print("Application OCR PDF vers Word avec Google Cloud Vision API")


if __name__ == '__main__':
    cli()
