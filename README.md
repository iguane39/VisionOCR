# VisionOCR - PDF to Word with Google Cloud Vision API

Application Python en ligne de commande pour convertir des PDFs scannés en documents Word (.docx) avec reconnaissance avancée du texte et préservation du formatage grâce à **Google Cloud Vision API**.

## 🌟 Fonctionnalités

- **OCR de qualité supérieure** : Précision >99% avec Google Cloud Vision API
- **Préservation du formatage** : Polices, styles, alignements, espacements
- **Détection automatique** : Structure du document (blocs, paragraphes, mots)
- **Cache intelligent** : Économise les coûts en évitant les appels API redondants
- **Support multi-langues** : 60+ langues avec détection automatique
- **Traitement par lot** : Conversion efficace de documents multi-pages
- **Interface CLI intuitive** : Facile à utiliser et à automatiser

## 📋 Prérequis

### Système

- Python 3.8 ou supérieur
- poppler-utils (pour la conversion PDF)

#### Installation de poppler :

**Ubuntu/Debian :**
```bash
sudo apt-get install poppler-utils
```

**macOS :**
```bash
brew install poppler
```

**Windows :**
Téléchargez depuis [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) et ajoutez au PATH.

### Google Cloud

- Compte Google Cloud avec Vision API activé
- Fichier `credentials.json` de compte de service

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd VisionOCR
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer Google Cloud Vision API

Suivez les instructions détaillées :

```bash
python main.py setup
```

**Résumé rapide :**

1. Créez un projet sur [Google Cloud Console](https://console.cloud.google.com/)
2. Activez l'API Cloud Vision
3. Créez un compte de service avec le rôle "Cloud Vision API User"
4. Téléchargez le fichier JSON de credentials
5. Placez-le dans `credentials/google_credentials.json`

### 5. Configuration des variables d'environnement

```bash
cp .env.example .env
# Éditez .env avec vos paramètres
```

## 📖 Utilisation

### Commande de base

```bash
python main.py convert document.pdf
```

### Exemples avancés

**Convertir avec chemin de sortie personnalisé :**
```bash
python main.py convert livre.pdf -o mon_livre.docx
```

**Convertir uniquement certaines pages :**
```bash
python main.py convert livre.pdf --pages 1-10
python main.py convert livre.pdf --pages 5,7,9,12
```

**Augmenter la qualité (DPI plus élevé) :**
```bash
python main.py convert document.pdf --dpi 400
```

**Forcer un nouvel OCR (sans cache) :**
```bash
python main.py convert document.pdf --no-cache
```

**Mode verbeux avec statistiques :**
```bash
python main.py convert document.pdf -vv --show-stats
```

**Utiliser un fichier credentials différent :**
```bash
python main.py convert document.pdf -c /path/to/credentials.json
```

### Organisation avec le dossier pdf/

Le projet inclut un dossier `pdf/` organisé pour faciliter la gestion de vos documents :

```bash
# 1. Placez vos PDFs dans pdf/input/
cp mon_document.pdf pdf/input/

# 2. Convertissez avec sortie automatique dans pdf/output/
python main.py convert pdf/input/mon_document.pdf -o pdf/output/mon_document.docx

# 3. Conversion par lot de tous les PDFs
for pdf in pdf/input/*.pdf; do
  filename=$(basename "$pdf" .pdf)
  python main.py convert "$pdf" -o "pdf/output/${filename}_ocr.docx"
done
```

**Voir `pdf/README.md` pour plus de détails sur l'organisation des fichiers.**

### Options complètes

```
Options:
  -o, --output PATH              Chemin du fichier de sortie
  -p, --pages TEXT               Pages à traiter (ex: 1-10, 5,7,9, all)
  --dpi INTEGER                  Résolution DPI (défaut: 300)
  -c, --credentials PATH         Chemin vers credentials.json
  --no-cache                     Désactiver le cache API
  --create-styles / --no-create-styles  Créer des styles Word
  -v, --verbose                  Augmenter la verbosité (-v, -vv, -vvv)
  --show-stats                   Afficher les statistiques API
  --help                         Afficher l'aide
```

## 📁 Structure du Projet

```
VisionOCR/
├── main.py                     # Point d'entrée CLI
├── config.py                   # Configuration centrale
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── .env.example               # Template configuration
├── .gitignore                 # Fichiers à ignorer
│
├── credentials/
│   └── google_credentials.json  # Clés API (non versionné)
│
├── pdf/                        # Dossier de travail pour PDFs
│   ├── README.md              # Guide d'organisation
│   ├── input/                 # PDFs à traiter (placez vos fichiers ici)
│   │   └── README.md          # Instructions détaillées
│   └── output/                # Documents Word générés
│       └── README.md          # Informations sur les résultats
│
├── modules/
│   ├── __init__.py
│   ├── vision_api_client.py    # Interface Google Vision API
│   ├── format_analyzer.py      # Analyse du formatage
│   ├── docx_builder.py         # Construction Word
│   ├── pdf_processor.py        # Conversion PDF → images
│   └── utils.py                # Fonctions utilitaires
│
├── models/
│   ├── __init__.py
│   └── document_structure.py   # Classes de données
│
├── tests/                      # Tests unitaires
│   └── __init__.py
│
├── examples/                   # Exemples de documents
│
└── logs/                       # Fichiers de log
```

## 🎯 Fonctionnement

L'application fonctionne en 4 étapes :

1. **Conversion PDF → Images** : Transformation des pages PDF en images haute résolution (300 DPI)
2. **OCR avec Vision API** : Envoi des images à Google Cloud Vision pour reconnaissance du texte
3. **Analyse du formatage** : Extraction des informations de style, alignement, tailles de police
4. **Construction Word** : Génération du document .docx avec préservation du formatage

## 💰 Tarification Google Cloud Vision API

- **1000 premières pages/mois** : GRATUIT
- **Pages suivantes** : $1.50 / 1000 pages
- **Cache** : Réduit drastiquement les coûts en évitant les appels répétés

### Exemple de coûts :
- Document de 50 pages (première fois) : $0.075
- Même document (avec cache) : $0.00
- Livre de 300 pages : $0.45

## 🔧 Configuration Avancée

### Fichier `config.py`

Personnalisez les paramètres dans `config.py` :

```python
# DPI pour la conversion
DPI_DEFAULT = 300  # Plus élevé = meilleure qualité mais plus lent

# Cache
CACHE_ENABLED = True
CACHE_TTL = 86400 * 30  # 30 jours

# Polices par défaut
DEFAULT_SERIF_FONT = 'Times New Roman'
DEFAULT_SANS_SERIF_FONT = 'Arial'

# Performance
MAX_WORKERS = 4  # Nombre de workers parallèles
```

## 🧪 Tests

Pour exécuter les tests (une fois pytest installé) :

```bash
pytest tests/
```

## 🐛 Dépannage

### Erreur "poppler not found"
- Assurez-vous que poppler-utils est installé
- Vérifiez que poppler est dans votre PATH

### Erreur "credentials not found"
- Vérifiez que `credentials.json` existe dans `credentials/`
- Ou définissez `GOOGLE_APPLICATION_CREDENTIALS` dans `.env`

### Erreur "Vision API quota exceeded"
- Vérifiez votre quota sur Google Cloud Console
- Attendez la réinitialisation mensuelle ou augmentez votre quota

### Qualité OCR insuffisante
- Augmentez le DPI : `--dpi 400`
- Vérifiez la qualité du PDF source
- Assurez-vous que les images ne sont pas trop floues

## 📊 Performances

### Temps de traitement typique
- Page simple (300 DPI) : ~2-3 secondes
- Livre 300 pages : ~15-20 minutes
- Utilisation cache : instantané

### Optimisations
- Le cache évite les appels API répétés
- Traitement parallèle de la conversion PDF
- Compression automatique des images >20 MB

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🔗 Liens Utiles

- [Documentation Google Cloud Vision API](https://cloud.google.com/vision/docs)
- [Google Cloud Console](https://console.cloud.google.com/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [pdf2image GitHub](https://github.com/Belval/pdf2image)

## 📧 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation Google Cloud Vision
- Vérifier les logs dans le dossier `logs/`

## ⚠️ Notes Importantes

- **Sécurité** : Ne JAMAIS commiter `credentials.json` sur Git
- **Confidentialité** : Les données envoyées à Google sont soumises à leur politique de confidentialité
- **Cache** : Le cache stocke les résultats OCR localement pour réutilisation
- **Coûts** : Surveillez votre utilisation sur Google Cloud Console

## 🎓 Cas d'Usage

- Numérisation de livres et documents anciens
- Conversion de factures et documents administratifs
- Archivage numérique de documents papier
- Extraction de texte de documents scannés
- Conversion de manuels et documentation technique

---

**Développé avec ❤️ pour une OCR de qualité professionnelle**
