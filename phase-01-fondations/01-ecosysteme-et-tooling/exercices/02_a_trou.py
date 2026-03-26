"""
Module 01 — Exercice à trou #2
🎯 Thème : pyproject.toml et structure de packages

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import json
from pathlib import Path

# ============================================================
# PARTIE 1 : Créer une structure de projet programmatiquement
# ============================================================

# On va simuler la création d'un projet Python avec la bonne structure
# C'est comme 'npm init' mais en script Python

def create_project_structure(base_dir: ___) -> None:  # Quel type pour un chemin ?
    """Crée la structure d'un projet Python."""
    
    project_name = "epic_rpg"
    
    # Les dossiers à créer
    directories = [
        base_dir / "src" / project_name,
        base_dir / "___",      # Dossier pour les tests
        base_dir / "docs",
    ]
    
    # Créer chaque dossier
    for dir_path in directories:
        dir_path.mkdir(parents=___, exist_ok=___)  # parents=? pour créer les parents
        print(f"📁 Créé : {dir_path}")
    
    # Créer les fichiers __init__.py
    init_files = [
        base_dir / "src" / project_name / "___",  # Comment s'appelle ce fichier ?
        base_dir / "tests" / "___",                # Même fichier pour les tests
    ]
    
    for init_file in init_files:
        init_file.___(exist_ok=True)  # Quelle méthode de Path crée un fichier vide ?
        print(f"📄 Créé : {init_file}")


# ============================================================
# PARTIE 2 : Générer un pyproject.toml
# ============================================================

def generate_pyproject(base_dir: Path) -> str:
    """Génère le contenu d'un pyproject.toml."""
    
    # En Python, les strings multi-lignes utilisent triple quotes
    # Comme les template literals en JS mais avec """
    
    content = ___"""
[project]
name = "epic-rpg"
version = "0.1.0"
description = "An epic RPG game engine"
requires-python = ">=3.12"
dependencies = [
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
]

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
"""___  # Comment terminer un triple-quoted string ?
    
    # Écrire le fichier
    pyproject_path = base_dir / "pyproject.toml"
    pyproject_path.write_text(content)  # Méthode pratique de Path !
    print(f"📄 Créé : {pyproject_path}")
    
    return content


# ============================================================
# PARTIE 3 : Parser et analyser les dépendances
# ============================================================

def parse_dependencies(pyproject_content: str) -> ___[str]:  # Quel type pour une liste ?
    """
    Parse les dépendances depuis le contenu d'un pyproject.toml.
    Version simplifiée — en vrai on utiliserait le module tomllib.
    """
    deps = []
    in_deps = False
    
    for line in pyproject_content.___("\n"):  # Quelle méthode pour couper par ligne ?
        if "dependencies = [" in line and "optional" not in line:
            in_deps = True
            ___  # Quel mot-clé pour passer à l'itération suivante ?
        
        if in_deps:
            if "]" in line:
                in_deps = False
                ___  # Quel mot-clé pour passer à l'itération suivante ?
            
            # Nettoyer la ligne : enlever espaces, guillemets, virgule
            dep = line.strip().strip('"').strip("',")
            if dep:
                deps.___(dep)  # Quelle méthode pour ajouter à une liste ?
    
    return deps


# ============================================================
# PARTIE 4 : Dictionnaires (comme les objets JS)
# ============================================================

def create_project_manifest() -> ___[str, ___]:  # dict[clé_type, valeur_type]
    """Crée un manifeste de projet (comme package.json)."""
    
    manifest = {
        "name": "epic-rpg",
        "version": "0.1.0",
        "author": "Boss Python",
        "scripts": {
            "start": "python -m epic_rpg",
            "test": "pytest",
            "lint": "ruff check .",
        },
        "python_requires": ">=3.12",
    }
    
    # Accéder aux valeurs (comme en JS)
    print(f"Projet : {manifest[___]}")  # Accéder à la clé 'name'
    
    # .get() = accès safe (retourne None si la clé n'existe pas)
    # Équivalent : manifest?.license en JS
    license_info = manifest.___(___,  "MIT")  # .get avec valeur par défaut
    print(f"License : {license_info}")
    
    # Ajouter une clé
    manifest[___] = "MIT"  # Ajouter la clé 'license'
    
    # Vérifier si une clé existe (comme 'key' in obj en JS — ah bah c'est pareil !)
    has_scripts = ___ in manifest
    print(f"Has scripts : {has_scripts}")
    
    # Itérer sur les clés et valeurs
    print("\n📋 Scripts disponibles :")
    for key, value in manifest["scripts"].___():  # Quelle méthode pour key/value pairs ?
        print(f"  {key}: {value}")
    
    return manifest


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import tempfile
    
    # Créer un dossier temporaire pour le test
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        
        print("=" * 50)
        print("🏗️  CRÉATION DE LA STRUCTURE")
        print("=" * 50)
        create_project_structure(tmp_path)
        
        print("\n" + "=" * 50)
        print("📝 GÉNÉRATION DU PYPROJECT.TOML")
        print("=" * 50)
        content = generate_pyproject(tmp_path)
        
        print("\n" + "=" * 50)
        print("📦 PARSING DES DÉPENDANCES")
        print("=" * 50)
        deps = parse_dependencies(content)
        for dep in deps:
            print(f"  📦 {dep}")
        
        print("\n" + "=" * 50)
        print("📋 MANIFESTE DU PROJET")
        print("=" * 50)
        manifest = create_project_manifest()
        
        print("\n✅ Exercice terminé !")
