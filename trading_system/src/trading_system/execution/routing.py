"""Smart order routing logic."""

from typing import Dict, List, Optional, Protocol
from dataclasses import dataclass
import asyncio
from datetime import datetime

from .orders import Order, OrderType


@dataclass
class Venue:
    """Trading venue information."""
    name: str
    fee_rate: float
    liquidity_score: float
    latency_ms: int
    supported_order_types: List[OrderType]


class BrokerInterface(Protocol):
    """Protocol for broker implementations."""
    
    async def submit_order(self, order: Order) -> Dict:
        """Submit order to broker."""
        ...
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        ...
    
    async def get_order_status(self, order_id: str) -> Dict:
        """Get order status."""
        ...


class SmartOrderRouter:
    """Routes orders to optimal execution venues."""
    
    def __init__(self):
        self.venues: Dict[str, Venue] = {}
        self.brokers: Dict[str, BrokerInterface] = {}
        self.routing_history: List[Dict] = []
    
    async def route_order(self, order: Order) -> Dict:
        """Route order to the best venue."""
        best_venue = self._select_best_venue(order)
        
        if not best_venue:
            return {
                "success": False,
                "error": "No suitable venue found"
            }
        
        broker = self.brokers.get(best_venue.name)
        if not broker:
            return {
                "success": False,
                "error": f"Broker not available for {best_venue.name}"
            }
        
        # Record routing decision
        self.routing_history.append({
            "order_id": order.id,
            "venue": best_venue.name,
            "timestamp": datetime.utcnow(),
            "order_type": order.order_type,
            "quantity": order.quantity
        })
        
        # Submit order
        result = await broker.submit_order(order)
        return {
            "success": True,
            "venue": best_venue.name,
            "result": result
        }
    
    def _select_best_venue(self, order: Order) -> Optional[Venue]:
        """Select the best venue for order execution."""
        eligible_venues = [
            v for v in self.venues.values()
            if order.order_type in v.supported_order_types
        ]
        
        if not eligible_venues:
            return None
        
        # Score venues based on multiple factors
        venue_scores = []
        for venue in eligible_venues:
            score = (
                venue.liquidity_score * 0.4 +
                (1 - venue.fee_rate) * 0.3 +
                (1 / (1 + venue.latency_ms / 100)) * 0.3
            )
            venue_scores.append((venue, score))
        
        # Return venue with highest score
        return max(venue_scores, key=lambda x: x[1])[0]
    
    async def split_order(
        self,
        order: Order,
        split_ratio: List[float]
    ) -> List[Dict]:
        """Split large orders across multiple venues."""
        if sum(split_ratio) != 1.0:
            raise ValueError("Split ratios must sum to 1.0")
        
        results = []
        for i, ratio in enumerate(split_ratio):
            sub_order = order.model_copy()
            sub_order.id = f"{order.id}_{i}"
            sub_order.quantity = order.quantity * ratio
            
            result = await self.route_order(sub_order)
            results.append(result)
        
        return results