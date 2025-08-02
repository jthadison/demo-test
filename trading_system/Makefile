.PHONY: help install dev-install test lint format type-check clean run-api run-backtest docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code"
	@echo "  make type-check    - Run type checking"
	@echo "  make clean         - Clean cache files"
	@echo "  make run-api       - Run the API server"
	@echo "  make run-backtest  - Run backtesting"
	@echo "  make docker-up     - Start Docker services"
	@echo "  make docker-down   - Stop Docker services"

install:
	uv pip sync

dev-install:
	uv pip install -e ".[dev]"
	uv run pre-commit install

test:
	uv run pytest tests/ -v --cov=trading_system --cov-report=term-missing

test-unit:
	uv run pytest tests/unit/ -v

test-integration:
	uv run pytest tests/integration/ -v

lint:
	uv run ruff check src/ tests/
	uv run black --check src/ tests/

format:
	uv run ruff check --fix src/ tests/
	uv run black src/ tests/

type-check:
	uv run mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

run-api:
	uv run uvicorn trading_system.api.main:app --reload --host 0.0.0.0 --port 8000

run-backtest:
	uv run python -m trading_system.backtest

run-monitor:
	uv run python -m trading_system.monitoring.dashboard

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development database commands
db-migrate:
	uv run alembic upgrade head

db-rollback:
	uv run alembic downgrade -1

db-reset:
	uv run alembic downgrade base
	uv run alembic upgrade head

# Pre-commit hooks
pre-commit:
	uv run pre-commit run --all-files

# Build commands
build:
	uv build

# Environment setup
setup-env:
	cp .env.example .env
	@echo "Environment file created. Please update .env with your credentials."