
lint:
	flake8 --show-source lexrank tests
	isort --check-only -rc lexrank tests --diff

test:
	pytest tests

install-dev:
	pip install -U -r requirements/dev.txt

install-ci:
	pip install -U -r requirements/ci.txt
