# 🎮 Mini-Projet : Système de Sauvegarde de Jeu RPG

## Objectif

Construis un **système de sauvegarde complet** pour un jeu RPG, utilisant tout ce que tu as appris : exceptions custom, context managers, typing avancé et dataclasses.

## Cahier des charges

### Fonctionnalités

1. **Multi-slot save** : 5 slots de sauvegarde
2. **Auto-save** : sauvegarde automatique toutes les X secondes
3. **Backup & Restore** : backup avant chaque sauvegarde, rollback en cas d'erreur
4. **Integrity check** : checksum MD5 pour détecter la corruption
5. **Version check** : gestion de la compatibilité entre versions de save
6. **Event system** : notifications pour chaque action (save, load, delete)

### Exceptions à implémenter

```python
class SaveError(Exception): ...
class CorruptedSaveError(SaveError): ...   # Checksum invalide
class SaveSlotFullError(SaveError): ...     # Tous les slots pris
class SaveVersionError(SaveError): ...      # Version incompatible
class SaveNotFoundError(SaveError): ...     # Slot vide
```

### Context managers à implémenter

```python
# Transaction atomique
with save_manager.transaction(slot_id=1) as save:
    save.update_state(new_state)
    # Si erreur → rollback automatique

# Auto-save
with save_manager.auto_save(state, interval=30.0):
    # Le jeu tourne...
    # Sauvegarde auto toutes les 30s
    pass

# Locked save (empêche les accès concurrents)
with save_manager.lock(slot_id=1):
    state = save_manager.load(1)
    state.level += 1
    save_manager.save(1, state)
```

### Commandes CLI attendues

```bash
python -m save_system save --slot 1 --name "Avant le boss"
python -m save_system load --slot 1
python -m save_system list
python -m save_system delete --slot 1
python -m save_system verify --slot 1  # Vérifie l'intégrité
python -m save_system export --slot 1 --output save.json
python -m save_system import --input save.json --slot 2
```

## Structure attendue

```
mini-projet/
├── save_system/
│   ├── __init__.py
│   ├── __main__.py       # CLI avec argparse
│   ├── exceptions.py     # Hiérarchie d'exceptions
│   ├── models.py         # GameState, SaveMetadata (dataclasses)
│   ├── manager.py        # SaveManager avec context managers
│   ├── integrity.py      # Checksum, validation
│   └── events.py         # EventBus typé
├── tests/
│   ├── test_manager.py
│   ├── test_integrity.py
│   └── test_events.py
└── pyproject.toml
```

## Critères de réussite ✅

- [ ] Hiérarchie d'exceptions custom complète
- [ ] Context managers pour transaction et auto-save
- [ ] Checksum MD5 pour l'intégrité des sauvegardes
- [ ] Version check avec erreur descriptive
- [ ] Event bus typé avec Callable et Literal
- [ ] Dataclasses pour les modèles (GameState, SaveMetadata)
- [ ] Typing strict (passe `mypy --strict`)
- [ ] Au moins 5 tests avec pytest
- [ ] CLI fonctionnel avec argparse

## Bonus 🌟

- Compression des sauvegardes avec `gzip`
- Encryption basique des sauvegardes
- Migration automatique entre versions de save
- Cloud sync simulé (copie vers un dossier "cloud")
