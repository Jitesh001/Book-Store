.PHONY: all help run collect deps migrate freeze
FILENAME := .appname
APPNAME := `cat $(FILENAME)`
base ?= src
# target: all - Runs both django and celery if used with -j
all: run

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: run - Runs a dev server on localhost:8000
run:
	manage runserver

# target: deps - install dependencies from requirements file
prod_deps:
	pip install -r requirements.txt
	cd src && pip install -e .
	pip install -e .

dev_deps:
	pip install -U pip setuptools
	pip install -r dev-requirements.txt
	pre-commit install

deps: dev_deps prod_deps


# target: migrate - migrate the database
migrate:
	manage migrate

# target: sh - open django extension's shell plus
sh:
	manage shell

# target: db - open django DB shell
db:
	manage dbshell

startapp:
	manage startapp $(APPNAME)
