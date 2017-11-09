venv_dir=/home/ben/Dropbox/workspace/virtualenvs/mathvis
pyvenv=python3

run:
	python3 mathvis/window.py

freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

test:
	PYTHONPATH=./mathvis python3 -m pytest

