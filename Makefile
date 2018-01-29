.PHONY: init

init:
	pip install .[test]
	
test: init
	python setup.py test
