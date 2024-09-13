build: slo_yaml_generator/main.py
	python setup.py sdist bdist_wheel
	pip install .
