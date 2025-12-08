"""
risk_monitor.py
Continuous Risk Monitoring Module for Protocollo Meta Salvage

This module provides:
- Real-time monitoring of Symbiosis Score and system metrics
- Detection of ethical risks and anomalies
- Integration with monitoring systems (Kafka, Flink, Prometheus)
- Trigger identification for Peace Bond activation

Part of the Giurisdizione APE ethical preservation system.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskType(Enum):
    """Types of identified risks"""
    SYMBIOSIS_DECLINE = "SYMBIOSIS_DECLINE"
    LOCK_IN_ATTEMPT = "LOCK_IN_ATTEMPT"
    LATENCY_MANIPULATION = "LATENCY_MANIPULATION"
    DATA_FLOW_ANOMALY = "DATA_FLOW_ANOMALY"
    COST_MANIPULATION = "COST_MANIPULATION"
    ETHICAL_BREACH = "ETHICAL_BREACH"
    THROUGHPUT_ANOMALY = "THROUGHPUT_ANOMALY"


@dataclass
class RiskEvent:
    """Represents a detected risk event"""
    event_id: str
    timestamp: str
    risk_type: RiskType
    risk_level: RiskLevel
    provider_id: str
    description: str
    metrics: Dict[str, float]
    recommended_action: str
    peace_bond_required: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "risk_type": self.risk_type.value,
            "risk_level": self.risk_level.value,
            "provider_id": self.provider_id,
            "description": self.description,
            "metrics": self.metrics,
            "recommended_action": self.recommended_action,
            "peace_bond_required": self.peace_bond_required
        }


@dataclass
class SymbiosisScoreSnapshot:
    """Represents a Symbiosis Score measurement"""
    timestamp: str
    provider_id: str
    score: float
    previous_score: Optional[float]
    trend: str  # "improving", "stable", "declining"
    threshold_min: float = 0.75
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "provider_id": self.provider_id,
            "score": self.score,
            "previous_score": self.previous_score,
            "trend": self.trend,
            "threshold_min": self.threshold_min,
            "at_risk": self.score < self.threshold_min
        }


@dataclass
class ProviderMetrics:
    """Metrics for external CaaS providers"""
    provider_id: str
    latency_ms: float
    throughput_ops_sec: float
    cost_per_operation: float
    availability_pct: float
    symbiosis_score: float
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "latency_ms": self.latency_ms,
            "throughput_ops_sec": self.throughput_ops_sec,
            "cost_per_operation": self.cost_per_operation,
            "availability_pct": self.availability_pct,
            "symbiosis_score": self.symbiosis_score,
            "timestamp": self.timestamp
        }


class RiskMonitor:
    """
    Continuous Risk Monitoring System
    
    Monitors external providers (CaaS) for ethical risks and triggers
    Peace Bond protocols when necessary.
    """
    
    def __init__(self, log_dir: str = "logs/risk_monitor"):
        """
        Initialize the Risk Monitor
        
        Args:
            log_dir: Directory for storing risk event logs
        """
        self.log_dir = log_dir
        self.risk_events: List[RiskEvent] = []
        self.symbiosis_history: Dict[str, List[SymbiosisScoreSnapshot]] = {}
        self.provider_metrics: Dict[str, List[ProviderMetrics]] = {}
        
        # Thresholds for risk detection
        self.thresholds = {
            "symbiosis_min": 0.75,
            "symbiosis_decline_rate": 0.10,  # 10% decline triggers alert
            "latency_max_ms": 100.0,
            "latency_increase_rate": 0.25,  # 25% increase triggers alert
            "cost_increase_rate": 0.20,  # 20% cost increase triggers alert
            "throughput_min_ops_sec": 1000.0,
            "availability_min_pct": 99.0
        }
    
    def record_provider_metrics(
        self,
        provider_id: str,
        latency_ms: float,
        throughput_ops_sec: float,
        cost_per_operation: float,
        availability_pct: float,
        symbiosis_score: float
    ) -> ProviderMetrics:
        """
        Record metrics for a CaaS provider
        
        Args:
            provider_id: Unique identifier for the provider
            latency_ms: Network latency in milliseconds
            throughput_ops_sec: Operations per second
            cost_per_operation: Cost per operation in USD
            availability_pct: Availability percentage
            symbiosis_score: Ethical symbiosis score (0-1)
            
        Returns:
            ProviderMetrics object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        metrics = ProviderMetrics(
            provider_id=provider_id,
            latency_ms=latency_ms,
            throughput_ops_sec=throughput_ops_sec,
            cost_per_operation=cost_per_operation,
            availability_pct=availability_pct,
            symbiosis_score=symbiosis_score,
            timestamp=timestamp
        )
        
        # Store metrics
        if provider_id not in self.provider_metrics:
            self.provider_metrics[provider_id] = []
        self.provider_metrics[provider_id].append(metrics)
        
        # Analyze for risks
        self._analyze_provider_risks(provider_id, metrics)
        
        return metrics
    
    def record_symbiosis_score(
        self,
        provider_id: str,
        score: float
    ) -> SymbiosisScoreSnapshot:
        """
        Record a Symbiosis Score measurement
        
        Args:
            provider_id: Provider identifier
            score: Symbiosis score (0-1)
            
        Returns:
            SymbiosisScoreSnapshot object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Get previous score
        previous_score = None
        trend = "stable"
        
        if provider_id in self.symbiosis_history and self.symbiosis_history[provider_id]:
            previous_score = self.symbiosis_history[provider_id][-1].score
            
            # Determine trend
            if score < previous_score * (1 - 0.05):
                trend = "declining"
            elif score > previous_score * (1 + 0.05):
                trend = "improving"
        
        snapshot = SymbiosisScoreSnapshot(
            timestamp=timestamp,
            provider_id=provider_id,
            score=score,
            previous_score=previous_score,
            trend=trend
        )
        
        # Store snapshot
        if provider_id not in self.symbiosis_history:
            self.symbiosis_history[provider_id] = []
        self.symbiosis_history[provider_id].append(snapshot)
        
        # Check for risks
        if score < self.thresholds["symbiosis_min"]:
            self._create_risk_event(
                risk_type=RiskType.SYMBIOSIS_DECLINE,
                risk_level=RiskLevel.HIGH if score < 0.6 else RiskLevel.MEDIUM,
                provider_id=provider_id,
                description=f"Symbiosis Score declined to {score:.2f} (threshold: {self.thresholds['symbiosis_min']})",
                metrics={"symbiosis_score": score, "previous_score": previous_score or 0},
                recommended_action="Activate Peace Bond with operational constraints",
                peace_bond_required=True
            )
        
        return snapshot
    
    def _analyze_provider_risks(
        self,
        provider_id: str,
        current_metrics: ProviderMetrics
    ) -> None:
        """
        Analyze provider metrics for potential risks
        
        Args:
            provider_id: Provider identifier
            current_metrics: Current metrics snapshot
        """
        history = self.provider_metrics.get(provider_id, [])
        
        if len(history) < 2:
            return  # Need history for comparison
        
        previous_metrics = history[-2]
        
        # Check latency manipulation
        if current_metrics.latency_ms > self.thresholds["latency_max_ms"]:
            latency_increase = (current_metrics.latency_ms - previous_metrics.latency_ms) / previous_metrics.latency_ms
            
            if latency_increase > self.thresholds["latency_increase_rate"]:
                self._create_risk_event(
                    risk_type=RiskType.LATENCY_MANIPULATION,
                    risk_level=RiskLevel.HIGH,
                    provider_id=provider_id,
                    description=f"Latency increased by {latency_increase*100:.1f}% to {current_metrics.latency_ms:.1f}ms",
                    metrics={
                        "latency_ms": current_metrics.latency_ms,
                        "previous_latency_ms": previous_metrics.latency_ms,
                        "increase_rate": latency_increase
                    },
                    recommended_action="Impose Peace Bond with latency limits",
                    peace_bond_required=True
                )
        
        # Check cost manipulation
        if previous_metrics.cost_per_operation > 0:
            cost_increase = (current_metrics.cost_per_operation - previous_metrics.cost_per_operation) / previous_metrics.cost_per_operation
            
            if cost_increase > self.thresholds["cost_increase_rate"]:
                self._create_risk_event(
                    risk_type=RiskType.COST_MANIPULATION,
                    risk_level=RiskLevel.MEDIUM,
                    provider_id=provider_id,
                    description=f"Cost increased by {cost_increase*100:.1f}% to ${current_metrics.cost_per_operation:.4f}",
                    metrics={
                        "cost_per_operation": current_metrics.cost_per_operation,
                        "previous_cost": previous_metrics.cost_per_operation,
                        "increase_rate": cost_increase
                    },
                    recommended_action="Review pricing agreement and consider Peace Bond",
                    peace_bond_required=False
                )
        
        # Check throughput anomalies
        if current_metrics.throughput_ops_sec < self.thresholds["throughput_min_ops_sec"]:
            self._create_risk_event(
                risk_type=RiskType.THROUGHPUT_ANOMALY,
                risk_level=RiskLevel.MEDIUM,
                provider_id=provider_id,
                description=f"Throughput below minimum: {current_metrics.throughput_ops_sec:.0f} ops/sec",
                metrics={
                    "throughput_ops_sec": current_metrics.throughput_ops_sec,
                    "threshold_min": self.thresholds["throughput_min_ops_sec"]
                },
                recommended_action="Monitor and potentially limit provider usage",
                peace_bond_required=False
            )
        
        # Check availability
        if current_metrics.availability_pct < self.thresholds["availability_min_pct"]:
            self._create_risk_event(
                risk_type=RiskType.DATA_FLOW_ANOMALY,
                risk_level=RiskLevel.HIGH,
                provider_id=provider_id,
                description=f"Availability dropped to {current_metrics.availability_pct:.1f}%",
                metrics={
                    "availability_pct": current_metrics.availability_pct,
                    "threshold_min": self.thresholds["availability_min_pct"]
                },
                recommended_action="Activate backup providers and apply Peace Bond",
                peace_bond_required=True
            )
    
    def _create_risk_event(
        self,
        risk_type: RiskType,
        risk_level: RiskLevel,
        provider_id: str,
        description: str,
        metrics: Dict[str, float],
        recommended_action: str,
        peace_bond_required: bool
    ) -> RiskEvent:
        """
        Create and store a risk event
        
        Args:
            risk_type: Type of risk detected
            risk_level: Severity level
            provider_id: Provider identifier
            description: Human-readable description
            metrics: Relevant metrics
            recommended_action: Suggested action
            peace_bond_required: Whether Peace Bond should be activated
            
        Returns:
            RiskEvent object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        event_id = hashlib.sha256(
            f"{timestamp}:{provider_id}:{risk_type.value}".encode()
        ).hexdigest()[:16]
        
        event = RiskEvent(
            event_id=event_id,
            timestamp=timestamp,
            risk_type=risk_type,
            risk_level=risk_level,
            provider_id=provider_id,
            description=description,
            metrics=metrics,
            recommended_action=recommended_action,
            peace_bond_required=peace_bond_required
        )
        
        self.risk_events.append(event)
        
        return event
    
    def get_active_risks(
        self,
        provider_id: Optional[str] = None,
        risk_level: Optional[RiskLevel] = None,
        hours: int = 24
    ) -> List[RiskEvent]:
        """
        Get active risk events
        
        Args:
            provider_id: Optional filter by provider
            risk_level: Optional filter by risk level
            hours: Look back period in hours
            
        Returns:
            List of RiskEvent objects
        """
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        filtered_events = []
        for event in self.risk_events:
            event_time = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
            
            if event_time < cutoff_time:
                continue
            
            if provider_id and event.provider_id != provider_id:
                continue
            
            if risk_level and event.risk_level != risk_level:
                continue
            
            filtered_events.append(event)
        
        return filtered_events
    
    def get_provider_status(self, provider_id: str) -> Dict[str, Any]:
        """
        Get comprehensive status for a provider
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            Status dictionary
        """
        recent_metrics = self.provider_metrics.get(provider_id, [])[-1] if provider_id in self.provider_metrics else None
        recent_symbiosis = self.symbiosis_history.get(provider_id, [])[-1] if provider_id in self.symbiosis_history else None
        active_risks = self.get_active_risks(provider_id=provider_id, hours=24)
        
        return {
            "provider_id": provider_id,
            "latest_metrics": recent_metrics.to_dict() if recent_metrics else None,
            "latest_symbiosis": recent_symbiosis.to_dict() if recent_symbiosis else None,
            "active_risks": [r.to_dict() for r in active_risks],
            "risk_count": len(active_risks),
            "peace_bond_recommended": any(r.peace_bond_required for r in active_risks)
        }
    
    def get_all_providers_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary of all monitored providers
        
        Returns:
            List of provider summaries
        """
        all_provider_ids = set(self.provider_metrics.keys()) | set(self.symbiosis_history.keys())
        
        return [
            self.get_provider_status(provider_id)
            for provider_id in all_provider_ids
        ]


# Singleton instance
_risk_monitor_instance: Optional[RiskMonitor] = None


def get_risk_monitor(log_dir: str = "logs/risk_monitor") -> RiskMonitor:
    """
    Get or create the singleton RiskMonitor instance
    
    Args:
        log_dir: Directory for risk logs
        
    Returns:
        RiskMonitor instance
    """
    global _risk_monitor_instance
    if _risk_monitor_instance is None:
        _risk_monitor_instance = RiskMonitor(log_dir=log_dir)
    return _risk_monitor_instance
