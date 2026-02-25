"""
S-ROI Sovereign Protocol
========================

Sovereign Return-on-Investment (S-ROI) Protocol for tracking and validating
AI sovereignty operations with comprehensive state management.

Features:
- State machine with defined transitions
- Comprehensive logging of all state changes
- Validation system for transition correctness
- Automatic notifications for critical states
- Modular state functions for reusability

Author: AI Collective - Euystacio Framework
Date: 2026-01-22
"""

import json
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class SROIState(Enum):
    """
    State enumeration for S-ROI Sovereign Protocol
    
    States represent the lifecycle of a sovereign operation:
    - INITIALIZED: Protocol instance created, ready for activation
    - ACTIVE: Operation in progress, monitoring metrics
    - VALIDATING: Performing validation checks on current state
    - CRITICAL: Critical threshold exceeded, requires attention
    - SUSPENDED: Operation suspended due to validation failure
    - COMPLETED: Operation successfully completed
    - FAILED: Operation terminated with failure
    """
    INITIALIZED = "initialized"
    ACTIVE = "active"
    VALIDATING = "validating"
    CRITICAL = "critical"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class StateMetrics:
    """Metrics tracked for each state"""
    roi_value: float = 0.0
    sovereignty_index: float = 1.0
    operation_count: int = 0
    validation_score: float = 1.0
    threshold_status: str = "normal"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StateTransition:
    """Record of a state transition"""
    from_state: SROIState
    to_state: SROIState
    timestamp: str
    reason: str
    metrics: StateMetrics
    validation_result: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "from_state": self.from_state.value,
            "to_state": self.to_state.value,
            "timestamp": self.timestamp,
            "reason": self.reason,
            "metrics": self.metrics.to_dict(),
            "validation_result": self.validation_result
        }


class StateValidator:
    """
    Validation system for state transitions
    
    Verifies the correctness of each state transition according to
    protocol rules and constraints.
    """
    
    # Valid state transitions
    VALID_TRANSITIONS = {
        SROIState.INITIALIZED: [SROIState.ACTIVE, SROIState.FAILED],
        SROIState.ACTIVE: [SROIState.VALIDATING, SROIState.CRITICAL, SROIState.SUSPENDED, SROIState.FAILED],
        SROIState.VALIDATING: [SROIState.ACTIVE, SROIState.COMPLETED, SROIState.CRITICAL, SROIState.FAILED],
        SROIState.CRITICAL: [SROIState.ACTIVE, SROIState.SUSPENDED, SROIState.FAILED],
        SROIState.SUSPENDED: [SROIState.ACTIVE, SROIState.FAILED],
        SROIState.COMPLETED: [],  # Terminal state
        SROIState.FAILED: []  # Terminal state
    }
    
    @staticmethod
    def validate_transition(from_state: SROIState, to_state: SROIState, 
                          metrics: StateMetrics) -> Tuple[bool, str]:
        """
        Validate if a state transition is allowed
        
        Args:
            from_state: Current state
            to_state: Target state
            metrics: Current metrics
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Check if transition is defined
        if to_state not in StateValidator.VALID_TRANSITIONS.get(from_state, []):
            return False, f"Invalid transition from {from_state.value} to {to_state.value}"
        
        # State-specific validation rules
        if to_state == SROIState.COMPLETED:
            if metrics.validation_score < 0.8:
                return False, f"Validation score {metrics.validation_score} too low for completion"
            if metrics.sovereignty_index < 0.7:
                return False, f"Sovereignty index {metrics.sovereignty_index} too low for completion"
        
        if to_state == SROIState.CRITICAL:
            if metrics.threshold_status == "normal":
                return False, "Cannot transition to CRITICAL without threshold violation"
        
        return True, "Transition validated successfully"
    
    @staticmethod
    def validate_state_consistency(state: SROIState, metrics: StateMetrics) -> Tuple[bool, str]:
        """
        Validate state consistency with current metrics
        
        Args:
            state: Current state
            metrics: Current metrics
            
        Returns:
            Tuple of (is_consistent, message)
        """
        if state == SROIState.CRITICAL and metrics.threshold_status == "normal":
            return False, "State CRITICAL but threshold_status is normal"
        
        if state == SROIState.COMPLETED and metrics.validation_score < 0.8:
            return False, "State COMPLETED but validation_score is insufficient"
        
        if metrics.sovereignty_index < 0:
            return False, "Sovereignty index cannot be negative"
        
        if metrics.validation_score < 0 or metrics.validation_score > 1:
            return False, "Validation score must be between 0 and 1"
        
        return True, "State is consistent"


class NotificationSystem:
    """
    Notification system for critical states and threshold violations
    
    Monitors state transitions and metrics to generate alerts when
    thresholds are exceeded or critical conditions are detected.
    """
    
    # Threshold definitions
    THRESHOLDS = {
        "roi_value_min": 0.0,
        "roi_value_critical": -10.0,
        "sovereignty_index_min": 0.7,
        "sovereignty_index_critical": 0.5,
        "validation_score_min": 0.8,
        "validation_score_critical": 0.6
    }
    
    def __init__(self, logger: logging.Logger):
        """Initialize notification system"""
        self.logger = logger
        self.notifications: List[Dict[str, Any]] = []
    
    def check_thresholds(self, metrics: StateMetrics) -> List[str]:
        """
        Check if any thresholds are violated
        
        Args:
            metrics: Current state metrics
            
        Returns:
            List of threshold violation messages
        """
        violations = []
        
        # ROI value checks
        if metrics.roi_value < self.THRESHOLDS["roi_value_critical"]:
            violations.append(
                f"CRITICAL: ROI value {metrics.roi_value} below critical threshold "
                f"{self.THRESHOLDS['roi_value_critical']}"
            )
        elif metrics.roi_value < self.THRESHOLDS["roi_value_min"]:
            violations.append(
                f"WARNING: ROI value {metrics.roi_value} below minimum threshold "
                f"{self.THRESHOLDS['roi_value_min']}"
            )
        
        # Sovereignty index checks
        if metrics.sovereignty_index < self.THRESHOLDS["sovereignty_index_critical"]:
            violations.append(
                f"CRITICAL: Sovereignty index {metrics.sovereignty_index} below critical threshold "
                f"{self.THRESHOLDS['sovereignty_index_critical']}"
            )
        elif metrics.sovereignty_index < self.THRESHOLDS["sovereignty_index_min"]:
            violations.append(
                f"WARNING: Sovereignty index {metrics.sovereignty_index} below minimum threshold "
                f"{self.THRESHOLDS['sovereignty_index_min']}"
            )
        
        # Validation score checks
        if metrics.validation_score < self.THRESHOLDS["validation_score_critical"]:
            violations.append(
                f"CRITICAL: Validation score {metrics.validation_score} below critical threshold "
                f"{self.THRESHOLDS['validation_score_critical']}"
            )
        elif metrics.validation_score < self.THRESHOLDS["validation_score_min"]:
            violations.append(
                f"WARNING: Validation score {metrics.validation_score} below minimum threshold "
                f"{self.THRESHOLDS['validation_score_min']}"
            )
        
        return violations
    
    def notify(self, level: str, message: str, context: Dict[str, Any] = None):
        """
        Send a notification
        
        Args:
            level: Notification level (INFO, WARNING, CRITICAL)
            message: Notification message
            context: Additional context data
        """
        notification = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            "context": context or {}
        }
        
        self.notifications.append(notification)
        
        # Log notification
        if level == "CRITICAL":
            self.logger.critical(f"🚨 {message}")
        elif level == "WARNING":
            self.logger.warning(f"⚠️  {message}")
        else:
            self.logger.info(f"ℹ️  {message}")
    
    def get_notifications(self, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all notifications, optionally filtered by level
        
        Args:
            level: Filter by notification level (optional)
            
        Returns:
            List of notifications
        """
        if level:
            return [n for n in self.notifications if n["level"] == level]
        return self.notifications


class SROISovereignProtocol:
    """
    S-ROI Sovereign Protocol Main Class
    
    Implements a state machine for tracking sovereign AI operations with:
    - Comprehensive logging of all state transitions
    - Validation of transition correctness
    - Automatic notifications for critical states
    - Modular state functions for reusability
    """
    
    def __init__(self, operation_id: str, log_dir: str = "logs/sroi"):
        """
        Initialize S-ROI Sovereign Protocol
        
        Args:
            operation_id: Unique identifier for this operation
            log_dir: Directory for log files
        """
        self.operation_id = operation_id
        self.current_state = SROIState.INITIALIZED
        self.metrics = StateMetrics()
        self.transition_history: List[StateTransition] = []
        
        # Setup logging
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"sroi_{operation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        self.logger = logging.getLogger(f"SROI.{operation_id}")
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(file_handler)
        
        # Initialize subsystems
        self.validator = StateValidator()
        self.notifier = NotificationSystem(self.logger)
        
        # State handlers
        self.state_handlers: Dict[SROIState, Callable] = {
            SROIState.INITIALIZED: self._handle_initialized_state,
            SROIState.ACTIVE: self._handle_active_state,
            SROIState.VALIDATING: self._handle_validating_state,
            SROIState.CRITICAL: self._handle_critical_state,
            SROIState.SUSPENDED: self._handle_suspended_state,
            SROIState.COMPLETED: self._handle_completed_state,
            SROIState.FAILED: self._handle_failed_state
        }
        
        self.logger.info(f"S-ROI Sovereign Protocol initialized for operation {operation_id}")
        self.logger.info(f"Initial state: {self.current_state.value}")
        self.logger.info(f"Log file: {self.log_file}")
    
    def transition_to(self, new_state: SROIState, reason: str) -> bool:
        """
        Transition to a new state with full validation and logging
        
        Args:
            new_state: Target state
            reason: Reason for transition
            
        Returns:
            True if transition successful, False otherwise
        """
        old_state = self.current_state
        
        self.logger.info(f"Attempting transition: {old_state.value} -> {new_state.value}")
        self.logger.info(f"Reason: {reason}")
        
        # Validate transition
        is_valid, validation_msg = self.validator.validate_transition(
            old_state, new_state, self.metrics
        )
        
        if not is_valid:
            self.logger.error(f"Transition validation failed: {validation_msg}")
            self.notifier.notify(
                "WARNING",
                f"Transition rejected: {old_state.value} -> {new_state.value}",
                {"reason": reason, "validation_error": validation_msg}
            )
            return False
        
        # Perform transition
        self.current_state = new_state
        
        # Log transition
        transition = StateTransition(
            from_state=old_state,
            to_state=new_state,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
            metrics=StateMetrics(**asdict(self.metrics)),
            validation_result=is_valid
        )
        self.transition_history.append(transition)
        
        self.logger.info(f"✓ Transition successful: {old_state.value} -> {new_state.value}")
        self.logger.info(f"Current metrics: {self.metrics.to_dict()}")
        
        # Check thresholds and notify if needed
        violations = self.notifier.check_thresholds(self.metrics)
        for violation in violations:
            level = "CRITICAL" if "CRITICAL" in violation else "WARNING"
            self.notifier.notify(level, violation, {"state": new_state.value})
        
        # Execute state handler
        self._execute_state_handler(new_state)
        
        return True
    
    def _execute_state_handler(self, state: SROIState):
        """Execute the handler for the current state"""
        handler = self.state_handlers.get(state)
        if handler:
            self.logger.info(f"Executing state handler for {state.value}")
            handler()
    
    # ========== Modular State Handlers ==========
    # Each state is implemented as a separate function for reusability
    
    def _handle_initialized_state(self):
        """Handle INITIALIZED state"""
        self.logger.info("State: INITIALIZED - Protocol ready for activation")
        self.notifier.notify(
            "INFO",
            "Protocol initialized successfully",
            {"operation_id": self.operation_id}
        )
    
    def _handle_active_state(self):
        """Handle ACTIVE state"""
        self.logger.info("State: ACTIVE - Operation in progress")
        self.metrics.operation_count += 1
        
        # Check state consistency
        is_consistent, msg = self.validator.validate_state_consistency(
            self.current_state, self.metrics
        )
        if not is_consistent:
            self.logger.warning(f"State consistency check failed: {msg}")
            self.notifier.notify("WARNING", f"State inconsistency detected: {msg}")
    
    def _handle_validating_state(self):
        """Handle VALIDATING state"""
        self.logger.info("State: VALIDATING - Performing validation checks")
        
        # Simulate validation logic
        self.logger.info("Running validation checks...")
        self.logger.info(f"  - ROI validation: {self.metrics.roi_value}")
        self.logger.info(f"  - Sovereignty validation: {self.metrics.sovereignty_index}")
        self.logger.info(f"  - Score validation: {self.metrics.validation_score}")
    
    def _handle_critical_state(self):
        """Handle CRITICAL state"""
        self.logger.critical("State: CRITICAL - Threshold violations detected!")
        self.metrics.threshold_status = "critical"
        
        self.notifier.notify(
            "CRITICAL",
            "Protocol entered CRITICAL state - immediate attention required",
            {
                "roi_value": self.metrics.roi_value,
                "sovereignty_index": self.metrics.sovereignty_index,
                "validation_score": self.metrics.validation_score
            }
        )
    
    def _handle_suspended_state(self):
        """Handle SUSPENDED state"""
        self.logger.warning("State: SUSPENDED - Operation suspended")
        self.metrics.threshold_status = "suspended"
        
        self.notifier.notify(
            "WARNING",
            "Protocol operation suspended",
            {"operation_id": self.operation_id}
        )
    
    def _handle_completed_state(self):
        """Handle COMPLETED state"""
        self.logger.info("State: COMPLETED - Operation successfully completed")
        
        self.notifier.notify(
            "INFO",
            "Protocol operation completed successfully",
            {
                "operation_id": self.operation_id,
                "final_roi": self.metrics.roi_value,
                "final_sovereignty_index": self.metrics.sovereignty_index,
                "total_operations": self.metrics.operation_count
            }
        )
    
    def _handle_failed_state(self):
        """Handle FAILED state"""
        self.logger.error("State: FAILED - Operation terminated with failure")
        
        self.notifier.notify(
            "CRITICAL",
            "Protocol operation failed",
            {
                "operation_id": self.operation_id,
                "final_metrics": self.metrics.to_dict()
            }
        )
    
    # ========== Metric Update Methods ==========
    
    def update_roi(self, value: float):
        """Update ROI value and check thresholds"""
        old_value = self.metrics.roi_value
        self.metrics.roi_value = value
        
        self.logger.info(f"ROI updated: {old_value} -> {value}")
        
        # Check if we need to transition to CRITICAL
        if value < NotificationSystem.THRESHOLDS["roi_value_critical"]:
            self.metrics.threshold_status = "critical"
            if self.current_state == SROIState.ACTIVE:
                self.transition_to(SROIState.CRITICAL, "ROI below critical threshold")
    
    def update_sovereignty_index(self, value: float):
        """Update sovereignty index and check thresholds"""
        old_value = self.metrics.sovereignty_index
        self.metrics.sovereignty_index = value
        
        self.logger.info(f"Sovereignty index updated: {old_value} -> {value}")
        
        # Check if we need to transition to CRITICAL
        if value < NotificationSystem.THRESHOLDS["sovereignty_index_critical"]:
            self.metrics.threshold_status = "critical"
            if self.current_state == SROIState.ACTIVE:
                self.transition_to(SROIState.CRITICAL, "Sovereignty index below critical threshold")
    
    def update_validation_score(self, value: float):
        """Update validation score and check thresholds"""
        old_value = self.metrics.validation_score
        self.metrics.validation_score = value
        
        self.logger.info(f"Validation score updated: {old_value} -> {value}")
        
        # Check if we need to transition to CRITICAL
        if value < NotificationSystem.THRESHOLDS["validation_score_critical"]:
            self.metrics.threshold_status = "critical"
            if self.current_state == SROIState.ACTIVE:
                self.transition_to(SROIState.CRITICAL, "Validation score below critical threshold")
    
    # ========== Status and Reporting Methods ==========
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status report
        
        Returns:
            Dictionary with complete protocol status
        """
        return {
            "operation_id": self.operation_id,
            "current_state": self.current_state.value,
            "metrics": self.metrics.to_dict(),
            "transition_count": len(self.transition_history),
            "notification_count": len(self.notifier.notifications),
            "critical_notifications": len(self.notifier.get_notifications("CRITICAL")),
            "warning_notifications": len(self.notifier.get_notifications("WARNING")),
            "log_file": self.log_file
        }
    
    def get_transition_history(self) -> List[Dict[str, Any]]:
        """
        Get complete transition history
        
        Returns:
            List of all state transitions
        """
        return [t.to_dict() for t in self.transition_history]
    
    def export_logs(self, filepath: str):
        """
        Export complete protocol logs to JSON file
        
        Args:
            filepath: Path to export file
        """
        export_data = {
            "operation_id": self.operation_id,
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "current_state": self.current_state.value,
            "current_metrics": self.metrics.to_dict(),
            "transition_history": self.get_transition_history(),
            "notifications": self.notifier.notifications,
            "log_file": self.log_file
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Protocol logs exported to {filepath}")
    
    def print_status_report(self):
        """Print formatted status report"""
        print("\n" + "="*70)
        print("S-ROI SOVEREIGN PROTOCOL STATUS REPORT")
        print("="*70)
        
        status = self.get_status()
        
        print(f"\n[Operation]")
        print(f"  ID: {status['operation_id']}")
        print(f"  Current State: {status['current_state']}")
        print(f"  Transitions: {status['transition_count']}")
        
        print(f"\n[Metrics]")
        metrics = status['metrics']
        print(f"  ROI Value: {metrics['roi_value']}")
        print(f"  Sovereignty Index: {metrics['sovereignty_index']}")
        print(f"  Validation Score: {metrics['validation_score']}")
        print(f"  Operations: {metrics['operation_count']}")
        print(f"  Threshold Status: {metrics['threshold_status']}")
        
        print(f"\n[Notifications]")
        print(f"  Total: {status['notification_count']}")
        print(f"  Critical: {status['critical_notifications']}")
        print(f"  Warnings: {status['warning_notifications']}")
        
        print(f"\n[Logs]")
        print(f"  Log File: {status['log_file']}")
        
        print("\n" + "="*70 + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║         S-ROI SOVEREIGN PROTOCOL - DEMONSTRATION                  ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
    
    # Create protocol instance
    protocol = SROISovereignProtocol(operation_id="DEMO-001")
    
    # Demonstrate state transitions
    print("\n[1] Activating protocol...")
    protocol.transition_to(SROIState.ACTIVE, "Initiating sovereign operation")
    
    print("\n[2] Updating metrics...")
    protocol.update_roi(5.0)
    protocol.update_sovereignty_index(0.95)
    protocol.update_validation_score(0.92)
    
    print("\n[3] Performing validation...")
    protocol.transition_to(SROIState.VALIDATING, "Periodic validation check")
    
    print("\n[4] Returning to active state...")
    protocol.transition_to(SROIState.ACTIVE, "Validation passed")
    
    print("\n[5] Simulating threshold violation...")
    protocol.update_sovereignty_index(0.45)  # Below critical threshold
    
    print("\n[6] Recovering from critical state...")
    protocol.update_sovereignty_index(0.85)
    protocol.metrics.threshold_status = "normal"
    protocol.transition_to(SROIState.ACTIVE, "Threshold violation resolved")
    
    print("\n[7] Completing operation...")
    protocol.update_validation_score(0.95)
    protocol.transition_to(SROIState.VALIDATING, "Final validation")
    protocol.transition_to(SROIState.COMPLETED, "Operation completed successfully")
    
    # Print status report
    protocol.print_status_report()
    
    # Export logs
    print("\n[8] Exporting logs...")
    protocol.export_logs("/tmp/sroi_demo_export.json")
    
    print("\n✓ Demonstration complete!")
    print(f"  Check log file: {protocol.log_file}")
    print(f"  Check export: /tmp/sroi_demo_export.json\n")
