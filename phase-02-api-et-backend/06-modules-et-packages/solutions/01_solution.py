"""Module 06 — Solution exercice à trou #1"""

import json
from pathlib import Path
import collections as col


def analyze_imports(source_code: str) -> dict:
    standard_imports = []
    from_imports = {}
    aliased_imports = {}

    for line in source_code.strip().split("\n"):
        line = line.strip()
        if line.startswith("import ") and " as " not in line:
            module = line.replace("import ", "").strip()
            standard_imports.append(module)
        elif line.startswith("import ") and " as " in line:
            parts = line.replace("import ", "").split(" as ")
            aliased_imports[parts[1].strip()] = parts[0].strip()
        elif line.startswith("from "):
            parts = line.replace("from ", "").split(" import ")
            module = parts[0].strip()
            names = [n.strip() for n in parts[1].split(",")]
            from_imports[module] = names

    return {
        "standard_imports": standard_imports,
        "from_imports": from_imports,
        "aliased_imports": aliased_imports,
    }


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


def build_dependency_graph(modules: dict[str, list[str]]) -> dict[str, set[str]]:
    def get_all_deps(module: str, visited: set[str] | None = None) -> set[str]:
        if visited is None:
            visited = set()
        if module in visited:
            return set()
        visited.add(module)
        direct_deps = set(modules.get(module, []))
        all_deps = direct_deps.copy()
        for dep in direct_deps:
            transitive = get_all_deps(dep, visited)
            all_deps.update(transitive)
        return all_deps

    return {mod: get_all_deps(mod) for mod in modules}


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


def get_public_api(module_dict: dict) -> list[str]:
    if "__all__" in module_dict:
        return module_dict["__all__"]
    return [name for name in module_dict if not name.startswith("_")]


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

print("\n✅ Exercice terminé avec succès !")
