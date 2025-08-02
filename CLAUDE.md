# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Trading System

A professional algorithmic trading system built with Python 3.11+, using UV for package management.

## Key Commands

### Development Setup
```bash
# Install UV first: curl -LsSf https://astral.sh/uv/install.sh | sh
make dev-install    # Install all dependencies including dev tools
make setup-env      # Create .env from template
make docker-up      # Start PostgreSQL and Redis services
```

### Common Development Tasks
```bash
make test           # Run all tests with coverage
make lint           # Run ruff linting
make format         # Format code with black and ruff
make type-check     # Run mypy type checking
make run-api        # Start FastAPI server on port 8000
```

### Before Committing
```bash
make pre-commit     # Run all pre-commit hooks
make test           # Ensure all tests pass
```

## Architecture Overview

The system follows a modular architecture with clear separation of concerns:

1. **Data Layer** (`src/trading_system/data/`)
   - Providers: Integration with market data sources (Alpaca, Polygon, etc.)
   - Collectors: Real-time and historical data collection
   - Storage: PostgreSQL for historical, Redis for real-time

2. **Strategy Layer** (`src/trading_system/strategies/`)
   - BaseStrategy: Abstract base class all strategies inherit from
   - Indicators: Technical analysis indicators
   - Strategy: Wyckoffy Strategy with volume profile, order flow and smart money concepts ( order blocks, imbalances, liquidity pools, stop hunts, break of structure, change of character)
   - Signals: Signal generation logic
   - Backtest: Backtesting framework

3. **Risk Management** (`src/trading_system/risk/`)
   - Portfolio: Portfolio-wide risk metrics (VaR, Sharpe)
   - Position: Position sizing algorithms (Kelly, volatility-based)
   - Limits: Hard limits and controls

4. **Execution Layer** (`src/trading_system/execution/`)
   - Orders: Order models and management
   - Routing: Smart order routing across venues
   - Brokers: Broker-specific implementations

5. **Monitoring** (`src/trading_system/monitoring/`)
   - Metrics: System performance metrics
   - Alerts: Alert rules and notifications
   - Dashboard: Web-based monitoring interface

## Key Design Patterns

- **Protocol Classes**: Used for defining interfaces (e.g., DataProvider, BrokerInterface)
- **Pydantic Models**: For data validation and serialization
- **Async/Await**: Throughout for concurrent operations
- **Dependency Injection**: Via FastAPI for the API layer

## Testing Strategy

- Unit tests in `tests/unit/` for isolated component testing
- Integration tests in `tests/integration/` for end-to-end flows
- Fixtures in `tests/fixtures/` for shared test data
- Minimum 80% code coverage target

## Configuration

- Environment variables via `.env` file
- Pydantic Settings for type-safe configuration
- Separate configs for dev/staging/production

## Important Notes

- Always use UV commands (not pip directly)
- Type hints are mandatory - run mypy before committing
- Follow existing code patterns in each module
- Risk controls are critical - never bypass them
- All monetary values in USD cents to avoid float precision issues