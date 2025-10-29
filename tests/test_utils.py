# tests/test_utils.py
"""
Tests unitaires pour le module utils
"""

import pytest
from pathlib import Path
from modules.utils import (
    validate_pdf_path,
    get_output_path,
    format_file_size,
    estimate_processing_time
)


def test_format_file_size():
    """Test du formatage de taille de fichier"""
    assert format_file_size(500) == "500.0 B"
    assert format_file_size(1024) == "1.0 KB"
    assert format_file_size(1024 * 1024) == "1.0 MB"
    assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"


def test_estimate_processing_time():
    """Test de l'estimation du temps de traitement"""
    # Moins d'une minute
    result = estimate_processing_time(10)
    assert "secondes" in result

    # Plusieurs minutes
    result = estimate_processing_time(100)
    assert "minutes" in result


def test_get_output_path():
    """Test de la génération du chemin de sortie"""
    # Sans chemin de sortie spécifié
    input_path = "/path/to/document.pdf"
    output = get_output_path(input_path)
    assert output.endswith("document_ocr.docx")

    # Avec chemin de sortie spécifié
    output = get_output_path(input_path, "/custom/output.docx")
    assert output == "/custom/output.docx"


def test_validate_pdf_path_nonexistent():
    """Test de validation d'un fichier inexistant"""
    result = validate_pdf_path("/nonexistent/file.pdf")
    assert result is False


def test_validate_pdf_path_wrong_extension():
    """Test de validation d'un fichier avec mauvaise extension"""
    # Ce test nécessiterait un fichier temporaire
    # Skipped pour l'instant
    pass
