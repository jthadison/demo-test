"""Base strategy class for all trading strategies."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field


class Signal(BaseModel):
    """Trading signal model."""
    symbol: str
    action: str = Field(..., pattern="^(BUY|SELL|HOLD)$")
    quantity: float
    price: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseStrategy(ABC):
    """Abstract base class for trading strategies."""
    
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
        self._is_initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize strategy with historical data."""
        pass
    
    @abstractmethod
    async def analyze(self, data: pd.DataFrame) -> List[Signal]:
        """Analyze market data and generate signals."""
        pass
    
    @abstractmethod
    async def on_tick(self, tick_data: Dict[str, Any]) -> Optional[Signal]:
        """Process real-time tick data."""
        pass
    
    def validate_parameters(self) -> bool:
        """Validate strategy parameters."""
        return True