# Dossier PDF - Organisation des fichiers

Ce dossier organise vos fichiers PDF et les documents Word générés après OCR.

## Structure

```
pdf/
├── input/          # PDFs à traiter (placez vos fichiers ici)
│   ├── README.md   # Guide d'utilisation détaillé
│   └── *.pdf       # Vos PDFs scannés
│
└── output/         # Documents Word générés (résultats OCR)
    ├── README.md   # Informations sur les résultats
    └── *.docx      # Documents convertis
```

## Workflow rapide

### 1. Ajouter un PDF à traiter

```bash
# Copier votre PDF dans le dossier input
cp /chemin/vers/votre_document.pdf pdf/input/
```

### 2. Lancer la conversion

```bash
# Depuis la racine du projet
python main.py convert pdf/input/votre_document.pdf -o pdf/output/votre_document.docx
```

### 3. Récupérer le résultat

Le document Word sera dans `pdf/output/votre_document.docx`

## Conversion en lot

### Linux/macOS

```bash
#!/bin/bash
# Script de conversion par lot

for pdf in pdf/input/*.pdf; do
  filename=$(basename "$pdf" .pdf)
  echo "Traitement de $filename..."
  python main.py convert "$pdf" -o "pdf/output/${filename}_ocr.docx"
done

echo "Conversion terminée ! Résultats dans pdf/output/"
```

### Windows (PowerShell)

```powershell
# Script de conversion par lot
Get-ChildItem pdf\input\*.pdf | ForEach-Object {
  $outputName = "pdf\output\$($_.BaseName)_ocr.docx"
  Write-Host "Traitement de $($_.Name)..."
  python main.py convert $_.FullName -o $outputName
}

Write-Host "Conversion terminée ! Résultats dans pdf\output\"
```

## Organisation recommandée

### Pour des projets spécifiques

```
pdf/
├── input/
│   ├── projet_a/
│   │   ├── chapitre1.pdf
│   │   └── chapitre2.pdf
│   └── projet_b/
│       ├── document1.pdf
│       └── document2.pdf
│
└── output/
    ├── projet_a/
    │   ├── chapitre1_ocr.docx
    │   └── chapitre2_ocr.docx
    └── projet_b/
        ├── document1_ocr.docx
        └── document2_ocr.docx
```

### Conversion avec sous-dossiers

```bash
# Créer les sous-dossiers de sortie
mkdir -p pdf/output/projet_a

# Convertir avec chemin complet
python main.py convert pdf/input/projet_a/chapitre1.pdf \
  -o pdf/output/projet_a/chapitre1_ocr.docx
```

## Commandes utiles

### Voir tous les PDFs à traiter

```bash
ls -lh pdf/input/*.pdf
```

### Compter les PDFs

```bash
ls pdf/input/*.pdf | wc -l
```

### Voir la taille totale

```bash
du -sh pdf/input/
du -sh pdf/output/
```

### Nettoyer les fichiers traités

```bash
# Sauvegarder d'abord !
# Puis supprimer les PDFs traités
rm pdf/input/*.pdf

# Ou archiver avant de supprimer
tar -czf archive_pdfs_$(date +%Y%m%d).tar.gz pdf/input/*.pdf
rm pdf/input/*.pdf
```

## Bonnes pratiques

### 1. Nommage des fichiers

✅ **Bon** :
- `rapport_annuel_2024.pdf`
- `facture_client_001.pdf`
- `livre_chapitre_01.pdf`

❌ **À éviter** :
- `Document1.pdf`
- `Scan 2024-01-01.pdf`
- `IMG_20240101.pdf`

### 2. Organisation

- Un dossier par projet dans `input/` et `output/`
- Noms descriptifs et cohérents
- Archivage régulier des fichiers traités

### 3. Sauvegarde

```bash
# Script de backup automatique
backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp -r pdf/input "$backup_dir/"
cp -r pdf/output "$backup_dir/"
echo "Backup créé dans $backup_dir"
```

## Options de conversion avancées

### Haute qualité (DPI élevé)

```bash
python main.py convert pdf/input/document.pdf \
  -o pdf/output/document.docx \
  --dpi 400
```

### Pages spécifiques

```bash
# Pages 1 à 50
python main.py convert pdf/input/livre.pdf \
  -o pdf/output/livre_extrait.docx \
  --pages 1-50

# Pages individuelles
python main.py convert pdf/input/document.pdf \
  -o pdf/output/pages_selectionnees.docx \
  --pages 5,7,9,12
```

### Mode verbeux avec statistiques

```bash
python main.py convert pdf/input/document.pdf \
  -o pdf/output/document.docx \
  -vv \
  --show-stats
```

## Taille et limites

### Limites techniques
- **Taille maximale par image** : 20 MB (après conversion PDF)
- **DPI recommandé** : 300 (minimum)
- **Format supporté** : PDF uniquement

### Temps de traitement estimé
| Taille du PDF | Pages | Temps estimé |
|---------------|-------|--------------|
| < 5 MB        | 1-10  | ~30 secondes |
| 10-50 MB      | 10-50 | ~2-3 minutes |
| 50-100 MB     | 50-100| ~5-8 minutes |
| > 100 MB      | 100+  | ~10+ minutes |

## Dépannage

### Erreur : "Fichier trop volumineux"
Solution : Augmentez la compression ou divisez le PDF

```bash
# Diviser un PDF avec ghostscript
gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
   -dFirstPage=1 -dLastPage=50 \
   -sOutputFile=pdf/input/partie1.pdf \
   original.pdf
```

### Erreur : "poppler not found"
Solution : Installer poppler-utils

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### Qualité OCR insuffisante
Solutions :
1. Augmenter le DPI : `--dpi 400`
2. Vérifier la qualité du PDF source
3. Re-scanner le document si possible

## Support

Pour plus d'informations :
- `pdf/input/README.md` - Guide d'utilisation détaillé
- `pdf/output/README.md` - Informations sur les résultats
- `README.md` (racine) - Documentation complète
- `python main.py convert --help` - Aide en ligne

## Statistiques et coûts

### Vérifier les statistiques

```bash
python main.py convert pdf/input/document.pdf \
  -o pdf/output/document.docx \
  --show-stats
```

Affiche :
- Nombre d'appels API
- Utilisation du cache
- Coût estimé
- Temps de traitement

### Optimiser les coûts

1. **Utiliser le cache** (activé par défaut)
2. **Traiter uniquement les pages nécessaires** (`--pages`)
3. **Grouper les conversions** pour éviter les redémarrages

## Exemples pratiques

### 1. Convertir un livre chapitre par chapitre

```bash
# Diviser le livre en chapitres (avec un outil externe)
# Puis convertir chaque chapitre
for i in {1..10}; do
  python main.py convert "pdf/input/chapitre_$i.pdf" \
    -o "pdf/output/chapitre_$i.docx"
done
```

### 2. Convertir uniquement les pages impaires

```bash
python main.py convert pdf/input/document.pdf \
  -o pdf/output/pages_impaires.docx \
  --pages 1,3,5,7,9,11,13,15
```

### 3. Conversion haute qualité pour archivage

```bash
python main.py convert pdf/input/archive.pdf \
  -o pdf/output/archive_hq.docx \
  --dpi 600 \
  --create-styles \
  -vv
```

---

**Bonne conversion ! 📄➡️📝**
