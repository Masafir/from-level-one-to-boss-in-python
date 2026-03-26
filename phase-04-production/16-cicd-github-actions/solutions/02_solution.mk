# Module 16 — Solution exercice à trou #2

.PHONY: format lint test all

format:
	ruff format .

lint:
	ruff check .
	mypy src/

test:
	pytest -v

run:
	fastapi dev src/main.py

all: format lint test
