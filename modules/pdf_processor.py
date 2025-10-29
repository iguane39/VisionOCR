# modules/pdf_processor.py
"""
Convertit les pages PDF en images haute résolution
"""

from pdf2image import convert_from_path
from PIL import Image
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple
from loguru import logger
from concurrent.futures import ThreadPoolExecutor


class PDFProcessor:
    """
    Convertit les pages PDF en images haute résolution
    """

    def __init__(self, dpi: int = 300, parallel: bool = True):
        self.dpi = dpi
        self.parallel = parallel
        self.temp_dir = Path(tempfile.gettempdir()) / 'ocr_vision_temp'
        self.temp_dir.mkdir(exist_ok=True)
        logger.debug(f"Répertoire temporaire : {self.temp_dir}")

    def convert_to_images(self, pdf_path: str, pages: str = 'all') -> List[str]:
        """
        Convertit les pages PDF en images PNG

        Args:
            pdf_path: Chemin vers le PDF
            pages: Pages à convertir ('all', '1-10', '5,7,9')

        Returns:
            Liste des chemins vers les images créées
        """
        logger.info(f"Conversion PDF en images (DPI: {self.dpi})")

        # Déterminer les pages à convertir
        first_page, last_page = self._parse_pages(pages)

        # Convertir avec pdf2image
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=first_page,
                last_page=last_page,
                fmt='png'
            )
        except Exception as e:
            logger.error(f"Erreur lors de la conversion PDF: {e}")
            raise

        logger.info(f"{len(images)} pages converties")

        # Sauvegarder les images
        image_paths = []
        for i, image in enumerate(images, start=first_page or 1):
            image_path = self.temp_dir / f'page_{i:04d}.png'
            image.save(image_path, 'PNG')
            image_paths.append(str(image_path))

        logger.success(f"Images sauvegardées dans {self.temp_dir}")
        return image_paths

    def _parse_pages(self, pages: str) -> Tuple[Optional[int], Optional[int]]:
        """Parse la spécification de pages"""
        if pages == 'all':
            return None, None

        if '-' in pages:
            start, end = pages.split('-')
            return int(start), int(end)

        # Pages individuelles - convertir en range
        page_nums = [int(p) for p in pages.split(',')]
        return min(page_nums), max(page_nums)

    def cleanup_temp_files(self):
        """Nettoie les fichiers temporaires"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                logger.info("Fichiers temporaires nettoyés")
        except Exception as e:
            logger.warning(f"Impossible de nettoyer les fichiers temporaires: {e}")
