# modules/format_analyzer.py
"""
Analyse et enrichit les informations de formatage de Vision API
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter
from loguru import logger


class FormatAnalyzer:
    """
    Analyse et enrichit les informations de formatage de Vision API
    """

    def __init__(self, page_width: int, page_height: int):
        self.page_width = page_width
        self.page_height = page_height
        self.font_sizes = []
        self.line_heights = []

    def analyze_paragraph_formatting(self, paragraph: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse le formatage d'un paragraphe

        Returns:
            {
                'alignment': 'left' | 'center' | 'right' | 'justified',
                'indent_first_line': float,
                'indent_left': float,
                'indent_right': float,
                'spacing_before': float,
                'spacing_after': float,
                'line_spacing': float,
                'avg_font_size': float,
                'dominant_font': str,
                'has_bold': bool,
                'has_italic': bool,
                'is_title': bool
            }
        """
        bbox = paragraph['bounding_box']
        words = paragraph['words']

        # Calculer l'alignement
        alignment = self._detect_alignment(bbox, words)

        # Analyser les polices et tailles
        font_analysis = self._analyze_fonts(words)

        # Détecter si c'est un titre
        is_title = self._is_title(paragraph, font_analysis)

        return {
            'alignment': alignment,
            'avg_font_size': font_analysis['avg_size'],
            'dominant_font': font_analysis['dominant_font'],
            'has_bold': font_analysis['has_bold'],
            'has_italic': font_analysis['has_italic'],
            'is_title': is_title,
            'all_caps': self._is_all_caps(paragraph['text']),
            'bounding_box': bbox
        }

    def _detect_alignment(self, bbox: List[Tuple], words: List[Dict]) -> str:
        """Détecte l'alignement du texte"""
        if not words:
            return 'left'

        # Position horizontale du bloc
        left = bbox[0][0]
        right = bbox[1][0]
        block_center = (left + right) / 2
        page_center = self.page_width / 2

        # Centré
        if abs(block_center - page_center) / self.page_width < 0.1:
            return 'center'

        # Analyser l'alignement des mots
        first_word_x = words[0]['bounding_box'][0][0]
        last_word_x = words[-1]['bounding_box'][1][0]

        # Justifié : première ligne proche du bord gauche, dernière proche du bord droit
        if (first_word_x < self.page_width * 0.2 and
                last_word_x > self.page_width * 0.8):
            return 'justified'

        # Droite
        if right > self.page_width * 0.8:
            return 'right'

        return 'left'

    def _analyze_fonts(self, words: List[Dict]) -> Dict[str, Any]:
        """
        Analyse les propriétés de police des mots

        Note: Vision API ne fournit pas directement les infos de police,
        nous devons les inférer des propriétés visuelles et du contexte
        """
        sizes = []
        has_bold = False
        has_italic = False

        for word in words:
            # Calculer la hauteur du mot comme proxy de la taille de police
            bbox = word['bounding_box']
            height = bbox[2][1] - bbox[0][1]
            sizes.append(height)

            # Les propriétés bold/italic ne sont pas directement disponibles
            # dans Vision API standard, on les infère du contexte

        avg_size = np.mean(sizes) if sizes else 12

        # Convertir hauteur en pixels vers points typographiques (approximation)
        # Assuming 300 DPI: 1 point = 300/72 pixels ≈ 4.17 pixels
        avg_size_points = avg_size / 4.17

        return {
            'avg_size': avg_size_points,
            'dominant_font': self._infer_font_family(avg_size_points),
            'has_bold': has_bold,
            'has_italic': has_italic
        }

    def _infer_font_family(self, font_size: float) -> str:
        """
        Infère la famille de police (serif vs sans-serif)

        Note: Vision API ne fournit pas cette info directement.
        On utilise des heuristiques basées sur le contexte du document.
        """
        # Pour un livre littéraire, on assume Times New Roman
        # Pour un document moderne, on assume Arial
        # Ceci devrait être amélioré avec analyse visuelle

        return 'Times New Roman'  # Défaut pour documents littéraires

    def _is_title(self, paragraph: Dict, font_analysis: Dict) -> bool:
        """Détermine si un paragraphe est un titre"""
        text = paragraph['text']

        # Critères pour un titre
        criteria = [
            len(text) < 100,  # Court
            text.isupper(),  # Tout en majuscules
            font_analysis['avg_size'] > 14,  # Police plus grande
        ]

        return sum(criteria) >= 2

    def _is_all_caps(self, text: str) -> bool:
        """Vérifie si le texte est tout en majuscules"""
        letters = [c for c in text if c.isalpha()]
        if not letters:
            return False
        return sum(c.isupper() for c in letters) / len(letters) > 0.8

    def calculate_spacing(
        self,
        current_para: Dict,
        previous_para: Optional[Dict] = None
    ) -> Dict[str, float]:
        """
        Calcule les espacements entre paragraphes

        Returns:
            {
                'spacing_before': float (en points),
                'spacing_after': float,
                'line_spacing': float (multiplicateur)
            }
        """
        spacing = {
            'spacing_before': 0,
            'spacing_after': 12,  # 12pt par défaut
            'line_spacing': 1.15
        }

        if previous_para:
            # Calculer l'espace vertical entre les paragraphes
            current_top = current_para['bounding_box'][0][1]
            previous_bottom = previous_para['bounding_box'][2][1]

            vertical_gap = current_top - previous_bottom

            # Convertir pixels en points (300 DPI)
            spacing['spacing_before'] = max(0, vertical_gap / 4.17)

        # Ajuster l'espacement pour les titres
        if current_para.get('is_title'):
            spacing['spacing_before'] = 24
            spacing['spacing_after'] = 18

        return spacing

    def cluster_similar_styles(
        self, paragraphs: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """
        Regroupe les paragraphes avec des styles similaires
        pour créer des styles Word réutilisables
        """
        if not paragraphs:
            return {}

        try:
            from sklearn.cluster import DBSCAN

            # Extraire les caractéristiques de style
            features = []
            for para in paragraphs:
                features.append([
                    para.get('avg_font_size', 12),
                    1 if para.get('alignment') == 'center' else 0,
                    1 if para.get('is_title') else 0,
                    1 if para.get('all_caps') else 0
                ])

            # Clustering
            features_array = np.array(features)
            clustering = DBSCAN(eps=2, min_samples=2).fit(features_array)

            # Grouper par cluster
            clusters = {}
            for idx, label in enumerate(clustering.labels_):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(paragraphs[idx])

            return clusters

        except ImportError:
            logger.warning("scikit-learn non disponible, clustering désactivé")
            return {'default': paragraphs}
