# tests/test_format_analyzer.py
"""
Tests unitaires pour le module format_analyzer
"""

import pytest
from modules.format_analyzer import FormatAnalyzer


def test_format_analyzer_init():
    """Test de l'initialisation de FormatAnalyzer"""
    analyzer = FormatAnalyzer(1000, 1400)
    assert analyzer.page_width == 1000
    assert analyzer.page_height == 1400
    assert isinstance(analyzer.font_sizes, list)
    assert isinstance(analyzer.line_heights, list)


def test_detect_alignment_center():
    """Test de détection d'alignement centré"""
    analyzer = FormatAnalyzer(1000, 1400)

    # Paragraphe centré (au milieu de la page)
    bbox = [(450, 100), (550, 100), (550, 120), (450, 120)]
    words = [{'bounding_box': [(450, 100), (550, 100), (550, 120), (450, 120)]}]

    alignment = analyzer._detect_alignment(bbox, words)
    assert alignment == 'center'


def test_detect_alignment_left():
    """Test de détection d'alignement à gauche"""
    analyzer = FormatAnalyzer(1000, 1400)

    # Paragraphe aligné à gauche
    bbox = [(50, 100), (300, 100), (300, 120), (50, 120)]
    words = [{'bounding_box': [(50, 100), (300, 100), (300, 120), (50, 120)]}]

    alignment = analyzer._detect_alignment(bbox, words)
    assert alignment == 'left'


def test_is_all_caps():
    """Test de détection de texte en majuscules"""
    analyzer = FormatAnalyzer(1000, 1400)

    assert analyzer._is_all_caps("TOUT EN MAJUSCULES") is True
    assert analyzer._is_all_caps("Texte Normal") is False
    assert analyzer._is_all_caps("PRESQUE TOUT en majuscules") is False
    assert analyzer._is_all_caps("") is False


def test_is_title():
    """Test de détection de titre"""
    analyzer = FormatAnalyzer(1000, 1400)

    # Un titre typique : court, en majuscules, grande police
    paragraph = {
        'text': 'CHAPITRE I',
        'bounding_box': [(400, 100), (600, 100), (600, 130), (400, 130)]
    }
    font_analysis = {
        'avg_size': 16,
        'dominant_font': 'Times New Roman',
        'has_bold': True,
        'has_italic': False
    }

    is_title = analyzer._is_title(paragraph, font_analysis)
    assert is_title is True

    # Un paragraphe normal : long, taille normale
    paragraph_normal = {
        'text': 'Ceci est un paragraphe normal de texte qui est beaucoup plus long qu\'un titre et ne devrait pas être détecté comme titre.',
        'bounding_box': [(100, 100), (900, 100), (900, 120), (100, 120)]
    }
    font_analysis_normal = {
        'avg_size': 11,
        'dominant_font': 'Times New Roman',
        'has_bold': False,
        'has_italic': False
    }

    is_title = analyzer._is_title(paragraph_normal, font_analysis_normal)
    assert is_title is False


def test_calculate_spacing():
    """Test du calcul des espacements"""
    analyzer = FormatAnalyzer(1000, 1400)

    current_para = {
        'bounding_box': [(100, 200), (900, 200), (900, 220), (100, 220)]
    }
    previous_para = {
        'bounding_box': [(100, 100), (900, 100), (900, 120), (100, 120)]
    }

    spacing = analyzer.calculate_spacing(current_para, previous_para)

    assert 'spacing_before' in spacing
    assert 'spacing_after' in spacing
    assert 'line_spacing' in spacing
    assert spacing['spacing_before'] >= 0
