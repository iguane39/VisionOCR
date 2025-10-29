# modules/utils.py
"""
Fonctions utilitaires pour l'application OCR
"""

from pathlib import Path
from typing import Optional
from loguru import logger


def validate_pdf_path(pdf_path: str) -> bool:
    """
    Valide qu'un chemin pointe vers un fichier PDF existant

    Args:
        pdf_path: Chemin vers le fichier PDF

    Returns:
        True si valide, False sinon
    """
    path = Path(pdf_path)

    if not path.exists():
        logger.error(f"Le fichier n'existe pas: {pdf_path}")
        return False

    if not path.is_file():
        logger.error(f"Le chemin ne pointe pas vers un fichier: {pdf_path}")
        return False

    if path.suffix.lower() != '.pdf':
        logger.error(f"Le fichier n'est pas un PDF: {pdf_path}")
        return False

    return True


def ensure_directory_exists(directory: str):
    """
    Crée un répertoire s'il n'existe pas

    Args:
        directory: Chemin du répertoire
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)


def get_output_path(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Détermine le chemin de sortie pour le fichier DOCX

    Args:
        input_path: Chemin du PDF d'entrée
        output_path: Chemin de sortie souhaité (optionnel)

    Returns:
        Chemin de sortie pour le DOCX
    """
    if output_path:
        return output_path

    # Générer un nom de sortie basé sur l'entrée
    input_path_obj = Path(input_path)
    return str(input_path_obj.parent / f"{input_path_obj.stem}_ocr.docx")


def format_file_size(size_bytes: int) -> str:
    """
    Formate une taille de fichier en octets vers une chaîne lisible

    Args:
        size_bytes: Taille en octets

    Returns:
        Chaîne formatée (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def estimate_processing_time(num_pages: int, dpi: int = 300) -> str:
    """
    Estime le temps de traitement

    Args:
        num_pages: Nombre de pages
        dpi: Résolution DPI

    Returns:
        Estimation du temps (ex: "~5 minutes")
    """
    # Estimation approximative: 2-3 secondes par page à 300 DPI
    seconds_per_page = 2.5
    if dpi > 300:
        seconds_per_page *= (dpi / 300)

    total_seconds = num_pages * seconds_per_page

    if total_seconds < 60:
        return f"~{int(total_seconds)} secondes"
    elif total_seconds < 3600:
        minutes = int(total_seconds / 60)
        return f"~{minutes} minutes"
    else:
        hours = int(total_seconds / 3600)
        return f"~{hours} heures"
