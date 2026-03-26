# 🤖 Mini-Projet : Configure le pipeline du CEO

## Objectif

Met en place une chaîne CI/CD complète pour un projet Python existant, et crée un raccourci Makefile pour ton confort au quotidien.

## Mission

1. **Le fichier Makefile (L'outil local)**
   - À la racine de ton projet, crée un `Makefile`.
   - Ajoute une commande `make install` pour installer `requirements.txt`.
   - Ajoute une commande `make check` qui lance `ruff check`, `ruff format` et `mypy src/` à la suite.
   - Ajoute une commande `make test` pour lancer `pytest`.

2. **La CI GitHub Actions**
   - Crée le fichier `.github/workflows/ci.yml`.
   - Configure-le pour se déclencher sur tous les pushs vers `main`.
   - L'environnement doit être `ubuntu-latest` avec `python 3.12`.
   - Le pipeline DOIT appeler ton `Makefile` !
     * Exemple de step : `run: make install` puis `run: make check` puis `run: make test`.

## Pourquoi ce projet est important ?

Si tu appliques ces 2 fichiers sur N'IMPORTE QUEL projet Python (même un vieux code dégueulasse de 5 ans), tu vas automatiquement trouver 90% des erreurs (variables non déclarées, imports morts, erreurs de typage, tests cassés) AVANT même de déployer. C'est la marque des professionnels.

## Critères de réussite ✅

- [ ] Lancer `make check` sur ton terminal local fonctionne.
- [ ] Le workflow YAML est syntaxiquement valide.
- [ ] Le pipeline installe bien tes outils de dev (`ruff`, `mypy`, `pytest`).
