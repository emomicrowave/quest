test:
	poetry run pytest --cov=quest --cov-report html

black:
	poetry run black quest

install:
	poetry install

dev:
	poetry shell
