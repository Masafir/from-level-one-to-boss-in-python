"""
Module 06 — Exercice à trou #1
🎯 Thème : Imports et système de modules

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

# ============================================================
# PARTIE 1 : Différents types d'import
# ============================================================

# Import du module entier
___ json  # Quel mot-clé pour importer ?

# Import spécifique
___ pathlib ___ Path  # Comme : const { Path } = require('pathlib')

# Import avec alias
import collections ___ col  # Quel mot-clé pour l'alias ?

# ============================================================
# PARTIE 2 : Simuler un système de packages
# ============================================================

# On va créer un mini système de packages en mémoire pour comprendre
# comment Python résout les imports

import sys
import types
from dataclasses import dataclass, field

@dataclass
class ModuleInfo:
    name: str
    path: str
    exports: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


def analyze_imports(source_code: str) -> dict:
    """
    Analyse un code source et extrait les imports.
    
    Retourne un dict avec :
    - 'standard_imports': modules de la lib standard
    - 'from_imports': dict {module: [noms importés]}
    - 'aliased_imports': dict {alias: module_original}
    """
    standard_imports = []
    from_imports = {}
    aliased_imports = {}
    
    for line in source_code.strip().___("\n"):  # Quelle méthode pour split par ligne ?
        line = line.strip()
        
        if line.startswith("import ") and " as " not in line:
            # Import simple : "import json"
            module = line.replace("import ", "").strip()
            standard_imports.___(module)  # Ajouter à la liste
        
        elif line.startswith("import ") and " as " in line:
            # Import aliasé : "import numpy as np"
            parts = line.replace("import ", "").split(" as ")
            aliased_imports[parts[1].strip()] = parts[0].___()  # Nettoyer les espaces
        
        elif line.startswith("from "):
            # From import : "from json import loads, dumps"
            parts = line.replace("from ", "").split(" import ")
            module = parts[0].strip()
            names = [n.strip() for n in parts[1].split(",")]
            from_imports[module] = ___  # Quelle valeur ?
    
    return {
        "standard_imports": standard_imports,
        "from_imports": from_imports,
        "aliased_imports": aliased_imports,
    }


# Test
sample_code = """
import json
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter
from game_engine.models import Player, Enemy
from game_engine.services import CombatService
"""

result = analyze_imports(sample_code)
print("📦 Analyse des imports :")
print(f"  Standard: {result['standard_imports']}")
print(f"  From: {result['from_imports']}")
print(f"  Aliased: {result['aliased_imports']}")


# ============================================================
# PARTIE 3 : Résolution de dépendances
# ============================================================

def build_dependency_graph(modules: dict[str, list[str]]) -> dict[str, set[str]]:
    """
    Construit un graphe de dépendances à partir d'un dict
    {module_name: [dependencies]}.
    
    Retourne toutes les dépendances (directes ET transitives).
    """
    def get_all_deps(module: str, visited: set[str] | None = None) -> set[str]:
        if visited is ___:  # Quel opérateur pour comparer à None ?
            visited = set()
        
        if module ___ visited:  # Quel opérateur pour "est dans" ?
            return set()  # Éviter les cycles
        
        visited.add(module)
        direct_deps = set(modules.get(module, []))
        all_deps = direct_deps.copy()
        
        for dep in direct_deps:
            # Récursion pour les dépendances transitives
            transitive = get_all_deps(dep, visited)
            all_deps.___(transitive)  # Quelle méthode de set pour ajouter plusieurs ?
        
        return all_deps
    
    return {mod: get_all_deps(mod) for mod in modules}


# Test
project_modules = {
    "api.routes": ["services.combat", "models.player"],
    "services.combat": ["models.player", "models.item", "utils.dice"],
    "services.inventory": ["models.item", "utils.validation"],
    "models.player": ["models.item"],
    "models.item": [],
    "utils.dice": [],
    "utils.validation": [],
}

graph = build_dependency_graph(project_modules)
print("\n🔗 Dépendances transitives :")
for module, deps in sorted(graph.items()):
    print(f"  {module} → {sorted(deps)}")


# ============================================================
# PARTIE 4 : __all__ et exports
# ============================================================

def get_public_api(module_dict: dict) -> list[str]:
    """
    Simule ce que fait __all__ : retourne les noms "publics" d'un module.
    Convention : les noms commençant par _ sont privés.
    """
    if "___" in module_dict:  # Quel attribut spécial contrôle les exports ?
        return module_dict["__all__"]
    
    # Sans __all__, tout ce qui ne commence pas par _ est public
    return [name for name in module_dict if not name.startswith("___")]


# Simuler un module
fake_module = {
    "__all__": ["Player", "create_player"],
    "Player": "class",
    "create_player": "function",
    "_internal_helper": "function",
    "__version__": "1.0.0",
    "SECRET_KEY": "should-not-be-exported",
}

public = get_public_api(fake_module)
print(f"\n📤 API publique : {public}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
