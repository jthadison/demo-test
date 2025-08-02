"""Position sizing algorithms."""

from enum import Enum
from typing import Dict, Optional
import numpy as np


class SizingMethod(Enum):
    """Position sizing methods."""
    FIXED = "fixed"
    KELLY = "kelly"
    RISK_PARITY = "risk_parity"
    VOLATILITY_BASED = "volatility_based"


class PositionSizer:
    """Calculate optimal position sizes."""
    
    def __init__(
        self,
        method: SizingMethod = SizingMethod.VOLATILITY_BASED,
        max_position_size: float = 0.1,
        risk_per_trade: float = 0.02
    ):
        self.method = method
        self.max_position_size = max_position_size
        self.risk_per_trade = risk_per_trade
    
    def calculate_position_size(
        self,
        account_value: float,
        signal_strength: float,
        volatility: float,
        stop_loss_pct: Optional[float] = None
    ) -> float:
        """Calculate position size based on the selected method."""
        base_size = account_value * self.max_position_size
        
        if self.method == SizingMethod.FIXED:
            return base_size * signal_strength
        
        elif self.method == SizingMethod.VOLATILITY_BASED:
            volatility_scalar = 0.15 / max(volatility, 0.05)
            return base_size * signal_strength * min(volatility_scalar, 1.0)
        
        elif self.method == SizingMethod.KELLY:
            return self._kelly_criterion(
                account_value, signal_strength, volatility
            )
        
        return base_size
    
    def _kelly_criterion(
        self,
        account_value: float,
        win_probability: float,
        avg_win_loss_ratio: float = 1.5
    ) -> float:
        """Calculate position size using Kelly Criterion."""
        if win_probability <= 0 or win_probability >= 1:
            return 0.0
        
        kelly_pct = (win_probability * avg_win_loss_ratio - (1 - win_probability)) / avg_win_loss_ratio
        kelly_pct = max(0, min(kelly_pct, self.max_position_size))
        
        return account_value * kelly_pct