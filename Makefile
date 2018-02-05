.PHONY: init

init:
	pip install .[test]

test:
	python setup.py test

