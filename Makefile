.PHONY: env install install-dev clean dev-server server test capybara

NO_COLOUR=\x1b[0m
TARGET_COLOUR=\x1b[96m

help:
	@echo "\nCravelist Server"
	@echo "======================================================"
	@echo "$(TARGET_COLOUR)env$(NO_COLOUR) \t\t\t create python virtualenv"
	@echo "$(TARGET_COLOUR)clean$(NO_COLOUR) \t\t\t clean up .pyc files"
	@echo "$(TARGET_COLOUR)install$(NO_COLOUR) \t\t install app dependencies"
	@echo "$(TARGET_COLOUR)install-dev$(NO_COLOUR) \t\t install app dev dependencies"
	@echo "$(TARGET_COLOUR)dev-server$(NO_COLOUR) \t\t start dev server"
	@echo "$(TARGET_COLOUR)server$(NO_COLOUR) \t\t\t start gunicorn server"
	@echo "$(TARGET_COLOUR)test$(NO_COLOUR) \t\t\t run unit and component tests\n"

env:
	test -d venv || virtualenv venv -p python3

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete

install:
	pip install -Ur requirements.txt

install-dev:
	pip install -Ur requirements-dev.txt

dev-server:
	python run_debug.py

server:
	/gunicorn.sh

test:
	python -m nose -s --verbosity=3

test-user:
	python -m nose -s --verbosity=3 tests/models/test_user_model.py
