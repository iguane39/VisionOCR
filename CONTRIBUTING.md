# Guide de Contribution à VisionOCR

Merci de votre intérêt pour contribuer à VisionOCR ! Ce document fournit des directives pour contribuer au projet.

## 🚀 Comment Contribuer

### Signaler un Bug

Si vous trouvez un bug, veuillez créer une issue avec :
- Une description claire du problème
- Les étapes pour reproduire le bug
- Le comportement attendu vs le comportement observé
- Votre environnement (OS, version Python, versions des dépendances)
- Les logs pertinents (fichiers dans `logs/`)

### Proposer une Fonctionnalité

Pour proposer une nouvelle fonctionnalité :
1. Vérifiez qu'elle n'existe pas déjà dans les issues
2. Créez une issue décrivant :
   - Le problème que la fonctionnalité résout
   - Comment vous proposez de l'implémenter
   - Les cas d'usage

### Soumettre un Pull Request

1. **Fork** le repository
2. **Créez une branche** pour votre fonctionnalité :
   ```bash
   git checkout -b feature/ma-super-fonctionnalite
   ```
3. **Développez** votre fonctionnalité
4. **Testez** vos changements :
   ```bash
   pytest tests/
   ```
5. **Formatez** le code :
   ```bash
   black .
   flake8 .
   ```
6. **Committez** vos changements :
   ```bash
   git commit -m "Ajout: description claire de la fonctionnalité"
   ```
7. **Push** vers votre fork :
   ```bash
   git push origin feature/ma-super-fonctionnalite
   ```
8. **Créez un Pull Request** avec :
   - Une description claire des changements
   - Les issues résolues (si applicable)
   - Des captures d'écran (si UI)

## 📋 Standards de Code

### Style de Code

- Suivre PEP 8
- Utiliser `black` pour le formatage
- Limiter les lignes à 88 caractères (défaut black)
- Utiliser des docstrings pour toutes les fonctions publiques

### Exemple de Docstring

```python
def ma_fonction(param1: str, param2: int) -> bool:
    """
    Description courte de la fonction.

    Description plus longue si nécessaire, expliquant
    les détails de l'implémentation.

    Args:
        param1: Description du premier paramètre
        param2: Description du deuxième paramètre

    Returns:
        Description de ce qui est retourné

    Raises:
        ValueError: Quand param2 est négatif
    """
    pass
```

### Conventions de Nommage

- **Classes** : `PascalCase` (ex: `VisionAPIClient`)
- **Fonctions/Méthodes** : `snake_case` (ex: `detect_document_text`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `MAX_IMAGE_SIZE`)
- **Variables privées** : `_leading_underscore` (ex: `_cache_key`)

### Tests

- Écrire des tests pour toute nouvelle fonctionnalité
- Maintenir une couverture de code > 80%
- Placer les tests dans le dossier `tests/`
- Nommer les fichiers de test `test_*.py`

```python
# Exemple de test
def test_ma_fonctionnalite():
    """Test de ma fonctionnalité"""
    result = ma_fonction("test", 42)
    assert result is True
```

## 🔍 Structure du Code

### Ajouter un Nouveau Module

1. Créer le fichier dans `modules/`
2. Ajouter les imports nécessaires
3. Documenter toutes les fonctions publiques
4. Créer les tests correspondants dans `tests/`
5. Mettre à jour la documentation si nécessaire

### Modifier l'API Google Vision

Si vous modifiez l'interaction avec l'API :
- Tester avec plusieurs types de documents
- Vérifier l'impact sur les coûts
- Documenter les changements de tarification

## 🐛 Debugging

### Logs

Utiliser le système de logging existant :

```python
from loguru import logger

logger.debug("Message de debug détaillé")
logger.info("Information générale")
logger.warning("Avertissement")
logger.error("Erreur")
logger.success("Opération réussie")
```

### Mode Verbeux

Tester avec différents niveaux de verbosité :
```bash
python main.py convert test.pdf -v      # INFO
python main.py convert test.pdf -vv     # DEBUG
```

## 📚 Documentation

### README

Mettre à jour le README.md si vous :
- Ajoutez une nouvelle fonctionnalité utilisateur
- Changez l'interface CLI
- Modifiez les prérequis

### Code Comments

- Commenter le "pourquoi", pas le "quoi"
- Éviter les commentaires évidents
- Expliquer les décisions complexes

```python
# Bon : explique le raisonnement
# Vision API limite à 20MB, on divise par 2 pour avoir de la marge
MAX_SIZE = 10_000_000

# Mauvais : répète ce que fait le code
# Assigner 10 millions à MAX_SIZE
MAX_SIZE = 10_000_000
```

## 🔐 Sécurité

- **JAMAIS** committer de credentials ou clés API
- Utiliser `.env` pour les secrets
- Vérifier que `.gitignore` est à jour
- Signaler les vulnérabilités en privé

## 🎯 Priorités de Contribution

### High Priority

- Amélioration de la détection de formatage
- Support de nouveaux formats de sortie
- Optimisation des performances
- Correction de bugs

### Medium Priority

- Amélioration de la documentation
- Ajout de tests
- Support de nouvelles langues
- Interface graphique

### Low Priority

- Refactoring du code existant
- Optimisations mineures

## ✅ Checklist avant PR

- [ ] Le code suit les standards PEP 8
- [ ] Les tests passent (`pytest tests/`)
- [ ] Le code est formaté avec `black`
- [ ] La documentation est à jour
- [ ] Les nouvelles fonctionnalités ont des tests
- [ ] Pas de credentials dans le code
- [ ] Les logs sont appropriés
- [ ] Le README est à jour si nécessaire

## 💬 Communication

- Soyez respectueux et professionnel
- Utilisez un langage clair et précis
- Acceptez les critiques constructives
- Aidez les autres contributeurs

## 📖 Ressources

- [Documentation Python](https://docs.python.org/3/)
- [Google Cloud Vision API](https://cloud.google.com/vision/docs)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

## 🙏 Remerciements

Merci de contribuer à VisionOCR ! Chaque contribution, petite ou grande, est appréciée.

---

Des questions ? N'hésitez pas à ouvrir une issue pour discussion !
