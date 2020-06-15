test:
	pytest --cov=quest --cov-report html

black:
	black **.py
