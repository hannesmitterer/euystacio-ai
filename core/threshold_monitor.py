"""
threshold_monitor.py
Real-Time Threshold Monitoring Module for Euystacio AI

This module provides:
- Automated alerts and logging for QEK and H-VAR metric deviations
- Machine learning-based drift prediction to anticipate anomalies
- Ethisches Ideal limits tracking and enforcement
- Real-time metric monitoring and alerting

Prepared for Coronation Day and testing phases.
"""

import json
import os
import statistics
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class MetricType(Enum):
    """Types of monitored metrics"""
    QEK = "QEK"  # Quantum Ethical Kernel
    H_VAR = "H_VAR"  # Harmonic Volatility Ratio
    ETHISCHES_IDEAL = "ETHISCHES_IDEAL"


@dataclass
class MetricSnapshot:
    """Represents a single metric measurement"""
    timestamp: str
    metric_type: MetricType
    value: float
    threshold_min: float
    threshold_max: float
    within_limits: bool
    deviation_pct: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "threshold_min": self.threshold_min,
            "threshold_max": self.threshold_max,
            "within_limits": self.within_limits,
            "deviation_pct": self.deviation_pct
        }


@dataclass
class Alert:
    """Represents an alert for metric deviation"""
    alert_id: str
    timestamp: str
    level: AlertLevel
    metric_type: MetricType
    message: str
    current_value: float
    threshold_breached: str
    recommended_action: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "level": self.level.value,
            "metric_type": self.metric_type.value,
            "message": self.message,
            "current_value": self.current_value,
            "threshold_breached": self.threshold_breached,
            "recommended_action": self.recommended_action
        }


@dataclass
class DriftPrediction:
    """Machine learning-based drift prediction result"""
    prediction_id: str
    timestamp: str
    metric_type: MetricType
    current_trend: str  # "stable", "drifting_up", "drifting_down"
    predicted_value: float
    confidence: float
    time_to_threshold_breach: Optional[float]  # hours until predicted breach
    anomaly_score: float
    requires_attention: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "timestamp": self.timestamp,
            "metric_type": self.metric_type.value,
            "current_trend": self.current_trend,
            "predicted_value": self.predicted_value,
            "confidence": self.confidence,
            "time_to_threshold_breach": self.time_to_threshold_breach,
            "anomaly_score": self.anomaly_score,
            "requires_attention": self.requires_attention
        }


class ThresholdMonitor:
    """
    Real-Time Threshold Monitoring System
    
    Monitors QEK (Quantum Ethical Kernel) and H-VAR (Harmonic Volatility Ratio)
    metrics with automated alerts, drift prediction, and Ethisches Ideal enforcement.
    """
    
    # Default thresholds for metrics (Ethisches Ideal limits)
    DEFAULT_THRESHOLDS = {
        MetricType.QEK: {
            "min": 0.85,
            "max": 1.00,
            "ideal": 0.938,
            "warning_buffer": 0.05,
            "critical_buffer": 0.02
        },
        MetricType.H_VAR: {
            "min": 0.00,
            "max": 0.10,
            "ideal": 0.043,
            "warning_buffer": 0.02,
            "critical_buffer": 0.01
        },
        MetricType.ETHISCHES_IDEAL: {
            "min": 0.95,
            "max": 1.00,
            "ideal": 1.00,
            "warning_buffer": 0.02,
            "critical_buffer": 0.01
        }
    }
    
    def __init__(self, log_path: str = "logs/threshold_monitor.log"):
        """Initialize the threshold monitor"""
        self.log_path = log_path
        self.metric_history: Dict[MetricType, List[MetricSnapshot]] = {
            MetricType.QEK: [],
            MetricType.H_VAR: [],
            MetricType.ETHISCHES_IDEAL: []
        }
        self.alerts: List[Alert] = []
        self.predictions: List[DriftPrediction] = []
        self.thresholds = self.DEFAULT_THRESHOLDS.copy()
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        return hashlib.sha256(
            f"ALERT-{datetime.now(timezone.utc).isoformat()}-{len(self.alerts)}".encode()
        ).hexdigest()[:12].upper()
    
    def _generate_prediction_id(self) -> str:
        """Generate unique prediction ID"""
        return hashlib.sha256(
            f"PRED-{datetime.now(timezone.utc).isoformat()}-{len(self.predictions)}".encode()
        ).hexdigest()[:12].upper()
    
    def record_metric(self, metric_type: MetricType, value: float) -> MetricSnapshot:
        """
        Record a new metric measurement and check thresholds
        
        Args:
            metric_type: Type of metric being recorded
            value: Current metric value
            
        Returns:
            MetricSnapshot with analysis results
        """
        threshold = self.thresholds[metric_type]
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate if within limits
        within_limits = threshold["min"] <= value <= threshold["max"]
        
        # Calculate deviation from ideal using absolute difference when ideal is zero
        ideal = threshold["ideal"]
        if ideal != 0:
            deviation_pct = abs((value - ideal) / ideal) * 100
        else:
            # For zero ideal (like H-VAR min), use the max threshold as reference
            max_threshold = threshold["max"]
            deviation_pct = (abs(value) / max_threshold) * 100 if max_threshold != 0 else 0.0
        
        snapshot = MetricSnapshot(
            timestamp=timestamp,
            metric_type=metric_type,
            value=round(value, 6),
            threshold_min=threshold["min"],
            threshold_max=threshold["max"],
            within_limits=within_limits,
            deviation_pct=round(deviation_pct, 4)
        )
        
        # Add to history
        self.metric_history[metric_type].append(snapshot)
        
        # Keep history manageable (last 1000 readings)
        if len(self.metric_history[metric_type]) > 1000:
            self.metric_history[metric_type] = self.metric_history[metric_type][-1000:]
        
        # Check for alerts
        self._check_thresholds_and_alert(snapshot)
        
        # Log the metric
        self._log_metric(snapshot)
        
        return snapshot
    
    def _check_thresholds_and_alert(self, snapshot: MetricSnapshot):
        """Check thresholds and generate alerts if needed"""
        threshold = self.thresholds[snapshot.metric_type]
        value = snapshot.value
        
        # Determine alert level and message
        alert_level = None
        message = ""
        threshold_breached = ""
        recommended_action = ""
        
        # For H-VAR, lower is generally better
        if snapshot.metric_type == MetricType.H_VAR:
            if value > threshold["max"]:
                alert_level = AlertLevel.CRITICAL
                message = f"H-VAR exceeded maximum threshold: {value:.4f} > {threshold['max']}"
                threshold_breached = "max"
                recommended_action = "Immediate review of network volatility factors required"
            elif value > threshold["max"] - threshold["critical_buffer"]:
                alert_level = AlertLevel.WARNING
                message = f"H-VAR approaching critical threshold: {value:.4f}"
                threshold_breached = "approaching_max"
                recommended_action = "Monitor closely and prepare stabilization measures"
        # For QEK and ETHISCHES_IDEAL, higher is better
        else:
            if value < threshold["min"]:
                alert_level = AlertLevel.CRITICAL
                message = f"{snapshot.metric_type.value} below minimum threshold: {value:.4f} < {threshold['min']}"
                threshold_breached = "min"
                recommended_action = "Immediate ethical kernel recalibration required"
            elif value < threshold["min"] + threshold["critical_buffer"]:
                alert_level = AlertLevel.WARNING
                message = f"{snapshot.metric_type.value} approaching critical threshold: {value:.4f}"
                threshold_breached = "approaching_min"
                recommended_action = "Review ethical alignment parameters"
            elif value > threshold["max"]:
                alert_level = AlertLevel.INFO
                message = f"{snapshot.metric_type.value} exceeds maximum (good): {value:.4f}"
                threshold_breached = "max_exceeded_positive"
                recommended_action = "No action required - system performing optimally"
        
        if alert_level:
            alert = Alert(
                alert_id=self._generate_alert_id(),
                timestamp=snapshot.timestamp,
                level=alert_level,
                metric_type=snapshot.metric_type,
                message=message,
                current_value=value,
                threshold_breached=threshold_breached,
                recommended_action=recommended_action
            )
            self.alerts.append(alert)
            self._log_alert(alert)
    
    def predict_drift(self, metric_type: MetricType) -> Optional[DriftPrediction]:
        """
        Use statistical analysis to predict metric drift
        
        This implements a simple but effective drift detection using:
        - Moving average analysis
        - Trend detection via linear regression approximation
        - Anomaly scoring based on standard deviation
        
        Args:
            metric_type: Type of metric to analyze
            
        Returns:
            DriftPrediction with analysis results or None if insufficient data
        """
        history = self.metric_history[metric_type]
        
        if len(history) < 10:
            return None  # Need sufficient data for prediction
        
        # Get recent values
        recent_values = [s.value for s in history[-50:]]  # Last 50 readings
        
        # Calculate statistics
        mean_val = statistics.mean(recent_values)
        std_dev = statistics.stdev(recent_values) if len(recent_values) > 1 else 0
        
        # Simple trend detection using first and second half comparison
        first_half = recent_values[:len(recent_values)//2]
        second_half = recent_values[len(recent_values)//2:]
        
        first_half_mean = statistics.mean(first_half)
        second_half_mean = statistics.mean(second_half)
        
        # Determine trend
        trend_delta = second_half_mean - first_half_mean
        threshold = self.thresholds[metric_type]
        
        if abs(trend_delta) < std_dev * 0.1:
            current_trend = "stable"
        elif trend_delta > 0:
            current_trend = "drifting_up"
        else:
            current_trend = "drifting_down"
        
        # Predict future value (simple linear extrapolation)
        predicted_value = second_half_mean + trend_delta * 0.5
        
        # Calculate confidence based on data consistency
        if std_dev > 0:
            cv = std_dev / mean_val if mean_val != 0 else 0  # Coefficient of variation
            confidence = max(0.5, 1.0 - cv)
        else:
            confidence = 0.95
        
        # Calculate time to threshold breach (if trend continues)
        time_to_breach = None
        if current_trend != "stable":
            if metric_type == MetricType.H_VAR:
                # For H-VAR, we're concerned about going above max
                if trend_delta > 0:
                    distance_to_breach = threshold["max"] - second_half_mean
                    if trend_delta != 0:
                        time_to_breach = abs(distance_to_breach / trend_delta) * 0.25  # hours
            else:
                # For QEK/ETHISCHES_IDEAL, we're concerned about going below min
                if trend_delta < 0:
                    distance_to_breach = second_half_mean - threshold["min"]
                    if trend_delta != 0:
                        time_to_breach = abs(distance_to_breach / trend_delta) * 0.25  # hours
        
        # Calculate anomaly score (z-score based)
        latest_value = recent_values[-1]
        if std_dev > 0:
            anomaly_score = abs(latest_value - mean_val) / std_dev
        else:
            anomaly_score = 0.0
        
        # Determine if attention is required
        requires_attention = (
            anomaly_score > 2.0 or  # More than 2 standard deviations
            (time_to_breach is not None and time_to_breach < 24) or  # Breach within 24 hours
            (current_trend != "stable" and abs(trend_delta) > std_dev)  # Significant drift
        )
        
        prediction = DriftPrediction(
            prediction_id=self._generate_prediction_id(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            metric_type=metric_type,
            current_trend=current_trend,
            predicted_value=round(predicted_value, 6),
            confidence=round(confidence, 4),
            time_to_threshold_breach=round(time_to_breach, 2) if time_to_breach else None,
            anomaly_score=round(anomaly_score, 4),
            requires_attention=requires_attention
        )
        
        self.predictions.append(prediction)
        self._log_prediction(prediction)
        
        return prediction
    
    def check_ethisches_ideal_limits(self) -> Dict[str, Any]:
        """
        Comprehensive check of all Ethisches Ideal limits
        
        Returns:
            Dictionary with status of all monitored metrics and overall compliance
        """
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_compliant": True,
            "metrics": {},
            "alerts_active": len([a for a in self.alerts[-10:] 
                                  if a.level in [AlertLevel.WARNING, AlertLevel.CRITICAL]]),
            "recommendations": []
        }
        
        for metric_type in MetricType:
            history = self.metric_history[metric_type]
            
            if not history:
                results["metrics"][metric_type.value] = {
                    "status": "no_data",
                    "current_value": None,
                    "compliant": None
                }
                continue
            
            latest = history[-1]
            threshold = self.thresholds[metric_type]
            
            # Calculate compliance status
            if latest.within_limits:
                status = "compliant"
            elif metric_type == MetricType.H_VAR and latest.value > threshold["max"]:
                status = "exceeds_limit"
                results["overall_compliant"] = False
            elif metric_type != MetricType.H_VAR and latest.value < threshold["min"]:
                status = "below_limit"
                results["overall_compliant"] = False
            else:
                status = "warning"
            
            results["metrics"][metric_type.value] = {
                "status": status,
                "current_value": latest.value,
                "ideal_value": threshold["ideal"],
                "deviation_pct": latest.deviation_pct,
                "compliant": latest.within_limits,
                "last_updated": latest.timestamp
            }
            
            # Add recommendations
            if status == "exceeds_limit" or status == "below_limit":
                results["recommendations"].append(
                    f"⚠️ {metric_type.value}: Immediate attention required - value {latest.value:.4f} "
                    f"is outside Ethisches Ideal limits [{threshold['min']}, {threshold['max']}]"
                )
            elif status == "warning":
                results["recommendations"].append(
                    f"📊 {metric_type.value}: Monitor closely - value {latest.value:.4f} "
                    f"is approaching threshold limits"
                )
        
        if not results["recommendations"]:
            results["recommendations"].append(
                "✅ All metrics within Ethisches Ideal limits - system operating optimally"
            )
        
        return results
    
    def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """
        Get data formatted for dashboard visualization
        
        Returns:
            Dashboard-ready data structure
        """
        dashboard_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": {},
            "recent_alerts": [],
            "drift_predictions": {},
            "ethisches_status": self.check_ethisches_ideal_limits()
        }
        
        for metric_type in MetricType:
            history = self.metric_history[metric_type]
            threshold = self.thresholds[metric_type]
            
            if history:
                # Get time series data for charts
                time_series = [
                    {"timestamp": s.timestamp, "value": s.value}
                    for s in history[-100:]  # Last 100 readings
                ]
                
                latest = history[-1]
                
                dashboard_data["metrics"][metric_type.value] = {
                    "current_value": latest.value,
                    "ideal_value": threshold["ideal"],
                    "min_threshold": threshold["min"],
                    "max_threshold": threshold["max"],
                    "within_limits": latest.within_limits,
                    "deviation_pct": latest.deviation_pct,
                    "time_series": time_series,
                    "status": "ok" if latest.within_limits else "alert"
                }
                
                # Get drift prediction
                prediction = self.predict_drift(metric_type)
                if prediction:
                    dashboard_data["drift_predictions"][metric_type.value] = prediction.to_dict()
        
        # Get recent alerts
        dashboard_data["recent_alerts"] = [
            a.to_dict() for a in self.alerts[-10:]
        ]
        
        return dashboard_data
    
    def _log_metric(self, snapshot: MetricSnapshot):
        """Log metric to file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(f"[METRIC] {snapshot.timestamp} | {snapshot.metric_type.value}: "
                       f"{snapshot.value:.6f} | Within limits: {snapshot.within_limits} | "
                       f"Deviation: {snapshot.deviation_pct:.2f}%\n")
        except (OSError, IOError):
            pass  # Fail silently if logging fails
    
    def _log_alert(self, alert: Alert):
        """Log alert to file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(f"[ALERT:{alert.level.value}] {alert.timestamp} | {alert.metric_type.value}: "
                       f"{alert.message} | Action: {alert.recommended_action}\n")
        except (OSError, IOError):
            pass
    
    def _log_prediction(self, prediction: DriftPrediction):
        """Log prediction to file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(f"[PREDICTION] {prediction.timestamp} | {prediction.metric_type.value}: "
                       f"Trend={prediction.current_trend} | Predicted={prediction.predicted_value:.6f} | "
                       f"Confidence={prediction.confidence:.2f} | Attention={prediction.requires_attention}\n")
        except (OSError, IOError):
            pass
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of recent alerts"""
        recent_alerts = self.alerts[-50:]  # Last 50 alerts
        
        return {
            "total_alerts": len(self.alerts),
            "recent_count": len(recent_alerts),
            "by_level": {
                AlertLevel.INFO.value: len([a for a in recent_alerts if a.level == AlertLevel.INFO]),
                AlertLevel.WARNING.value: len([a for a in recent_alerts if a.level == AlertLevel.WARNING]),
                AlertLevel.CRITICAL.value: len([a for a in recent_alerts if a.level == AlertLevel.CRITICAL]),
                AlertLevel.EMERGENCY.value: len([a for a in recent_alerts if a.level == AlertLevel.EMERGENCY])
            },
            "by_metric": {
                MetricType.QEK.value: len([a for a in recent_alerts if a.metric_type == MetricType.QEK]),
                MetricType.H_VAR.value: len([a for a in recent_alerts if a.metric_type == MetricType.H_VAR]),
                MetricType.ETHISCHES_IDEAL.value: len([a for a in recent_alerts if a.metric_type == MetricType.ETHISCHES_IDEAL])
            },
            "latest_alerts": [a.to_dict() for a in recent_alerts[-5:]]
        }


# Global monitor instance
_monitor_instance: Optional[ThresholdMonitor] = None


def get_threshold_monitor() -> ThresholdMonitor:
    """Get or create the global threshold monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = ThresholdMonitor()
    return _monitor_instance


if __name__ == "__main__":
    # Demo usage
    import random
    
    monitor = ThresholdMonitor()
    
    print("🔍 Threshold Monitor Demo")
    print("=" * 50)
    
    # Simulate some metric readings
    for i in range(20):
        # QEK - should stay high (0.85-1.0)
        qek_value = 0.93 + random.uniform(-0.05, 0.02)
        monitor.record_metric(MetricType.QEK, qek_value)
        
        # H-VAR - should stay low (0.0-0.1)
        hvar_value = 0.04 + random.uniform(-0.02, 0.03)
        monitor.record_metric(MetricType.H_VAR, hvar_value)
        
        # Ethisches Ideal - should be very high (0.95-1.0)
        ethik_value = 0.98 + random.uniform(-0.02, 0.02)
        monitor.record_metric(MetricType.ETHISCHES_IDEAL, ethik_value)
    
    # Check limits
    limits_status = monitor.check_ethisches_ideal_limits()
    print(f"\n📊 Ethisches Ideal Status:")
    print(f"   Overall Compliant: {limits_status['overall_compliant']}")
    for metric, data in limits_status["metrics"].items():
        print(f"   {metric}: {data['current_value']:.4f} ({data['status']})")
    
    # Get predictions
    print("\n🔮 Drift Predictions:")
    for metric_type in MetricType:
        pred = monitor.predict_drift(metric_type)
        if pred:
            print(f"   {metric_type.value}: Trend={pred.current_trend}, "
                  f"Confidence={pred.confidence:.2f}, Attention={pred.requires_attention}")
    
    # Get alert summary
    alert_summary = monitor.get_alert_summary()
    print(f"\n🚨 Alert Summary:")
    print(f"   Total: {alert_summary['total_alerts']}")
    print(f"   By Level: {alert_summary['by_level']}")
    
    print("\n✅ Demo complete!")
