SHELL := /bin/bash

.PHONY: help run dash test lint docker

help:
	@echo "Targets:"
	@echo "  run    - Start Flask API on http://localhost:5050"
	@echo "  dash   - Start Streamlit dashboard on http://localhost:8501"
	@echo "  test   - Run pytest tests"
	@echo "  lint   - Run flake8 on apps"
	@echo "  docker - Build Docker image (mindhack-labs)"

run:
	python app.py

dash:
	streamlit run dashboard_app.py

test:
	pytest -q

lint:
	flake8 apps

docker:
	docker build -t mindhack-labs .


seed:
	python seed_db.py

reset-db:
	python -c "from apps.db import reset_db; reset_db(); print('DB reset')"
