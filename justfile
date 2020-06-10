test:
	coverage run -m pytest
	coverage html

black:
	black **.py
