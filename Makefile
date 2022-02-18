run:
	python -m unittest

uninstall:
	pip uninstall -y -r <(pip freeze)
