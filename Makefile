PHONY: lint reformat test


lint:
	black --check app
	pylint app
	flake8 --statistics --show-source --count app
	bandit -r app

reformat:
	black app

test:
	python -m pytest --cov -vv