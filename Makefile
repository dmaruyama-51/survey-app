POETRY = $(shell which poetry)
POETRY_OPTION = --no-interaction --no-ansi
POETRY_RUN = ${POETRY} run ${POETRY_OPTION}

MYPY_OPTIONS = --install-types --non-interactive --ignore-missing-imports

test: 
	${POETRY_RUN} pytest tests/
lint: 
	${POETRY_RUN} mypy ${MYPY_OPTIONS} -p src -p tests
	${POETRY_RUN} uff check . --extend-select I --fix
format: 
	${POETRY_RUN} ruff format .

dev:
	${POETRY_RUN} streamlit run src/app.py

all: test lint format

.PHONY: test lint format all dev