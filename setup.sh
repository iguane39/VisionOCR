#!/bin/bash
# setup.sh - Script d'installation pour VisionOCR

set -e  # Arrêter en cas d'erreur

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║            Installation de VisionOCR v1.0.0                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier Python
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION détecté"

# Vérifier poppler
echo ""
echo "🔍 Vérification de poppler-utils..."
if ! command -v pdftopp &> /dev/null && ! command -v pdftoppm &> /dev/null; then
    echo "⚠️  poppler-utils n'est pas installé"
    echo "Installation recommandée :"
    echo "  - Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "  - macOS: brew install poppler"
    echo "  - Windows: https://github.com/oschwartz10612/poppler-windows/releases/"
    echo ""
    read -p "Continuer sans poppler ? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ poppler-utils installé"
fi

# Créer un environnement virtuel
echo ""
echo "📦 Création de l'environnement virtuel..."
if [ -d "venv" ]; then
    echo "⚠️  L'environnement virtuel existe déjà"
    read -p "Le recréer ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Environnement virtuel recréé"
    fi
else
    python3 -m venv venv
    echo "✓ Environnement virtuel créé"
fi

# Activer l'environnement virtuel
echo ""
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo ""
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Dépendances installées"

# Créer les répertoires nécessaires
echo ""
echo "📁 Création des répertoires..."
mkdir -p credentials logs .cache/vision_api examples/input examples/output
echo "✓ Répertoires créés"

# Copier .env.example vers .env si nécessaire
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "✓ Fichier .env créé (à configurer)"
fi

# Instructions finales
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  Installation terminée ! 🎉                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Prochaines étapes :"
echo ""
echo "1. Configurer Google Cloud Vision API :"
echo "   python main.py setup"
echo ""
echo "2. Placer votre fichier credentials.json dans le dossier credentials/"
echo ""
echo "3. (Optionnel) Éditer le fichier .env avec vos paramètres"
echo ""
echo "4. Tester l'installation :"
echo "   python main.py --help"
echo ""
echo "5. Convertir votre premier PDF :"
echo "   python main.py convert votre_document.pdf"
echo ""
echo "📖 Documentation complète : README.md"
echo ""
echo "Pour activer l'environnement virtuel :"
echo "   source venv/bin/activate"
echo ""
