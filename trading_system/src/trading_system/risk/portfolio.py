"""Portfolio risk management."""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class PortfolioMetrics:
    """Portfolio risk metrics."""
    total_value: float
    var_95: float  # Value at Risk
    sharpe_ratio: float
    max_drawdown: float
    beta: float
    correlation_matrix: Optional[pd.DataFrame] = None


class PortfolioRiskManager:
    """Manages portfolio-level risk metrics."""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.positions: Dict[str, float] = {}
        self.historical_returns: Optional[pd.DataFrame] = None
    
    def calculate_portfolio_var(
        self,
        confidence_level: float = 0.95,
        time_horizon: int = 1
    ) -> float:
        """Calculate Value at Risk for the portfolio."""
        if self.historical_returns is None:
            return 0.0
        
        portfolio_returns = self._calculate_portfolio_returns()
        var_percentile = (1 - confidence_level) * 100
        return np.percentile(portfolio_returns, var_percentile) * np.sqrt(time_horizon)
    
    def calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio of the portfolio."""
        if self.historical_returns is None:
            return 0.0
        
        portfolio_returns = self._calculate_portfolio_returns()
        excess_returns = portfolio_returns - self.risk_free_rate / 252
        
        if portfolio_returns.std() == 0:
            return 0.0
        
        return np.sqrt(252) * excess_returns.mean() / portfolio_returns.std()
    
    def _calculate_portfolio_returns(self) -> pd.Series:
        """Calculate portfolio returns based on positions."""
        weights = pd.Series(self.positions)
        weights = weights / weights.sum()
        return (self.historical_returns * weights).sum(axis=1)