# Trading System

A professional algorithmic trading system built with Python, featuring real-time data ingestion, strategy development, risk management, and order execution.

## Features

- **Data Ingestion**: Real-time and historical market data collection
- **Strategy Development**: Flexible framework for creating trading strategies
- **Risk Management**: Position sizing, portfolio risk metrics, and trading limits
- **Order Execution**: Smart order routing with multiple broker support
- **Monitoring**: Real-time system metrics and alerting
- **Backtesting**: Comprehensive backtesting framework

## Architecture

```
src/trading_system/
├── data/           # Market data ingestion and storage
├── strategies/     # Trading strategy implementations
├── risk/           # Risk management and position sizing
├── execution/      # Order execution and routing
└── monitoring/     # System monitoring and alerts
```

## Prerequisites

- Python 3.11+
- UV package manager
- Docker and Docker Compose (for services)
- PostgreSQL (for historical data)
- Redis (for real-time data)

## Installation

1. Install UV package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone <repository-url>
cd trading_system
```

3. Install dependencies:
```bash
make dev-install
```

4. Set up environment variables:
```bash
make setup-env
# Edit .env file with your API keys and configuration
```

5. Start services:
```bash
make docker-up
```

## Quick Start

### Running the API Server

```bash
make run-api
```

The API will be available at http://localhost:8000

### Running a Backtest

```bash
make run-backtest
```

### Running Tests

```bash
make test
```

## Development

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Type checking:
```bash
make type-check
```

### Project Structure

- `src/trading_system/`: Main package code
- `tests/`: Unit and integration tests
- `config/`: Configuration files
- `docs/`: Documentation
- `notebooks/`: Jupyter notebooks for research
- `scripts/`: Utility scripts

## Configuration

The system uses environment variables for configuration. See `.env.example` for all available options.

Key configurations:
- `BROKER_ENVIRONMENT`: Set to "paper" for paper trading or "live" for real trading
- `MAX_DAILY_LOSS_PCT`: Maximum daily loss percentage (default: 2%)
- `MAX_POSITION_SIZE_PCT`: Maximum position size as percentage of portfolio (default: 10%)

## API Documentation

When the API server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring

The system includes Prometheus metrics and Grafana dashboards:

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Risk Management

The system implements multiple risk controls:

1. **Position Sizing**: Volatility-based position sizing with Kelly Criterion option
2. **Portfolio Limits**: Maximum position size and concentration limits
3. **Daily Limits**: Maximum daily loss and trade count limits
4. **Order Rate Limiting**: Prevents excessive order submission

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in `/docs`
- Review example strategies in `/notebooks`

## Disclaimer

This software is for educational purposes only. Always test thoroughly with paper trading before using real funds. The authors are not responsible for any financial losses.