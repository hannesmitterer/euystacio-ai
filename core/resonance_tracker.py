"""
resonance_tracker.py
Resonance Tracking Module for S-ROI Sovereign Protocol

Tracks resonance levels, state changes, and provides logging functionality.
Implements WARNING state for values near thresholds.
"""

import time
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ResonanceState(Enum):
    """Resonance state levels"""
    NORMAL = "NORMAL"  # Normal operation
    WARNING = "WARNING"  # Near threshold - requires attention
    CRITICAL = "CRITICAL"  # Critical level - action required
    STABLE = "STABLE"  # Highly stable resonance


@dataclass
class ResonanceReading:
    """Single resonance reading"""
    timestamp: float
    value: float
    state: ResonanceState
    source: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
            "value": self.value,
            "state": self.state.value,
            "source": self.source,
            "metadata": self.metadata
        }


@dataclass
class StateChangeLog:
    """Log entry for state changes"""
    timestamp: float
    previous_state: str
    new_state: str
    resonance_value: float
    trigger: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "resonance_value": self.resonance_value,
            "trigger": self.trigger,
            "details": self.details
        }


class ResonanceTracker:
    """
    Tracks resonance levels and manages state transitions
    
    Features:
    - Continuous resonance monitoring
    - State change logging
    - WARNING state for near-threshold values
    - Historical data retention
    """
    
    def __init__(self, 
                 warning_threshold: float = 0.75,
                 critical_threshold: float = 0.9,
                 stable_threshold: float = 0.95):
        """
        Initialize resonance tracker
        
        Args:
            warning_threshold: Threshold for WARNING state (0.0-1.0)
            critical_threshold: Threshold for CRITICAL state (0.0-1.0)
            stable_threshold: Threshold for STABLE state (0.0-1.0)
        """
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.stable_threshold = stable_threshold
        
        # Current state
        self.current_resonance: Optional[float] = None
        self.current_state: ResonanceState = ResonanceState.NORMAL
        
        # History
        self.resonance_history: List[ResonanceReading] = []
        self.state_change_log: List[StateChangeLog] = []
        
        # Limits
        self.max_history_size = 1000
        self.max_log_size = 500
        
    def record_resonance(self, 
                        value: float, 
                        source: str = "unknown",
                        metadata: Optional[Dict[str, Any]] = None) -> ResonanceState:
        """
        Record a resonance reading
        
        Args:
            value: Resonance value (0.0-1.0)
            source: Source of the reading
            metadata: Additional metadata
            
        Returns:
            Current resonance state
        """
        # Validate value
        value = max(0.0, min(1.0, value))
        
        # Determine state
        new_state = self._determine_state(value)
        
        # Create reading
        reading = ResonanceReading(
            timestamp=time.time(),
            value=value,
            state=new_state,
            source=source,
            metadata=metadata or {}
        )
        
        # Add to history
        self.resonance_history.append(reading)
        
        # Trim history if needed
        if len(self.resonance_history) > self.max_history_size:
            self.resonance_history = self.resonance_history[-self.max_history_size:]
        
        # Check for state change
        if new_state != self.current_state:
            self._log_state_change(
                previous_state=self.current_state,
                new_state=new_state,
                resonance_value=value,
                trigger=source,
                details=metadata or {}
            )
            self.current_state = new_state
        
        # Update current resonance
        self.current_resonance = value
        
        return new_state
    
    def _determine_state(self, value: float) -> ResonanceState:
        """
        Determine resonance state based on value
        
        Args:
            value: Resonance value
            
        Returns:
            Corresponding ResonanceState
        """
        if value >= self.stable_threshold:
            return ResonanceState.STABLE
        elif value >= self.critical_threshold:
            return ResonanceState.CRITICAL
        elif value >= self.warning_threshold:
            return ResonanceState.WARNING
        else:
            return ResonanceState.NORMAL
    
    def _log_state_change(self,
                         previous_state: ResonanceState,
                         new_state: ResonanceState,
                         resonance_value: float,
                         trigger: str,
                         details: Dict[str, Any]):
        """
        Log a state change
        
        Args:
            previous_state: Previous state
            new_state: New state
            resonance_value: Resonance value at change
            trigger: What triggered the change
            details: Additional details
        """
        log_entry = StateChangeLog(
            timestamp=time.time(),
            previous_state=previous_state.value,
            new_state=new_state.value,
            resonance_value=resonance_value,
            trigger=trigger,
            details=details
        )
        
        self.state_change_log.append(log_entry)
        
        # Trim log if needed
        if len(self.state_change_log) > self.max_log_size:
            self.state_change_log = self.state_change_log[-self.max_log_size:]
        
        # Print notification
        print(f"[Resonance] State change: {previous_state.value} → {new_state.value} "
              f"(resonance: {resonance_value:.2f})")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current resonance status"""
        return {
            "current_resonance": self.current_resonance,
            "current_state": self.current_state.value,
            "warning_threshold": self.warning_threshold,
            "critical_threshold": self.critical_threshold,
            "stable_threshold": self.stable_threshold,
            "total_readings": len(self.resonance_history),
            "total_state_changes": len(self.state_change_log)
        }
    
    def get_recent_readings(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent resonance readings
        
        Args:
            count: Number of readings to return
            
        Returns:
            List of recent readings
        """
        recent = self.resonance_history[-count:] if self.resonance_history else []
        return [r.to_dict() for r in recent]
    
    def get_state_change_history(self, count: int = 20) -> List[Dict[str, Any]]:
        """
        Get state change history
        
        Args:
            count: Number of changes to return
            
        Returns:
            List of state changes
        """
        recent = self.state_change_log[-count:] if self.state_change_log else []
        return [log.to_dict() for log in recent]
    
    def calculate_average_resonance(self, 
                                    time_window_seconds: Optional[float] = None) -> Optional[float]:
        """
        Calculate average resonance over time window
        
        Args:
            time_window_seconds: Time window in seconds (None for all history)
            
        Returns:
            Average resonance value or None if no data
        """
        if not self.resonance_history:
            return None
        
        if time_window_seconds is None:
            # All history
            values = [r.value for r in self.resonance_history]
        else:
            # Filter by time window
            cutoff_time = time.time() - time_window_seconds
            values = [r.value for r in self.resonance_history if r.timestamp >= cutoff_time]
        
        if not values:
            return None
        
        return sum(values) / len(values)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        if not self.resonance_history:
            return {
                "total_readings": 0,
                "message": "No resonance data available"
            }
        
        values = [r.value for r in self.resonance_history]
        
        # Calculate statistics
        avg = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)
        
        # Count by state
        state_counts = {}
        for reading in self.resonance_history:
            state = reading.state.value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "total_readings": len(self.resonance_history),
            "total_state_changes": len(self.state_change_log),
            "current_resonance": self.current_resonance,
            "current_state": self.current_state.value,
            "average_resonance": avg,
            "min_resonance": min_val,
            "max_resonance": max_val,
            "readings_by_state": state_counts,
            "avg_last_10_readings": self.calculate_average_resonance(600)  # Last 10 minutes
        }
    
    def export_logs(self, filepath: str):
        """
        Export logs to JSON file
        
        Args:
            filepath: Path to export file
        """
        data = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "current_status": self.get_current_status(),
            "statistics": self.get_statistics(),
            "recent_readings": self.get_recent_readings(50),
            "state_change_history": self.get_state_change_history(50)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[Resonance] Logs exported to {filepath}")
    
    def is_in_warning_zone(self) -> bool:
        """Check if current resonance is in warning zone"""
        if self.current_resonance is None:
            return False
        
        return (self.warning_threshold <= self.current_resonance < self.critical_threshold)
    
    def is_critical(self) -> bool:
        """Check if current resonance is critical"""
        if self.current_resonance is None:
            return False
        
        return self.current_resonance >= self.critical_threshold
    
    def is_stable(self) -> bool:
        """Check if current resonance is stable"""
        if self.current_resonance is None:
            return False
        
        return self.current_resonance >= self.stable_threshold


# Self-test
if __name__ == "__main__":
    print("=== Resonance Tracker Self-Test ===\n")
    
    tracker = ResonanceTracker(
        warning_threshold=0.75,
        critical_threshold=0.9,
        stable_threshold=0.95
    )
    
    print("1. Recording resonance values:")
    
    # Test progression through states
    test_values = [
        (0.5, "normal_operation"),
        (0.76, "increasing_load"),
        (0.78, "sustained_load"),
        (0.91, "peak_activity"),
        (0.96, "optimal_resonance"),
        (0.88, "cooling_down"),
        (0.72, "returning_normal")
    ]
    
    for value, source in test_values:
        state = tracker.record_resonance(value, source=source, metadata={"test": True})
        print(f"   {source}: {value:.2f} → {state.value}")
        time.sleep(0.1)
    
    print("\n2. Current Status:")
    status = tracker.get_current_status()
    for key, val in status.items():
        print(f"   {key}: {val}")
    
    print("\n3. Statistics:")
    stats = tracker.get_statistics()
    for key, val in stats.items():
        print(f"   {key}: {val}")
    
    print("\n4. State Change History:")
    history = tracker.get_state_change_history(10)
    for change in history:
        print(f"   {change['previous_state']} → {change['new_state']} "
              f"(resonance: {change['resonance_value']:.2f})")
    
    print("\n5. Warning Zone Check:")
    print(f"   In warning zone: {tracker.is_in_warning_zone()}")
    print(f"   Critical: {tracker.is_critical()}")
    print(f"   Stable: {tracker.is_stable()}")
    
    print("\n✅ Resonance Tracker operational")
