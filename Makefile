venv_dir=/home/ben/Dropbox/workspace/virtualenvs/mathvis
pyvenv=python3

run:
	python3 mathvis/window.py

complex:
	python3 mathvis/cfractions.py

freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

