"""Alert management system."""

from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
from dataclasses import dataclass, field
import logging


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    """Alert status."""
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


@dataclass
class Alert:
    """Alert data model."""
    id: str
    name: str
    message: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.ACTIVE
    timestamp: datetime = field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def acknowledge(self) -> None:
        """Acknowledge the alert."""
        self.status = AlertStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.utcnow()
    
    def resolve(self) -> None:
        """Resolve the alert."""
        self.status = AlertStatus.RESOLVED
        self.resolved_at = datetime.utcnow()


class AlertManager:
    """Manages system alerts and notifications."""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: List[AlertRule] = []
        self.notification_handlers: List[Callable] = []
        self._monitoring_task: Optional[asyncio.Task] = None
        self.logger = logging.getLogger(__name__)
    
    async def start(self) -> None:
        """Start alert monitoring."""
        self._monitoring_task = asyncio.create_task(self._monitor_loop())
        self._setup_default_rules()
    
    async def stop(self) -> None:
        """Stop alert monitoring."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            await asyncio.gather(self._monitoring_task, return_exceptions=True)
    
    def create_alert(
        self,
        name: str,
        message: str,
        severity: AlertSeverity,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """Create a new alert."""
        alert_id = f"{name}_{datetime.utcnow().timestamp()}"
        alert = Alert(
            id=alert_id,
            name=name,
            message=message,
            severity=severity,
            metadata=metadata or {}
        )
        
        self.alerts[alert_id] = alert
        self._notify_handlers(alert)
        
        return alert
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        return [
            alert for alert in self.alerts.values()
            if alert.status == AlertStatus.ACTIVE
        ]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledge()
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        if alert_id in self.alerts:
            self.alerts[alert_id].resolve()
            return True
        return False
    
    def add_notification_handler(self, handler: Callable[[Alert], None]) -> None:
        """Add a notification handler."""
        self.notification_handlers.append(handler)
    
    def _notify_handlers(self, alert: Alert) -> None:
        """Notify all handlers of an alert."""
        for handler in self.notification_handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.error(f"Error in notification handler: {e}")
    
    def _setup_default_rules(self) -> None:
        """Set up default alert rules."""
        # Example rules
        self.alert_rules.extend([
            AlertRule(
                name="high_latency",
                condition=lambda m: m.get("order_latency_ms", 0) > 1000,
                message="Order execution latency is high",
                severity=AlertSeverity.WARNING
            ),
            AlertRule(
                name="connection_lost",
                condition=lambda m: not m.get("broker_connected", True),
                message="Lost connection to broker",
                severity=AlertSeverity.CRITICAL
            )
        ])
    
    async def _monitor_loop(self) -> None:
        """Background monitoring loop."""
        while True:
            try:
                # Check alert rules
                # In production, this would check actual metrics
                
                # Auto-resolve old acknowledged alerts
                self._auto_resolve_old_alerts()
                
                await asyncio.sleep(30)  # Check every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in alert monitoring: {e}")
    
    def _auto_resolve_old_alerts(self) -> None:
        """Auto-resolve old acknowledged alerts."""
        cutoff = datetime.utcnow() - timedelta(hours=24)
        
        for alert in list(self.alerts.values()):
            if (alert.status == AlertStatus.ACKNOWLEDGED and
                alert.acknowledged_at and
                alert.acknowledged_at < cutoff):
                alert.resolve()


@dataclass
class AlertRule:
    """Alert rule definition."""
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    message: str
    severity: AlertSeverity
    cooldown_minutes: int = 5