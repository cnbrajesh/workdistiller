.PHONY: install dev test lint api watch

install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check .

api:
	uvicorn api.main:app --reload

watch:
	python scripts/watch_capture_folder.py
