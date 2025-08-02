"""Performance metrics collection."""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class MetricPoint:
    """Single metric data point."""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collects and aggregates system metrics."""

    def __init__(self, retention_hours: int = 24):
        self.metrics: dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.retention_hours = retention_hours
        self.start_time = time.time()
        self._collection_task: asyncio.Task | None = None

    async def start(self) -> None:
        """Start metrics collection."""
        self._collection_task = asyncio.create_task(self._collect_loop())

    async def stop(self) -> None:
        """Stop metrics collection."""
        if self._collection_task:
            self._collection_task.cancel()
            await asyncio.gather(self._collection_task, return_exceptions=True)

    def record_metric(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None
    ) -> None:
        """Record a metric value."""
        metric = MetricPoint(name, value, tags=tags or {})
        self.metrics[name].append(metric)

    def get_metric_stats(
        self,
        name: str,
        duration: timedelta | None = None
    ) -> dict[str, float]:
        """Get statistics for a metric over a time period."""
        if name not in self.metrics or not self.metrics[name]:
            return {}

        now = datetime.utcnow()
        if duration:
            cutoff = now - duration
            values = [
                m.value for m in self.metrics[name]
                if m.timestamp >= cutoff
            ]
        else:
            values = [m.value for m in self.metrics[name]]

        if not values:
            return {}

        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1]
        }

    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        return time.time() - self.start_time

    async def _collect_loop(self) -> None:
        """Background loop for collecting system metrics."""
        while True:
            try:
                # Collect system metrics
                self.record_metric("system.cpu_percent", self._get_cpu_usage())
                self.record_metric("system.memory_mb", self._get_memory_usage())

                # Clean old metrics
                self._clean_old_metrics()

                await asyncio.sleep(60)  # Collect every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in metrics collection: {e}")

    def _get_cpu_usage(self) -> float:
        """Get CPU usage percentage."""
        # Placeholder - would use psutil in production
        return 25.0

    def _get_memory_usage(self) -> float:
        """Get memory usage in MB."""
        # Placeholder - would use psutil in production
        return 512.0

    def _clean_old_metrics(self) -> None:
        """Remove metrics older than retention period."""
        cutoff = datetime.utcnow() - timedelta(hours=self.retention_hours)

        for metric_name in list(self.metrics.keys()):
            # Remove old entries
            while self.metrics[metric_name] and self.metrics[metric_name][0].timestamp < cutoff:
                self.metrics[metric_name].popleft()

            # Remove empty metrics
            if not self.metrics[metric_name]:
                del self.metrics[metric_name]
