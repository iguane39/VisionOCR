# modules/docx_builder.py
"""
Construit un document Word à partir des données Vision API
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from typing import Dict, List, Any
from loguru import logger


class DocxBuilder:
    """
    Construit un document Word à partir des données Vision API
    """

    def __init__(self, create_styles: bool = True):
        self.document = Document()
        self.create_styles = create_styles
        self.style_counter = 0

        # Configuration des marges
        sections = self.document.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

    def create_document_from_vision_data(self, pages_data: List[Dict]) -> Document:
        """
        Crée le document Word complet à partir des données Vision API

        Args:
            pages_data: Liste de pages avec leurs blocs/paragraphes annotés
        """
        logger.info(f"Construction du document Word avec {len(pages_data)} pages")

        # Créer des styles réutilisables si demandé
        if self.create_styles:
            self._create_custom_styles()

        # Traiter chaque page
        for page_idx, page_data in enumerate(pages_data):
            logger.debug(f"Traitement de la page {page_idx + 1}")

            for block in page_data.get('blocks', []):
                if block['type'] != 'TEXT':
                    continue

                for paragraph_data in block.get('paragraphs', []):
                    self._add_paragraph_to_document(paragraph_data)

        logger.success("Document Word créé avec succès")
        return self.document

    def _create_custom_styles(self):
        """Crée des styles Word personnalisés"""
        styles = self.document.styles

        # Style pour les titres principaux
        if 'Title Custom' not in [s.name for s in styles]:
            try:
                title_style = styles.add_style('Title Custom', WD_STYLE_TYPE.PARAGRAPH)
                title_style.font.name = 'Times New Roman'
                title_style.font.size = Pt(18)
                title_style.font.bold = True
                title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                title_style.paragraph_format.space_before = Pt(24)
                title_style.paragraph_format.space_after = Pt(12)
            except Exception as e:
                logger.warning(f"Impossible de créer le style 'Title Custom': {e}")

        # Style pour le corps de texte
        if 'Body Text Custom' not in [s.name for s in styles]:
            try:
                body_style = styles.add_style('Body Text Custom', WD_STYLE_TYPE.PARAGRAPH)
                body_style.font.name = 'Times New Roman'
                body_style.font.size = Pt(11)
                body_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                body_style.paragraph_format.space_after = Pt(12)
                body_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                body_style.paragraph_format.line_spacing = Pt(15)  # 1.15x
            except Exception as e:
                logger.warning(f"Impossible de créer le style 'Body Text Custom': {e}")

    def _add_paragraph_to_document(self, para_data: Dict):
        """
        Ajoute un paragraphe au document avec son formatage
        """
        # Créer le paragraphe
        paragraph = self.document.add_paragraph()

        # Appliquer le style approprié
        if self.create_styles:
            try:
                if para_data.get('is_title'):
                    paragraph.style = 'Title Custom'
                else:
                    paragraph.style = 'Body Text Custom'
            except Exception as e:
                logger.warning(f"Impossible d'appliquer le style: {e}")

        # Appliquer l'alignement
        alignment_map = {
            'left': WD_ALIGN_PARAGRAPH.LEFT,
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'right': WD_ALIGN_PARAGRAPH.RIGHT,
            'justified': WD_ALIGN_PARAGRAPH.JUSTIFY
        }
        paragraph.alignment = alignment_map.get(
            para_data.get('alignment', 'left'),
            WD_ALIGN_PARAGRAPH.LEFT
        )

        # Appliquer les espacements
        if 'spacing_before' in para_data:
            paragraph.paragraph_format.space_before = Pt(para_data['spacing_before'])
        if 'spacing_after' in para_data:
            paragraph.paragraph_format.space_after = Pt(para_data['spacing_after'])

        # Ajouter le texte mot par mot avec formatage
        for word_idx, word_data in enumerate(para_data.get('words', [])):
            # Ajouter un espace entre les mots (sauf le premier)
            if word_idx > 0:
                paragraph.add_run(' ')

            # Créer le run pour le mot
            run = paragraph.add_run(word_data['text'])

            # Appliquer le formatage
            run.font.name = para_data.get('dominant_font', 'Times New Roman')

            if para_data.get('avg_font_size'):
                run.font.size = Pt(para_data['avg_font_size'])

            if para_data.get('has_bold'):
                run.bold = True

            if para_data.get('has_italic'):
                run.italic = True

            # Petites capitales
            if para_data.get('all_caps') and not para_data.get('is_title'):
                run.font.small_caps = True

    def save(self, output_path: str):
        """Sauvegarde le document"""
        self.document.save(output_path)
        logger.success(f"Document sauvegardé : {output_path}")
