# Module 16 — Exercice à trou #2
# 🎯 Thème : Le Makefile
#
# Le Makefile est indispensable pour avoir des "scripts" courts sur ton PC local,
# exactement comme "npm run lint". 
# 
# Si tu tapes `make lint`, ça lance ruff check && mypy.
# Complète ce Makefile classique.

.PHONY: format lint test all

format:
	___ format .  # Quel outil formate le code python ?

lint:
	___ check .   # Quel outil linter le code python ?
	___ .         # Quel outil vérifie les types (Type hints) ?

test:
	___ -v        # Quel outil lance les tests automatiques ?

run:
	# Lancement d'un serveur d'API de dev
	fastapi ___ src/main.py # Quelle commande pour lancer fastapi de manière récursive en dev ?

# La cible 'all' lance format, puis lint, puis test.
___: format lint test
