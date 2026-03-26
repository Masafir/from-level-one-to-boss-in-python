# Module 16 — CI / CD avec Python et GitHub Actions 🤖

> **Objectif** : Automatiser l'assurance qualité de ton code. Un bon dev Fullstack ne déploie jamais à la main.

## 1. C'est quoi la CI/CD ?

*   **CI (Continuous Integration)** : À chaque Push ou Pull Request sur Git, un robot va installer tes dépendances, vérifier le format du code (Lint/Typecheck), et lancer les tests unitaires. Si ça casse, on bloque la PR !
*   **CD (Continuous Deployment)** : Si la CI est verte et que ça arrive sur la branche `main`, le robot déploie l'application sur ton serveur ou pousse ton image sur le Docker Hub.

Avec GitHub, l'outil numéro 1 est **GitHub Actions**. C'est globalement un fichier YAML.

## 2. Le Linting & Formatting en Python

Avant d'écrire la CI, il faut les bons outils pour que la CI puisse inspecter ton code.
Le standard actuel (2025) tourne autour d'un seul outil incroyablement rapide (écrit en Rust) : **Ruff**.
Puis on rajoute **Mypy** pour le typage.

```bash
# Installation
pip install ruff mypy pytest

# 1. Vérifie si le code respecte les standards PEP8 (Linter)
ruff check .

# 2. Re-formate le code proprement (Formatter = le Prettier de Python)
ruff format .

# 3. Vérifie que tes types (les Type Hints) sont logiques
mypy src/
```

> Tu intègres ces commandes dans ta CI pour bloquer le code sale.

## 3. Écrire le fichier GitHub Action (CI)

Dans ton projet, crée le dossier `.github/workflows/` et ajoute `ci.yml`.

```yaml
# .github/workflows/ci.yml
name: Python App CI

# Quand déclencher ce workflow ?
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build_and_test:
    runs-on: ubuntu-latest  # Le serveur gratuit prêté par GitHub

    steps:
    # 1. Copier le code sur le serveur GitHub
    - name: Checkout code
      uses: actions/checkout@v4

    # 2. Installer Python
    - name: Set up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        # Optionnel: Cache pip pour aller plus vite la prochaine fois
        cache: 'pip'

    # 3. Installer les dépendances 
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install ruff mypy pytest pytest-cov
        # S'il y a un requirements.txt :
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    # 4. Linting (Ruff Check)
    - name: Run Ruff Linter
      run: ruff check .

    # 5. Typechecking (Mypy)
    - name: Run Mypy Type Checking
      run: mypy src/ --strict

    # 6. Tests (Pytest) avec rapport de couverture
    - name: Run Tests
      # Si on a besoin de variables d'environnement bidons pour les tests
      env:
        DATABASE_URL: sqlite:///:memory:
        SECRET_KEY: test_secret
      run: |
        pytest --cov=src --cov-fail-under=80 -v
```

## 4. Pipeline CD : Pousser sur Docker Hub

Une fois la CI testée et approuvée, on peut pousser l'image Docker sur un registre (ex: Docker Hub ou GitHub Container Registry).

```yaml
# .github/workflows/cd.yml
name: Build and Push Docker Image

on:
  push:
    # Déclencher uniquement quand on crée un nouveau tag git (ex: v1.0.0)
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Logins via les "Secrets" configurés sur GitHub (Settings > Secrets and variables)
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # Build et Push
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/my-python-api:latest,${{ secrets.DOCKERHUB_USERNAME }}/my-python-api:${{ github.ref_name }}
```

## 5. Le `Makefile` : Le meilleur ami du Dev

Pour éviter de taper `ruff check .` puis `ruff format .` puis `pytest` 50 fois par jour avant de push, le standard est d'utiliser un vieux mais indémodable fichier `Makefile` à la racine de ton projet.

```makefile
# Makefile
.PHONY: format lint test check

format:
	ruff format .

lint:
	ruff check .
	mypy src/

test:
	pytest -v

# The ultimate check avant de commit !
check: format lint test
```

Sur ton mac, tu tapes juste `make check` dans le terminal, et ça lance toute ta suite qualité comme le  ferait la CI. C'est l'équivalent des scripts dans un fichier `package.json` en Node.

---

## 🎯 Résumé

| Concept | Équivalent Node | Outil Python |
|---------|-----------------|--------------|
| **CI/CD** | Actions / GitLab CI | GitHub Actions (`.github/workflows/*.yml`) |
| **Linter** | ESLint | `ruff check` |
| **Formatter** | Prettier | `ruff format` |
| **Type Checker** | TypeScript Compiler | `mypy` |
| **Scripts alias** | `npm run lint` | `make lint` (via `Makefile`) |

---

➡️ **Passe aux exercices pour écrire ton premier workflow GitHub !**
