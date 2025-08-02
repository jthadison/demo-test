"""Data ingestion and management module."""

from typing import Protocol, Any
from datetime import datetime
import pandas as pd


class DataProvider(Protocol):
    """Protocol for data providers."""
    
    async def fetch_historical(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = "1d"
    ) -> pd.DataFrame:
        """Fetch historical market data."""
        ...
    
    async def stream_realtime(
        self,
        symbols: list[str],
        callback: Any
    ) -> None:
        """Stream real-time market data."""
        ...