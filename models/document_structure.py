# models/document_structure.py
"""
Classes pour représenter la structure d'un document
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Symbol:
    """Représente un symbole (caractère) dans le texte"""
    text: str
    confidence: float
    bounding_box: List[tuple]
    property: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Word:
    """Représente un mot dans le texte"""
    text: str
    confidence: float
    bounding_box: List[tuple]
    symbols: List[Symbol] = field(default_factory=list)


@dataclass
class Paragraph:
    """Représente un paragraphe dans le texte"""
    text: str
    confidence: float
    bounding_box: List[tuple]
    words: List[Word] = field(default_factory=list)

    # Propriétés de formatage
    alignment: str = 'left'
    avg_font_size: float = 11.0
    dominant_font: str = 'Times New Roman'
    has_bold: bool = False
    has_italic: bool = False
    is_title: bool = False
    all_caps: bool = False

    # Espacements
    spacing_before: float = 0
    spacing_after: float = 12
    line_spacing: float = 1.15


@dataclass
class Block:
    """Représente un bloc de texte dans une page"""
    type: str  # 'TEXT', 'TABLE', 'PICTURE', etc.
    confidence: float
    bounding_box: List[tuple]
    paragraphs: List[Paragraph] = field(default_factory=list)
    text: str = ''


@dataclass
class Page:
    """Représente une page du document"""
    width: int
    height: int
    confidence: float
    blocks: List[Block] = field(default_factory=list)
    page_number: int = 1


@dataclass
class Document:
    """Représente le document complet"""
    full_text: str
    pages: List[Page] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_total_pages(self) -> int:
        """Retourne le nombre total de pages"""
        return len(self.pages)

    def get_total_words(self) -> int:
        """Retourne le nombre total de mots"""
        total = 0
        for page in self.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    total += len(paragraph.words)
        return total

    def get_average_confidence(self) -> float:
        """Retourne la confiance moyenne du document"""
        confidences = []
        for page in self.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    confidences.append(paragraph.confidence)

        if not confidences:
            return 0.0

        return sum(confidences) / len(confidences)
