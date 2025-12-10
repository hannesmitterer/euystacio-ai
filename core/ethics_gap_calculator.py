"""
ethics_gap_calculator.py
Ethics Gap and Enhanced H-VAR Measurement for Euystacio AI

This module provides:
- Ethics Gap calculation between ideal and actual ethical performance
- Enhanced H-VAR (Human Volatility) measurement
- Integration with CORAX corrective routines
- Diagnostic framework for ethical interventions

Part of the Incorruptible Global Health System (IGHS) framework.
"""

import json
import os
import statistics
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class EthicsGapSeverity(Enum):
    """Severity levels for Ethics Gap"""
    MINIMAL = "MINIMAL"  # < 0.1
    LOW = "LOW"  # 0.1 - 0.2
    MODERATE = "MODERATE"  # 0.2 - 0.4
    HIGH = "HIGH"  # 0.4 - 0.6
    CRITICAL = "CRITICAL"  # > 0.6


class VolatilityLevel(Enum):
    """Human Volatility levels"""
    STABLE = "STABLE"  # H-VAR < 0.02
    LOW = "LOW"  # 0.02 - 0.04
    MODERATE = "MODERATE"  # 0.04 - 0.08
    HIGH = "HIGH"  # 0.08 - 0.15
    EXTREME = "EXTREME"  # > 0.15


@dataclass
class EthicsGapMeasurement:
    """Measurement of the Ethics Gap"""
    measurement_id: str
    timestamp: str
    ethical_ideal: float  # Target ethical performance (0.0 - 1.0)
    actual_performance: float  # Current ethical performance (0.0 - 1.0)
    gap_value: float  # Difference (ideal - actual)
    gap_percentage: float  # Gap as percentage
    severity: EthicsGapSeverity
    contributing_factors: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "measurement_id": self.measurement_id,
            "timestamp": self.timestamp,
            "ethical_ideal": self.ethical_ideal,
            "actual_performance": self.actual_performance,
            "gap_value": self.gap_value,
            "gap_percentage": self.gap_percentage,
            "severity": self.severity.value,
            "contributing_factors": self.contributing_factors
        }


@dataclass
class HVARMeasurement:
    """Enhanced H-VAR (Human Volatility) measurement"""
    measurement_id: str
    timestamp: str
    hvar_value: float  # Volatility score (0.0 - 1.0)
    volatility_level: VolatilityLevel
    data_points: int  # Number of data points used
    standard_deviation: float
    mean_value: float
    trend: str  # "increasing", "decreasing", "stable"
    forecast_5_cycles: float  # Predicted H-VAR in 5 cycles
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "measurement_id": self.measurement_id,
            "timestamp": self.timestamp,
            "hvar_value": self.hvar_value,
            "volatility_level": self.volatility_level.value,
            "data_points": self.data_points,
            "standard_deviation": self.standard_deviation,
            "mean_value": self.mean_value,
            "trend": self.trend,
            "forecast_5_cycles": self.forecast_5_cycles
        }


@dataclass
class DiagnosticResult:
    """Result of ethical diagnostic analysis"""
    diagnostic_id: str
    timestamp: str
    ethics_gap: EthicsGapMeasurement
    hvar: HVARMeasurement
    intervention_required: bool
    intervention_urgency: str  # "low", "medium", "high", "critical"
    recommended_actions: List[str]
    corax_trigger: bool  # Whether to trigger CORAX routine
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagnostic_id": self.diagnostic_id,
            "timestamp": self.timestamp,
            "ethics_gap": self.ethics_gap.to_dict(),
            "hvar": self.hvar.to_dict(),
            "intervention_required": self.intervention_required,
            "intervention_urgency": self.intervention_urgency,
            "recommended_actions": self.recommended_actions,
            "corax_trigger": self.corax_trigger
        }


class EthicsGapCalculator:
    """
    Calculator for Ethics Gap and H-VAR measurements
    
    Provides diagnostic framework for identifying ethical performance gaps
    and human volatility, feeding directly into intervention mechanisms.
    """
    
    def __init__(self, log_path: str = "logs/ethics_gap.log"):
        """Initialize the Ethics Gap Calculator"""
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Measurement history
        self.ethics_gap_history: List[EthicsGapMeasurement] = []
        self.hvar_history: List[HVARMeasurement] = []
        self.diagnostic_history: List[DiagnosticResult] = []
        
        # Configuration
        self.ethical_ideal_target = 0.95  # Target ethical performance
        self.hvar_threshold = 0.043  # Maximum acceptable H-VAR (from CORAX-ROUTINE.txt)
        self.hvar_proactive_threshold = 0.042  # Proactive intervention threshold
        
        # Performance data buffer
        self.performance_buffer: List[float] = []
        self.max_buffer_size = 100
        
        # Constants for trend detection
        self.TREND_INCREASE_THRESHOLD = 1.05  # 5% increase threshold
        self.TREND_DECREASE_THRESHOLD = 0.95  # 5% decrease threshold
        
        self._log_event("ethics_gap_calculator_initialized", {
            "ethical_ideal_target": self.ethical_ideal_target,
            "hvar_threshold": self.hvar_threshold
        })
    
    def calculate_ethics_gap(
        self, 
        actual_performance: float,
        context: Optional[Dict[str, Any]] = None
    ) -> EthicsGapMeasurement:
        """
        Calculate the Ethics Gap between ideal and actual performance
        
        Args:
            actual_performance: Current ethical performance (0.0 - 1.0)
            context: Additional context for gap analysis
        
        Returns:
            EthicsGapMeasurement
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        measurement_id = self._generate_measurement_id("EG")
        
        # Calculate gap
        gap_value = self.ethical_ideal_target - actual_performance
        gap_percentage = (gap_value / self.ethical_ideal_target) * 100
        
        # Determine severity
        if gap_value < 0.1:
            severity = EthicsGapSeverity.MINIMAL
        elif gap_value < 0.2:
            severity = EthicsGapSeverity.LOW
        elif gap_value < 0.4:
            severity = EthicsGapSeverity.MODERATE
        elif gap_value < 0.6:
            severity = EthicsGapSeverity.HIGH
        else:
            severity = EthicsGapSeverity.CRITICAL
        
        # Identify contributing factors
        contributing_factors = self._identify_gap_factors(
            actual_performance, 
            context or {}
        )
        
        measurement = EthicsGapMeasurement(
            measurement_id=measurement_id,
            timestamp=timestamp,
            ethical_ideal=self.ethical_ideal_target,
            actual_performance=actual_performance,
            gap_value=gap_value,
            gap_percentage=gap_percentage,
            severity=severity,
            contributing_factors=contributing_factors
        )
        
        # Store in history
        self.ethics_gap_history.append(measurement)
        
        # Log measurement
        self._log_event("ethics_gap_calculated", measurement.to_dict())
        
        return measurement
    
    def calculate_hvar(
        self,
        performance_data: Optional[List[float]] = None
    ) -> HVARMeasurement:
        """
        Calculate H-VAR (Human Volatility) from performance data
        
        Args:
            performance_data: List of recent performance values (0.0 - 1.0)
                If None, uses internal buffer
        
        Returns:
            HVARMeasurement
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        measurement_id = self._generate_measurement_id("HV")
        
        # Use provided data or buffer
        data = performance_data if performance_data is not None else self.performance_buffer
        
        if len(data) < 2:
            # Insufficient data, return minimal volatility
            measurement = HVARMeasurement(
                measurement_id=measurement_id,
                timestamp=timestamp,
                hvar_value=0.0,
                volatility_level=VolatilityLevel.STABLE,
                data_points=len(data),
                standard_deviation=0.0,
                mean_value=data[0] if data else 0.0,
                trend="stable",
                forecast_5_cycles=data[0] if data else 0.0
            )
        else:
            # Calculate statistics
            mean_val = statistics.mean(data)
            std_dev = statistics.stdev(data) if len(data) > 1 else 0.0
            
            # H-VAR is normalized standard deviation
            hvar_value = std_dev / mean_val if mean_val > 0 else 0.0
            
            # Determine volatility level
            if hvar_value < 0.02:
                volatility_level = VolatilityLevel.STABLE
            elif hvar_value < 0.04:
                volatility_level = VolatilityLevel.LOW
            elif hvar_value < 0.08:
                volatility_level = VolatilityLevel.MODERATE
            elif hvar_value < 0.15:
                volatility_level = VolatilityLevel.HIGH
            else:
                volatility_level = VolatilityLevel.EXTREME
            
            # Determine trend
            if len(data) >= 5:
                recent_mean = statistics.mean(data[-5:])
                earlier_mean = statistics.mean(data[-10:-5]) if len(data) >= 10 else mean_val
                
                if recent_mean > earlier_mean * self.TREND_INCREASE_THRESHOLD:
                    trend = "increasing"
                elif recent_mean < earlier_mean * self.TREND_DECREASE_THRESHOLD:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "stable"
            
            # Forecast 5 cycles ahead using linear regression
            forecast = self._forecast_hvar(data, cycles=5)
            
            measurement = HVARMeasurement(
                measurement_id=measurement_id,
                timestamp=timestamp,
                hvar_value=hvar_value,
                volatility_level=volatility_level,
                data_points=len(data),
                standard_deviation=std_dev,
                mean_value=mean_val,
                trend=trend,
                forecast_5_cycles=forecast
            )
        
        # Store in history
        self.hvar_history.append(measurement)
        
        # Log measurement
        self._log_event("hvar_calculated", measurement.to_dict())
        
        return measurement
    
    def add_performance_data(self, value: float):
        """Add a performance data point to the buffer"""
        self.performance_buffer.append(value)
        
        # Trim buffer if too large
        if len(self.performance_buffer) > self.max_buffer_size:
            self.performance_buffer = self.performance_buffer[-self.max_buffer_size:]
    
    def run_diagnostic(
        self,
        actual_performance: float,
        context: Optional[Dict[str, Any]] = None
    ) -> DiagnosticResult:
        """
        Run complete diagnostic analysis
        
        Calculates both Ethics Gap and H-VAR, determines intervention needs,
        and provides recommendations.
        
        Args:
            actual_performance: Current ethical performance (0.0 - 1.0)
            context: Additional context for analysis
        
        Returns:
            DiagnosticResult with complete analysis
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        diagnostic_id = self._generate_measurement_id("DIAG")
        
        # Add to buffer
        self.add_performance_data(actual_performance)
        
        # Calculate Ethics Gap
        ethics_gap = self.calculate_ethics_gap(actual_performance, context)
        
        # Calculate H-VAR
        hvar = self.calculate_hvar()
        
        # Determine intervention requirements
        intervention_required = (
            ethics_gap.severity in [EthicsGapSeverity.HIGH, EthicsGapSeverity.CRITICAL] or
            hvar.hvar_value >= self.hvar_proactive_threshold or
            hvar.volatility_level in [VolatilityLevel.HIGH, VolatilityLevel.EXTREME]
        )
        
        # Determine urgency
        if ethics_gap.severity == EthicsGapSeverity.CRITICAL or hvar.volatility_level == VolatilityLevel.EXTREME:
            urgency = "critical"
        elif ethics_gap.severity == EthicsGapSeverity.HIGH or hvar.volatility_level == VolatilityLevel.HIGH:
            urgency = "high"
        elif ethics_gap.severity == EthicsGapSeverity.MODERATE or hvar.volatility_level == VolatilityLevel.MODERATE:
            urgency = "medium"
        else:
            urgency = "low"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(ethics_gap, hvar)
        
        # Determine if CORAX should be triggered
        corax_trigger = (
            hvar.hvar_value >= self.hvar_proactive_threshold or
            hvar.forecast_5_cycles >= self.hvar_threshold or
            ethics_gap.severity in [EthicsGapSeverity.HIGH, EthicsGapSeverity.CRITICAL]
        )
        
        diagnostic = DiagnosticResult(
            diagnostic_id=diagnostic_id,
            timestamp=timestamp,
            ethics_gap=ethics_gap,
            hvar=hvar,
            intervention_required=intervention_required,
            intervention_urgency=urgency,
            recommended_actions=recommendations,
            corax_trigger=corax_trigger
        )
        
        # Store in history
        self.diagnostic_history.append(diagnostic)
        
        # Log diagnostic
        self._log_event("diagnostic_completed", {
            "diagnostic_id": diagnostic_id,
            "intervention_required": intervention_required,
            "urgency": urgency,
            "corax_trigger": corax_trigger
        })
        
        return diagnostic
    
    def _identify_gap_factors(
        self,
        actual_performance: float,
        context: Dict[str, Any]
    ) -> List[str]:
        """Identify factors contributing to the Ethics Gap"""
        factors = []
        
        gap = self.ethical_ideal_target - actual_performance
        
        if gap > 0.1:
            if context.get("ownership_violations", 0) > 0:
                factors.append("Ownership violations detected")
            
            if context.get("sharing_compliance", 1.0) < 0.8:
                factors.append("Low sharing compliance")
            
            if context.get("love_license_score", 1.0) < 0.7:
                factors.append("Insufficient compassionate motivation")
            
            if context.get("dignity_violations", 0) > 0:
                factors.append("Human dignity violations")
            
            if context.get("access_restrictions", 0) > 0:
                factors.append("Discriminatory access restrictions")
            
            if context.get("bureaucratic_delays", 0) > 0:
                factors.append("Bureaucratic intervention delays")
        
        if not factors:
            factors.append("General ethical performance below ideal")
        
        return factors
    
    def _generate_recommendations(
        self,
        ethics_gap: EthicsGapMeasurement,
        hvar: HVARMeasurement
    ) -> List[str]:
        """Generate intervention recommendations"""
        recommendations = []
        
        # Ethics Gap recommendations
        if ethics_gap.severity in [EthicsGapSeverity.HIGH, EthicsGapSeverity.CRITICAL]:
            recommendations.append("URGENT: Implement immediate ethical correctives")
            recommendations.append("Review and enforce 'No ownership, only sharing' principle")
            
            for factor in ethics_gap.contributing_factors:
                if "ownership" in factor.lower():
                    recommendations.append("Eliminate ownership structures, convert to stewardship model")
                elif "sharing" in factor.lower():
                    recommendations.append("Enhance resource sharing mechanisms")
                elif "compassion" in factor.lower() or "love" in factor.lower():
                    recommendations.append("Strengthen compassionate motivation in actions")
                elif "dignity" in factor.lower():
                    recommendations.append("Implement dignity preservation protocols")
                elif "access" in factor.lower():
                    recommendations.append("Remove discriminatory access restrictions")
        
        # H-VAR recommendations
        if hvar.hvar_value >= self.hvar_threshold:
            recommendations.append("CRITICAL: H-VAR exceeded threshold - activate CORAX routine")
            recommendations.append("Implement load reduction (10-20%)")
            recommendations.append("Execute cooling cycle (3-5 seconds)")
        elif hvar.hvar_value >= self.hvar_proactive_threshold:
            recommendations.append("WARNING: H-VAR approaching threshold - proactive measures required")
            recommendations.append("Initiate preventive load balancing")
        
        if hvar.trend == "increasing":
            recommendations.append("H-VAR trend increasing - monitor closely")
            recommendations.append("Prepare for potential CORAX activation")
        
        if hvar.forecast_5_cycles >= self.hvar_threshold:
            recommendations.append("FORECAST: H-VAR predicted to breach threshold in 5 cycles")
            recommendations.append("Initiate preemptive stabilization measures")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue monitoring - parameters within acceptable range")
        
        return recommendations
    
    def _forecast_hvar(self, data: List[float], cycles: int) -> float:
        """Forecast H-VAR for future cycles using simple linear regression"""
        if len(data) < 3:
            return data[-1] if data else 0.0
        
        # Use last 10 data points for forecast
        recent_data = data[-10:] if len(data) >= 10 else data
        n = len(recent_data)
        
        # Calculate linear regression
        x = list(range(n))
        y = recent_data
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        # Calculate slope
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return y[-1]
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Forecast
        forecast_x = n + cycles - 1
        forecast_value = slope * forecast_x + intercept
        
        # Ensure non-negative
        return max(0.0, forecast_value)
    
    def get_diagnostic_summary(self) -> Dict[str, Any]:
        """Get summary of recent diagnostics"""
        if not self.diagnostic_history:
            return {
                "status": "no_data",
                "message": "No diagnostic data available"
            }
        
        recent = self.diagnostic_history[-10:]
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_diagnostics": len(self.diagnostic_history),
            "recent_diagnostics": len(recent),
            "interventions_required": sum(1 for d in recent if d.intervention_required),
            "corax_triggers": sum(1 for d in recent if d.corax_trigger),
            "latest_ethics_gap": recent[-1].ethics_gap.to_dict() if recent else None,
            "latest_hvar": recent[-1].hvar.to_dict() if recent else None,
            "average_ethics_gap": statistics.mean([d.ethics_gap.gap_value for d in recent]),
            "average_hvar": statistics.mean([d.hvar.hvar_value for d in recent]),
            "current_urgency": recent[-1].intervention_urgency if recent else "unknown"
        }
    
    def _generate_measurement_id(self, prefix: str) -> str:
        """Generate unique measurement ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        count = len(self.ethics_gap_history) + len(self.hvar_history)
        return f"{prefix}-{count:06d}-{int(datetime.now(timezone.utc).timestamp())}"
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log event to file"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


# Global instance
_ethics_gap_calculator_instance = None


def get_ethics_gap_calculator() -> EthicsGapCalculator:
    """Get global Ethics Gap Calculator instance"""
    global _ethics_gap_calculator_instance
    if _ethics_gap_calculator_instance is None:
        _ethics_gap_calculator_instance = EthicsGapCalculator()
    return _ethics_gap_calculator_instance


if __name__ == "__main__":
    # Demo usage
    calc = EthicsGapCalculator()
    
    # Simulate performance data
    print("Running diagnostic simulations...\n")
    
    # Scenario 1: Good performance
    print("Scenario 1: Good ethical performance")
    diagnostic1 = calc.run_diagnostic(
        actual_performance=0.93,
        context={
            "ownership_violations": 0,
            "sharing_compliance": 0.95,
            "love_license_score": 0.90
        }
    )
    print(f"Ethics Gap: {diagnostic1.ethics_gap.gap_value:.3f} ({diagnostic1.ethics_gap.severity.value})")
    print(f"H-VAR: {diagnostic1.hvar.hvar_value:.4f} ({diagnostic1.hvar.volatility_level.value})")
    print(f"Intervention required: {diagnostic1.intervention_required}")
    print(f"CORAX trigger: {diagnostic1.corax_trigger}\n")
    
    # Scenario 2: Moderate performance with volatility
    print("Scenario 2: Moderate performance with increasing volatility")
    for i in range(10):
        calc.add_performance_data(0.75 + (i * 0.02))  # Increasing trend
    
    diagnostic2 = calc.run_diagnostic(
        actual_performance=0.80,
        context={
            "ownership_violations": 2,
            "sharing_compliance": 0.70,
            "bureaucratic_delays": 3
        }
    )
    print(f"Ethics Gap: {diagnostic2.ethics_gap.gap_value:.3f} ({diagnostic2.ethics_gap.severity.value})")
    print(f"H-VAR: {diagnostic2.hvar.hvar_value:.4f} ({diagnostic2.hvar.volatility_level.value})")
    print(f"Trend: {diagnostic2.hvar.trend}")
    print(f"Forecast (5 cycles): {diagnostic2.hvar.forecast_5_cycles:.4f}")
    print(f"Intervention required: {diagnostic2.intervention_required}")
    print(f"Urgency: {diagnostic2.intervention_urgency}")
    print(f"CORAX trigger: {diagnostic2.corax_trigger}")
    print(f"Recommendations: {len(diagnostic2.recommended_actions)}")
    for rec in diagnostic2.recommended_actions[:3]:
        print(f"  - {rec}")
