"""
Module 01 — Solution exercice à trou #2
"""

import json
from pathlib import Path


def create_project_structure(base_dir: Path) -> None:
    """Crée la structure d'un projet Python."""
    project_name = "epic_rpg"

    directories = [
        base_dir / "src" / project_name,
        base_dir / "tests",
        base_dir / "docs",
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Créé : {dir_path}")

    init_files = [
        base_dir / "src" / project_name / "__init__.py",
        base_dir / "tests" / "__init__.py",
    ]

    for init_file in init_files:
        init_file.touch(exist_ok=True)
        print(f"📄 Créé : {init_file}")


def generate_pyproject(base_dir: Path) -> str:
    """Génère le contenu d'un pyproject.toml."""
    content = """\
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
"""

    pyproject_path = base_dir / "pyproject.toml"
    pyproject_path.write_text(content)
    print(f"📄 Créé : {pyproject_path}")

    return content


def parse_dependencies(pyproject_content: str) -> list[str]:
    """Parse les dépendances depuis le contenu pyproject.toml."""
    deps = []
    in_deps = False

    for line in pyproject_content.split("\n"):
        if "dependencies = [" in line and "optional" not in line:
            in_deps = True
            continue

        if in_deps:
            if "]" in line:
                in_deps = False
                continue

            dep = line.strip().strip('"').strip("',")
            if dep:
                deps.append(dep)

    return deps


def create_project_manifest() -> dict[str, any]:
    """Crée un manifeste de projet."""
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

    print(f"Projet : {manifest['name']}")

    license_info = manifest.get("license", "MIT")
    print(f"License : {license_info}")

    manifest["license"] = "MIT"

    has_scripts = "scripts" in manifest
    print(f"Has scripts : {has_scripts}")

    print("\n📋 Scripts disponibles :")
    for key, value in manifest["scripts"].items():
        print(f"  {key}: {value}")

    return manifest


if __name__ == "__main__":
    import tempfile

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
