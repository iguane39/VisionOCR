# Exemples d'utilisation de VisionOCR

Ce dossier contient des exemples et des cas d'usage pour VisionOCR.

## Exemples de commandes

### 1. Conversion basique
```bash
python main.py convert document.pdf
```

### 2. Conversion avec options avancées
```bash
python main.py convert livre.pdf \
  --output mon_livre_ocr.docx \
  --pages 1-50 \
  --dpi 400 \
  --verbose \
  --show-stats
```

### 3. Traitement par lot
```bash
# Traiter plusieurs PDFs
for pdf in *.pdf; do
  python main.py convert "$pdf" -o "${pdf%.pdf}_ocr.docx"
done
```

### 4. Avec cache désactivé
```bash
python main.py convert document.pdf --no-cache
```

### 5. Pages spécifiques
```bash
# Pages 1 à 10
python main.py convert livre.pdf --pages 1-10

# Pages individuelles
python main.py convert livre.pdf --pages 5,7,9,12,15
```

## Résultats attendus

Après conversion, vous obtiendrez :
- Un document Word (.docx) avec le texte extrait
- Préservation du formatage original
- Styles Word créés automatiquement
- Structure des paragraphes maintenue

## Fichiers d'exemple

Placez vos PDFs de test dans ce dossier pour les essayer :

```
examples/
├── sample_input.pdf       # Votre PDF à tester
└── sample_output.docx     # Résultat attendu
```

## Notes

- Les PDFs scannés donnent de meilleurs résultats à 300 DPI ou plus
- Les documents avec beaucoup d'images peuvent prendre plus de temps
- Le cache accélère considérablement les conversions répétées
