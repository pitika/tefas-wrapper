clean:
	# build
	rm -rf build/
	rm -rf dist/
	rm -rf tefas_wrapper.egg-info/
	rm -rf .eggs/
	# pyc
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*