# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2025-10-29

### Ajouté
- Application CLI complète pour conversion PDF vers Word
- Intégration avec Google Cloud Vision API
- Module `vision_api_client.py` avec cache intelligent
- Module `format_analyzer.py` pour analyse du formatage
- Module `docx_builder.py` pour construction des documents Word
- Module `pdf_processor.py` pour conversion PDF vers images
- Système de cache pour économiser les appels API
- Support multi-pages avec sélection de pages (all, 1-10, 5,7,9)
- Configuration DPI ajustable (défaut: 300)
- Détection automatique de la structure du document
- Préservation du formatage (polices, styles, alignements)
- Logs détaillés avec loguru
- Barres de progression avec tqdm
- Mode verbeux (-v, -vv, -vvv)
- Statistiques d'utilisation de l'API (--show-stats)
- Commande `setup` pour instructions de configuration
- Documentation complète (README.md, CONTRIBUTING.md)
- Tests unitaires de base
- Fichier de configuration centralisé (config.py)
- Support des variables d'environnement (.env)

### Fonctionnalités
- OCR de qualité supérieure (>99% de précision)
- Détection automatique de 60+ langues
- Création de styles Word réutilisables
- Analyse d'alignement (gauche, centre, droite, justifié)
- Détection de titres automatique
- Calcul intelligent des espacements
- Gestion des polices (serif, sans-serif, monospace)
- Support des paragraphes, blocs et structures complexes

### Technique
- Architecture modulaire et extensible
- Type hints pour meilleure maintenabilité
- Gestion d'erreurs robuste
- Nettoyage automatique des fichiers temporaires
- Support du traitement parallèle
- Optimisation de la taille des images

### Documentation
- README complet avec exemples
- Guide de contribution
- Documentation des modules
- Exemples d'utilisation
- Instructions de configuration Google Cloud

## [Non publié]

### À venir
- Interface graphique (GUI)
- Support de formats de sortie additionnels (HTML, Markdown)
- Traitement par lot amélioré
- Détection de tableaux
- Support des images dans le document
- Amélioration de la détection de police
- Support du formatage avancé (gras, italique, souligné)
- Mode de correction orthographique
- Export de statistiques détaillées
- API REST pour intégration
- Support Docker
- CI/CD avec GitHub Actions

### Corrections prévues
- Améliorer la détection d'alignement justifié
- Optimiser le clustering de styles
- Réduire le temps de traitement
- Améliorer la gestion des polices non standard

---

## Types de changements

- **Ajouté** : pour les nouvelles fonctionnalités
- **Modifié** : pour les changements dans les fonctionnalités existantes
- **Déprécié** : pour les fonctionnalités bientôt supprimées
- **Supprimé** : pour les fonctionnalités supprimées
- **Corrigé** : pour les corrections de bugs
- **Sécurité** : en cas de vulnérabilités
