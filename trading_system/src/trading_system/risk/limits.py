"""Risk limits and controls."""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TradingLimits:
    """Trading risk limits configuration."""
    max_daily_loss: float = 0.02  # 2% of portfolio
    max_position_size: float = 0.1  # 10% of portfolio
    max_leverage: float = 1.0
    max_orders_per_minute: int = 10
    max_daily_trades: int = 100
    concentration_limit: float = 0.25  # Max 25% in single asset


class RiskLimits:
    """Enforce risk limits and trading controls."""

    def __init__(self, limits: TradingLimits | None = None):
        self.limits = limits or TradingLimits()
        self.daily_loss = 0.0
        self.daily_trades = 0
        self.last_reset = datetime.now()
        self.order_timestamps: list[datetime] = []

    def check_trade_allowed(
        self,
        trade_value: float,
        portfolio_value: float,
        symbol: str,
        current_positions: dict[str, float]
    ) -> tuple[bool, str | None]:
        """Check if a trade is allowed under current limits."""
        self._reset_daily_counters_if_needed()

        # Check daily loss limit
        if abs(self.daily_loss) >= self.limits.max_daily_loss * portfolio_value:
            return False, "Daily loss limit reached"

        # Check position size limit
        position_pct = trade_value / portfolio_value
        if position_pct > self.limits.max_position_size:
            return False, f"Position size {position_pct:.1%} exceeds limit"

        # Check concentration limit
        symbol_exposure = current_positions.get(symbol, 0) + trade_value
        if abs(symbol_exposure) / portfolio_value > self.limits.concentration_limit:
            return False, f"Concentration limit exceeded for {symbol}"

        # Check rate limiting
        now = datetime.now()
        recent_orders = [
            ts for ts in self.order_timestamps
            if now - ts < timedelta(minutes=1)
        ]
        if len(recent_orders) >= self.limits.max_orders_per_minute:
            return False, "Order rate limit exceeded"

        # Check daily trade limit
        if self.daily_trades >= self.limits.max_daily_trades:
            return False, "Daily trade limit reached"

        return True, None

    def record_trade(self, pnl: float) -> None:
        """Record a completed trade."""
        self.daily_loss += pnl
        self.daily_trades += 1
        self.order_timestamps.append(datetime.now())

    def _reset_daily_counters_if_needed(self) -> None:
        """Reset daily counters at market open."""
        now = datetime.now()
        if now.date() > self.last_reset.date():
            self.daily_loss = 0.0
            self.daily_trades = 0
            self.last_reset = now
            self.order_timestamps = []
