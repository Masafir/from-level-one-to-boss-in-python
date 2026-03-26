"""
Module 01 — Exercice à trou #1
🎯 Thème : Setup d'un projet Python

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

# ============================================================
# PARTIE 1 : Imports et modules de la bibliothèque standard
# ============================================================

# En Python, on importe des modules avec le mot-clé 'import'
# Équivalent Node : const os = require('os') ou import os from 'os'

import ___  # Importe le module pour interagir avec l'OS
import ___  # Importe le module pour manipuler les chemins de fichiers
from datetime import ___  # Importe la classe datetime

# ============================================================
# PARTIE 2 : Variables et f-strings
# ============================================================

# Python utilise les f-strings (comme les template literals en JS)
# JS  : `Hello ${name}`
# Py  : f"Hello {name}"

project_name = "game-score-tracker"
python_version = "3.12"

# Complète le f-string pour afficher "Projet: game-score-tracker (Python 3.12)"
message = f"Projet: {___} (Python {___})"
print(message)

# ============================================================
# PARTIE 3 : Travailler avec les chemins (pathlib)
# ============================================================

# En Python moderne, on utilise pathlib (pas os.path)
# C'est comme path.join() en Node, mais en mieux

from ___ import Path  # Importe Path depuis le bon module

# Crée un chemin vers le dossier du projet
project_dir = Path(___).parent  # __file__ = chemin du script actuel

# Affiche le dossier parent du script
print(f"Dossier du projet : {project_dir}")

# Crée un chemin vers un fichier (sans le créer)
# Utilise l'opérateur / pour joindre les chemins (spécifique à pathlib !)
config_path = project_dir / "___" / "config.toml"
print(f"Chemin config : {config_path}")

# ============================================================
# PARTIE 4 : Vérifier l'environnement
# ============================================================

# sys.prefix pointe vers le venv actif (ou l'installation globale)
import ___

def check_venv() -> ___:  # Type hint : cette fonction retourne un booléen
    """Vérifie si on est dans un environnement virtuel."""
    # sys.prefix != sys.base_prefix quand un venv est actif
    return sys.___ != sys.___

is_in_venv = check_venv()
status = "✅ venv actif" if is_in_venv else "⚠️ PAS de venv !"
print(f"Environnement : {status}")

# ============================================================
# PARTIE 5 : Lire un fichier (context manager)
# ============================================================

# En Python, on utilise 'with' pour ouvrir des fichiers
# C'est comme un try/finally automatique qui ferme le fichier
# Équivalent Node : fs.readFileSync() mais en mieux géré

# On va créer un petit fichier de config puis le relire
config_content = """[game]
name = "Space Invaders"
max_score = 999999
"""

# Écrire le fichier
config_file = project_dir / "test_config.toml"
___ config_file.open("w") as f:  # Quel mot-clé pour le context manager ?
    f.write(config_content)

# Relire le fichier
___ config_file.open("r") as f:  # Même mot-clé !
    content = f.___()  # Quelle méthode pour lire tout le contenu ?
    print(f"\nContenu du fichier :\n{content}")

# Nettoyer : supprimer le fichier test
config_file.___(missing_ok=True)  # Quelle méthode de Path pour supprimer ?

# ============================================================
# PARTIE 6 : Le point d'entrée
# ============================================================

# En Python, le fameux "if __name__" c'est comme vérifier
# si le fichier est exécuté directement (pas importé)
# Équivalent : if (require.main === module) en Node

if ___:
    print("\n🎮 Script exécuté directement !")
    print(f"Timestamp : {datetime.now()}")
    print("Setup terminé avec succès ! ✅")
