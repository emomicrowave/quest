test:
	pytest --cov=quest --cov-report html

black:
	black **.py

install:
	pipx install --force .

dev:
	poetry shell
