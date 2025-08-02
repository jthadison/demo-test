"""Order execution module."""

from .orders import Order, OrderStatus, OrderType
from .routing import SmartOrderRouter

__all__ = ["Order", "OrderType", "OrderStatus", "SmartOrderRouter", "OrderExecutor"]


class OrderExecutor:
    """Main order execution coordinator."""

    def __init__(self) -> None:
        self.router = SmartOrderRouter()
        self.active_orders: dict = {}

    async def execute_order(self, order: Order) -> dict:
        """Execute an order through the appropriate broker."""
        return {
            "order_id": order.id,
            "status": "submitted",
            "timestamp": order.timestamp
        }
