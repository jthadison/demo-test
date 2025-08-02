"""Trading System - Professional algorithmic trading platform."""

__version__ = "0.1.0"
__author__ = "Trading System Team"

from trading_system.data import DataProvider
from trading_system.execution import OrderExecutor
from trading_system.monitoring import SystemMonitor
from trading_system.risk import RiskManager
from trading_system.strategies import BaseStrategy

__all__ = [
    "DataProvider",
    "BaseStrategy",
    "RiskManager",
    "OrderExecutor",
    "SystemMonitor",
]
