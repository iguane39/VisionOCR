# modules/vision_api_client.py
"""
Client pour Google Cloud Vision API avec gestion du cache
"""

from google.cloud import vision
from google.oauth2 import service_account
from typing import List, Dict, Any
from loguru import logger
from diskcache import Cache
import hashlib
from pathlib import Path


class VisionAPIClient:
    """
    Client pour Google Cloud Vision API avec gestion du cache
    """

    def __init__(self, credentials_path: str, cache_enabled: bool = True):
        """
        Initialise le client Vision API

        Args:
            credentials_path: Chemin vers le fichier JSON de credentials
            cache_enabled: Active le cache pour économiser les appels API
        """
        # Vérifier que le fichier de credentials existe
        if not Path(credentials_path).exists():
            raise FileNotFoundError(
                f"Fichier de credentials non trouvé: {credentials_path}\n"
                f"Veuillez télécharger votre fichier credentials.json depuis Google Cloud Console"
            )

        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)
        self.cache_enabled = cache_enabled

        if cache_enabled:
            self.cache = Cache('.cache/vision_api')
            logger.info("Cache activé pour Vision API")

    def _get_cache_key(self, image_content: bytes) -> str:
        """Génère une clé de cache basée sur le contenu de l'image"""
        return hashlib.sha256(image_content).hexdigest()

    def detect_document_text(self, image_path: str) -> vision.AnnotateImageResponse:
        """
        Détecte le texte dans une image avec DOCUMENT_TEXT_DETECTION

        Args:
            image_path: Chemin vers l'image

        Returns:
            Réponse complète de Vision API avec annotations
        """
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Vérifier le cache
        if self.cache_enabled:
            cache_key = self._get_cache_key(content)
            cached_response = self.cache.get(cache_key)
            if cached_response:
                logger.debug(f"Résultat trouvé dans le cache pour {image_path}")
                return cached_response

        # Appel API
        image = vision.Image(content=content)

        response = self.client.document_text_detection(
            image=image,
            image_context={"language_hints": ["fr", "en"]}
        )

        if response.error.message:
            raise Exception(f"Vision API Error: {response.error.message}")

        # Mettre en cache
        if self.cache_enabled:
            self.cache.set(cache_key, response, expire=86400 * 30)
            logger.debug(f"Réponse mise en cache pour {image_path}")

        logger.success(f"OCR complété pour {image_path}")
        return response

    def batch_detect_document_text(
        self, image_paths: List[str]
    ) -> List[vision.AnnotateImageResponse]:
        """
        Traitement par lot de plusieurs images (plus efficace)

        Args:
            image_paths: Liste de chemins d'images

        Returns:
            Liste de réponses Vision API
        """
        requests = []

        for image_path in image_paths:
            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            requests.append({
                'image': image,
                'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
                'image_context': {'language_hints': ['fr', 'en']}
            })

        # Batch request
        response = self.client.batch_annotate_images(requests=requests)

        logger.success(f"Batch OCR complété pour {len(image_paths)} images")
        return response.responses

    def extract_text_annotations(
        self, response: vision.AnnotateImageResponse
    ) -> Dict[str, Any]:
        """
        Extrait et structure les informations du texte détecté

        Returns:
            {
                'full_text': str,
                'pages': [
                    {
                        'blocks': [
                            {
                                'type': 'TEXT',
                                'text': str,
                                'confidence': float,
                                'bounding_box': [(x, y), ...],
                                'paragraphs': [...]
                            }
                        ]
                    }
                ]
            }
        """
        if not response.full_text_annotation:
            return {'full_text': '', 'pages': []}

        result = {
            'full_text': response.full_text_annotation.text,
            'pages': []
        }

        for page in response.full_text_annotation.pages:
            page_data = {
                'width': page.width,
                'height': page.height,
                'confidence': page.confidence,
                'blocks': []
            }

            for block in page.blocks:
                block_data = {
                    'type': self._get_block_type(block.block_type),
                    'confidence': block.confidence,
                    'bounding_box': self._extract_bounding_box(block.bounding_box),
                    'paragraphs': []
                }

                for paragraph in block.paragraphs:
                    para_data = {
                        'confidence': paragraph.confidence,
                        'bounding_box': self._extract_bounding_box(
                            paragraph.bounding_box
                        ),
                        'words': []
                    }

                    for word in paragraph.words:
                        word_data = {
                            'text': ''.join([symbol.text for symbol in word.symbols]),
                            'confidence': word.confidence,
                            'bounding_box': self._extract_bounding_box(
                                word.bounding_box
                            ),
                            'symbols': []
                        }

                        for symbol in word.symbols:
                            symbol_data = {
                                'text': symbol.text,
                                'confidence': symbol.confidence,
                                'bounding_box': self._extract_bounding_box(
                                    symbol.bounding_box
                                ),
                                'property': self._extract_text_property(
                                    symbol.property
                                )
                            }
                            word_data['symbols'].append(symbol_data)

                        para_data['words'].append(word_data)

                    # Reconstituer le texte du paragraphe
                    para_data['text'] = ' '.join([w['text'] for w in para_data['words']])
                    block_data['paragraphs'].append(para_data)

                # Reconstituer le texte du bloc
                block_data['text'] = ' '.join([p['text'] for p in block_data['paragraphs']])
                page_data['blocks'].append(block_data)

            result['pages'].append(page_data)

        return result

    def _get_block_type(self, block_type) -> str:
        """Convertit le type de bloc Vision API en chaîne"""
        types = {
            0: 'UNKNOWN',
            1: 'TEXT',
            2: 'TABLE',
            3: 'PICTURE',
            4: 'RULER',
            5: 'BARCODE'
        }
        return types.get(block_type, 'UNKNOWN')

    def _extract_bounding_box(self, bounding_box) -> List[tuple]:
        """Extrait les coordonnées du bounding box"""
        return [(vertex.x, vertex.y) for vertex in bounding_box.vertices]

    def _extract_text_property(self, property) -> Dict[str, Any]:
        """
        Extrait les propriétés de formatage du texte

        Vision API fournit :
        - detected_break : type de rupture (espace, nouvelle ligne, etc.)
        - detected_languages : langues détectées
        """
        if not property:
            return {}

        result = {}

        # Type de rupture (important pour détecter les paragraphes)
        if property.detected_break:
            result['break_type'] = self._get_break_type(property.detected_break.type_)
            result['is_prefix'] = property.detected_break.is_prefix

        # Langues détectées
        if property.detected_languages:
            result['languages'] = [
                {
                    'language_code': lang.language_code,
                    'confidence': lang.confidence
                }
                for lang in property.detected_languages
            ]

        return result

    def _get_break_type(self, break_type) -> str:
        """Convertit le type de rupture Vision API"""
        types = {
            0: 'UNKNOWN',
            1: 'SPACE',
            2: 'SURE_SPACE',
            3: 'EOL_SURE_SPACE',  # Fin de ligne avec espace
            4: 'HYPHEN',
            5: 'LINE_BREAK'
        }
        return types.get(break_type, 'UNKNOWN')

    def get_api_usage_stats(self) -> Dict[str, int]:
        """Retourne les statistiques d'utilisation de l'API"""
        if not self.cache_enabled:
            return {'cache_hits': 0, 'cache_misses': 0}

        stats = {}
        try:
            cache_stats = self.cache.stats(enable=True)
            stats = {
                'cache_size': len(self.cache),
                'cache_hits': cache_stats.get('hits', 0),
                'cache_misses': cache_stats.get('misses', 0)
            }
        except Exception:
            stats = {'cache_size': len(self.cache), 'cache_hits': 0, 'cache_misses': 0}

        return stats
