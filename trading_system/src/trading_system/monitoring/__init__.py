"""System monitoring and alerting module."""

from .alerts import AlertManager
from .metrics import MetricsCollector

__all__ = ["MetricsCollector", "AlertManager", "SystemMonitor"]


class SystemMonitor:
    """Main system monitoring coordinator."""

    def __init__(self) -> None:
        self.metrics = MetricsCollector()
        self.alerts = AlertManager()

    async def start_monitoring(self) -> None:
        """Start system monitoring."""
        await self.metrics.start()
        await self.alerts.start()

    async def get_system_health(self) -> dict:
        """Get current system health status."""
        return {
            "status": "healthy",
            "uptime": self.metrics.get_uptime(),
            "active_alerts": self.alerts.get_active_alerts()
        }
