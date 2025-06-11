.PHONY: lint mypy test

all: lint mypy test

lint:
	uv run ruff format pybdl/ tests/ \
	&& uv run ruff check --fix --show-fixes pybdl/ tests/ \
	&& uv run bandit -c pyproject.toml -r pybdl/

mypy:
	uv run mypy pybdl/ tests/

test:
	uv run pytest --cov --cov-report term-missing:skip-covered
