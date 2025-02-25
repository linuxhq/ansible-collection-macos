# Makefile

all: venv python galaxy

clean:
	$(RM) -r venv

galaxy:
	venv/bin/ansible-galaxy install -r requirements.yml

python:
	venv/bin/python3 -m pip install --upgrade pip
	PYTHONWARNINGS='ignore:DEPRECATION' venv/bin/pip install -r requirements.txt

venv:
	test -d venv || python3 -m venv venv
