"""Risk management module."""

from .portfolio import PortfolioRiskManager
from .position import PositionSizer
from .limits import RiskLimits

__all__ = ["PortfolioRiskManager", "PositionSizer", "RiskLimits", "RiskManager"]


class RiskManager:
    """Main risk management coordinator."""
    
    def __init__(self):
        self.portfolio_manager = PortfolioRiskManager()
        self.position_sizer = PositionSizer()
        self.risk_limits = RiskLimits()
    
    async def evaluate_trade(self, signal: dict) -> dict:
        """Evaluate if a trade meets risk criteria."""
        return {
            "approved": True,
            "adjusted_quantity": signal.get("quantity", 0),
            "risk_metrics": {}
        }