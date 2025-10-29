# Dossier des PDFs à traiter

Ce dossier contient les fichiers PDF scannés à convertir en documents Word.

## Utilisation

1. **Placez vos PDFs ici** pour les traiter avec VisionOCR
2. **Exécutez la conversion** depuis le répertoire racine du projet

## Exemples de commandes

### Convertir un PDF spécifique

```bash
# Depuis la racine du projet
python main.py convert pdf/input/mon_document.pdf
```

Le fichier de sortie sera automatiquement créé avec le suffixe `_ocr.docx` dans le même dossier.

### Convertir avec sortie personnalisée

```bash
python main.py convert pdf/input/mon_document.pdf -o pdf/output/mon_document.docx
```

### Convertir tous les PDFs du dossier

```bash
# Script bash pour convertir tous les PDFs
for pdf in pdf/input/*.pdf; do
  filename=$(basename "$pdf" .pdf)
  python main.py convert "$pdf" -o "pdf/output/${filename}_ocr.docx"
done
```

### Windows (PowerShell)

```powershell
Get-ChildItem pdf\input\*.pdf | ForEach-Object {
  $outputName = "pdf\output\$($_.BaseName)_ocr.docx"
  python main.py convert $_.FullName -o $outputName
}
```

## Conseils

### Pour de meilleurs résultats :

- **Qualité du scan** : Utilisez au moins 300 DPI
- **Format** : PDF avec images claires et nettes
- **Taille** : Les grands fichiers peuvent prendre plus de temps
- **Langue** : L'API détecte automatiquement plus de 60 langues

### Options utiles :

```bash
# Augmenter la qualité (DPI plus élevé)
python main.py convert pdf/input/document.pdf --dpi 400

# Traiter uniquement certaines pages
python main.py convert pdf/input/livre.pdf --pages 1-50

# Mode verbeux pour voir les détails
python main.py convert pdf/input/document.pdf -vv

# Afficher les statistiques d'utilisation API
python main.py convert pdf/input/document.pdf --show-stats

# Forcer un nouvel OCR (sans cache)
python main.py convert pdf/input/document.pdf --no-cache
```

## Structure attendue

```
pdf/input/
├── document1.pdf
├── document2.pdf
├── livre_chapitre1.pdf
└── facture_2024.pdf
```

Après traitement, les résultats seront dans `pdf/output/` :

```
pdf/output/
├── document1_ocr.docx
├── document2_ocr.docx
├── livre_chapitre1_ocr.docx
└── facture_2024_ocr.docx
```

## Types de documents supportés

- Documents scannés (livres, magazines, articles)
- Factures et documents administratifs
- Lettres et correspondance
- Formulaires papier numérisés
- Documents manuscrits (résultats variables)
- Archives historiques

## Limites

- **Taille maximale** : 20 MB par image (après conversion PDF)
- **Format** : PDFs uniquement (pour images, utilisez pdf2image d'abord)
- **Qualité** : Meilleurs résultats avec texte imprimé net

## Support

Pour toute question, consultez :
- Documentation principale : `README.md`
- Configuration : `python main.py setup`
- Aide : `python main.py convert --help`
