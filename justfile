test:
	pytest --cov=kobold --cov-report html

black:
	black **.py
