"""
Module 01 — Solution exercice à trou #1
"""

import os
import sys
from datetime import datetime
from pathlib import Path

project_name = "game-score-tracker"
python_version = "3.12"

message = f"Projet: {project_name} (Python {python_version})"
print(message)

project_dir = Path(__file__).parent

print(f"Dossier du projet : {project_dir}")

config_path = project_dir / "src" / "config.toml"
print(f"Chemin config : {config_path}")

import sys

def check_venv() -> bool:
    """Vérifie si on est dans un environnement virtuel."""
    return sys.prefix != sys.base_prefix

is_in_venv = check_venv()
status = "✅ venv actif" if is_in_venv else "⚠️ PAS de venv !"
print(f"Environnement : {status}")

config_content = """[game]
name = "Space Invaders"
max_score = 999999
"""

config_file = project_dir / "test_config.toml"
with config_file.open("w") as f:
    f.write(config_content)

with config_file.open("r") as f:
    content = f.read()
    print(f"\nContenu du fichier :\n{content}")

config_file.unlink(missing_ok=True)

if __name__ == "__main__":
    print("\n🎮 Script exécuté directement !")
    print(f"Timestamp : {datetime.now()}")
    print("Setup terminé avec succès ! ✅")
