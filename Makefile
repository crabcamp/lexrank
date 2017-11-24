
lint:
	flake8 --show-source lexrank
	isort --check-only -rc lexrank --diff

test:
	pytest tests

install-dev:
	pip install -U -r requirements/dev.txt

install-ci:
	pip install -U -r requirements/ci.txt
