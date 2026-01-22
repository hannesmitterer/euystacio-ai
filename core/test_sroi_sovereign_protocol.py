"""
Unit Tests for S-ROI Sovereign Protocol

Tests all components:
- State transitions
- Validation system
- Notification system
- Logging functionality
- Metric updates
"""

import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime

from core.sroi_sovereign_protocol import (
    SROIState,
    StateMetrics,
    StateValidator,
    NotificationSystem,
    SROISovereignProtocol
)


class TestStateMetrics(unittest.TestCase):
    """Test StateMetrics dataclass"""
    
    def test_default_values(self):
        """Test default metric values"""
        metrics = StateMetrics()
        self.assertEqual(metrics.roi_value, 0.0)
        self.assertEqual(metrics.sovereignty_index, 1.0)
        self.assertEqual(metrics.operation_count, 0)
        self.assertEqual(metrics.validation_score, 1.0)
        self.assertEqual(metrics.threshold_status, "normal")
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        metrics = StateMetrics(roi_value=5.0, sovereignty_index=0.9)
        data = metrics.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["roi_value"], 5.0)
        self.assertEqual(data["sovereignty_index"], 0.9)


class TestStateValidator(unittest.TestCase):
    """Test StateValidator class"""
    
    def test_valid_transitions(self):
        """Test valid state transitions"""
        validator = StateValidator()
        metrics = StateMetrics(validation_score=0.9, sovereignty_index=0.8)
        
        # INITIALIZED -> ACTIVE
        is_valid, msg = validator.validate_transition(
            SROIState.INITIALIZED, SROIState.ACTIVE, metrics
        )
        self.assertTrue(is_valid)
        
        # ACTIVE -> VALIDATING
        is_valid, msg = validator.validate_transition(
            SROIState.ACTIVE, SROIState.VALIDATING, metrics
        )
        self.assertTrue(is_valid)
    
    def test_invalid_transitions(self):
        """Test invalid state transitions"""
        validator = StateValidator()
        metrics = StateMetrics()
        
        # INITIALIZED -> COMPLETED (invalid)
        is_valid, msg = validator.validate_transition(
            SROIState.INITIALIZED, SROIState.COMPLETED, metrics
        )
        self.assertFalse(is_valid)
        self.assertIn("Invalid transition", msg)
        
        # COMPLETED -> ACTIVE (terminal state)
        is_valid, msg = validator.validate_transition(
            SROIState.COMPLETED, SROIState.ACTIVE, metrics
        )
        self.assertFalse(is_valid)
    
    def test_completion_validation(self):
        """Test validation for completion state"""
        validator = StateValidator()
        
        # Insufficient validation score
        metrics = StateMetrics(validation_score=0.5, sovereignty_index=0.9)
        is_valid, msg = validator.validate_transition(
            SROIState.VALIDATING, SROIState.COMPLETED, metrics
        )
        self.assertFalse(is_valid)
        self.assertIn("Validation score", msg)
        
        # Insufficient sovereignty index
        metrics = StateMetrics(validation_score=0.9, sovereignty_index=0.5)
        is_valid, msg = validator.validate_transition(
            SROIState.VALIDATING, SROIState.COMPLETED, metrics
        )
        self.assertFalse(is_valid)
        self.assertIn("Sovereignty index", msg)
        
        # Valid completion
        metrics = StateMetrics(validation_score=0.9, sovereignty_index=0.8)
        is_valid, msg = validator.validate_transition(
            SROIState.VALIDATING, SROIState.COMPLETED, metrics
        )
        self.assertTrue(is_valid)
    
    def test_critical_state_validation(self):
        """Test validation for critical state"""
        validator = StateValidator()
        
        # Cannot transition to CRITICAL with normal threshold
        metrics = StateMetrics(threshold_status="normal")
        is_valid, msg = validator.validate_transition(
            SROIState.ACTIVE, SROIState.CRITICAL, metrics
        )
        self.assertFalse(is_valid)
        self.assertIn("threshold violation", msg)
        
        # Can transition to CRITICAL with threshold violation
        metrics = StateMetrics(threshold_status="critical")
        is_valid, msg = validator.validate_transition(
            SROIState.ACTIVE, SROIState.CRITICAL, metrics
        )
        self.assertTrue(is_valid)
    
    def test_state_consistency(self):
        """Test state consistency validation"""
        validator = StateValidator()
        
        # Consistent state
        metrics = StateMetrics(validation_score=0.9, sovereignty_index=0.8)
        is_consistent, msg = validator.validate_state_consistency(
            SROIState.ACTIVE, metrics
        )
        self.assertTrue(is_consistent)
        
        # Inconsistent: negative sovereignty index
        metrics = StateMetrics(sovereignty_index=-0.5)
        is_consistent, msg = validator.validate_state_consistency(
            SROIState.ACTIVE, metrics
        )
        self.assertFalse(is_consistent)
        self.assertIn("negative", msg)
        
        # Inconsistent: validation score out of range
        metrics = StateMetrics(validation_score=1.5)
        is_consistent, msg = validator.validate_state_consistency(
            SROIState.ACTIVE, metrics
        )
        self.assertFalse(is_consistent)


class TestNotificationSystem(unittest.TestCase):
    """Test NotificationSystem class"""
    
    def setUp(self):
        """Set up test notification system"""
        import logging
        self.logger = logging.getLogger("test")
        self.notifier = NotificationSystem(self.logger)
    
    def test_threshold_checks(self):
        """Test threshold violation detection"""
        # No violations
        metrics = StateMetrics(roi_value=5.0, sovereignty_index=0.9, validation_score=0.9)
        violations = self.notifier.check_thresholds(metrics)
        self.assertEqual(len(violations), 0)
        
        # ROI critical violation
        metrics = StateMetrics(roi_value=-15.0)
        violations = self.notifier.check_thresholds(metrics)
        self.assertTrue(any("ROI" in v and "CRITICAL" in v for v in violations))
        
        # Sovereignty critical violation
        metrics = StateMetrics(sovereignty_index=0.4)
        violations = self.notifier.check_thresholds(metrics)
        self.assertTrue(any("Sovereignty" in v and "CRITICAL" in v for v in violations))
        
        # Validation score critical violation
        metrics = StateMetrics(validation_score=0.5)
        violations = self.notifier.check_thresholds(metrics)
        self.assertTrue(any("Validation" in v and "CRITICAL" in v for v in violations))
    
    def test_warning_thresholds(self):
        """Test warning threshold detection"""
        # ROI warning
        metrics = StateMetrics(roi_value=-5.0)
        violations = self.notifier.check_thresholds(metrics)
        self.assertTrue(any("ROI" in v and "WARNING" in v for v in violations))
        
        # Sovereignty warning
        metrics = StateMetrics(sovereignty_index=0.65)
        violations = self.notifier.check_thresholds(metrics)
        self.assertTrue(any("Sovereignty" in v and "WARNING" in v for v in violations))
    
    def test_notify(self):
        """Test notification creation"""
        self.notifier.notify("INFO", "Test message", {"key": "value"})
        
        notifications = self.notifier.get_notifications()
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["level"], "INFO")
        self.assertEqual(notifications[0]["message"], "Test message")
        self.assertEqual(notifications[0]["context"]["key"], "value")
    
    def test_filter_by_level(self):
        """Test notification filtering"""
        self.notifier.notify("INFO", "Info message")
        self.notifier.notify("WARNING", "Warning message")
        self.notifier.notify("CRITICAL", "Critical message")
        self.notifier.notify("INFO", "Another info")
        
        critical = self.notifier.get_notifications("CRITICAL")
        self.assertEqual(len(critical), 1)
        self.assertEqual(critical[0]["message"], "Critical message")
        
        info = self.notifier.get_notifications("INFO")
        self.assertEqual(len(info), 2)


class TestSROISovereignProtocol(unittest.TestCase):
    """Test main SROISovereignProtocol class"""
    
    def setUp(self):
        """Set up test protocol instance"""
        self.temp_dir = tempfile.mkdtemp()
        self.protocol = SROISovereignProtocol(
            operation_id="TEST-001",
            log_dir=self.temp_dir
        )
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test protocol initialization"""
        self.assertEqual(self.protocol.operation_id, "TEST-001")
        self.assertEqual(self.protocol.current_state, SROIState.INITIALIZED)
        self.assertIsInstance(self.protocol.metrics, StateMetrics)
        self.assertEqual(len(self.protocol.transition_history), 0)
    
    def test_basic_transition(self):
        """Test basic state transition"""
        success = self.protocol.transition_to(
            SROIState.ACTIVE,
            "Test activation"
        )
        
        self.assertTrue(success)
        self.assertEqual(self.protocol.current_state, SROIState.ACTIVE)
        self.assertEqual(len(self.protocol.transition_history), 1)
    
    def test_invalid_transition_rejected(self):
        """Test that invalid transitions are rejected"""
        # Try invalid transition INITIALIZED -> COMPLETED
        success = self.protocol.transition_to(
            SROIState.COMPLETED,
            "Invalid transition"
        )
        
        self.assertFalse(success)
        self.assertEqual(self.protocol.current_state, SROIState.INITIALIZED)
        self.assertEqual(len(self.protocol.transition_history), 0)
    
    def test_metric_updates(self):
        """Test metric update methods"""
        # Activate first
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        
        # Update ROI
        self.protocol.update_roi(10.0)
        self.assertEqual(self.protocol.metrics.roi_value, 10.0)
        
        # Update sovereignty
        self.protocol.update_sovereignty_index(0.85)
        self.assertEqual(self.protocol.metrics.sovereignty_index, 0.85)
        
        # Update validation score
        self.protocol.update_validation_score(0.9)
        self.assertEqual(self.protocol.metrics.validation_score, 0.9)
    
    def test_automatic_critical_transition(self):
        """Test automatic transition to CRITICAL on threshold violation"""
        # Activate protocol
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        initial_state = self.protocol.current_state
        
        # Update sovereignty below critical threshold
        self.protocol.update_sovereignty_index(0.3)
        
        # Should automatically transition to CRITICAL
        self.assertEqual(self.protocol.current_state, SROIState.CRITICAL)
        self.assertEqual(self.protocol.metrics.threshold_status, "critical")
    
    def test_full_lifecycle(self):
        """Test complete protocol lifecycle"""
        # 1. Activate
        self.protocol.transition_to(SROIState.ACTIVE, "Start operation")
        self.assertEqual(self.protocol.current_state, SROIState.ACTIVE)
        
        # 2. Update metrics
        self.protocol.update_roi(5.0)
        self.protocol.update_sovereignty_index(0.9)
        self.protocol.update_validation_score(0.95)
        
        # 3. Validate
        self.protocol.transition_to(SROIState.VALIDATING, "Validation check")
        self.assertEqual(self.protocol.current_state, SROIState.VALIDATING)
        
        # 4. Complete
        self.protocol.transition_to(SROIState.COMPLETED, "Operation complete")
        self.assertEqual(self.protocol.current_state, SROIState.COMPLETED)
        
        # Verify transition history (INITIALIZED->ACTIVE, ACTIVE->VALIDATING, VALIDATING->COMPLETED = 3 transitions)
        self.assertEqual(len(self.protocol.transition_history), 3)
    
    def test_status_report(self):
        """Test status report generation"""
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        self.protocol.update_roi(7.5)
        
        status = self.protocol.get_status()
        
        self.assertEqual(status["operation_id"], "TEST-001")
        self.assertEqual(status["current_state"], "active")
        self.assertEqual(status["metrics"]["roi_value"], 7.5)
        self.assertEqual(status["transition_count"], 1)
    
    def test_transition_history(self):
        """Test transition history tracking"""
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        self.protocol.transition_to(SROIState.VALIDATING, "Validation")
        
        history = self.protocol.get_transition_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["from_state"], "initialized")
        self.assertEqual(history[0]["to_state"], "active")
        self.assertEqual(history[1]["from_state"], "active")
        self.assertEqual(history[1]["to_state"], "validating")
    
    def test_log_export(self):
        """Test log export functionality"""
        # Create some activity
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        self.protocol.update_roi(5.0)
        
        # Export logs
        export_path = os.path.join(self.temp_dir, "export.json")
        self.protocol.export_logs(export_path)
        
        # Verify export file exists and contains data
        self.assertTrue(os.path.exists(export_path))
        
        with open(export_path, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data["operation_id"], "TEST-001")
        self.assertEqual(data["current_state"], "active")
        self.assertIn("transition_history", data)
        self.assertIn("notifications", data)
    
    def test_notifications_generated(self):
        """Test that notifications are generated correctly"""
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        
        # Trigger critical condition
        self.protocol.update_sovereignty_index(0.4)
        
        # Check notifications
        critical_notifications = self.protocol.notifier.get_notifications("CRITICAL")
        self.assertGreater(len(critical_notifications), 0)
    
    def test_state_handlers_executed(self):
        """Test that state handlers are executed"""
        # Each transition should execute a handler
        self.protocol.transition_to(SROIState.ACTIVE, "Activation")
        
        # Operation count should be incremented by ACTIVE handler
        self.assertGreater(self.protocol.metrics.operation_count, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up for integration tests"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_successful_operation_flow(self):
        """Test complete successful operation flow"""
        protocol = SROISovereignProtocol(
            operation_id="INTEGRATION-001",
            log_dir=self.temp_dir
        )
        
        # Execute successful flow
        protocol.transition_to(SROIState.ACTIVE, "Start")
        protocol.update_roi(10.0)
        protocol.update_sovereignty_index(0.95)
        protocol.update_validation_score(0.92)
        
        protocol.transition_to(SROIState.VALIDATING, "Validation")
        protocol.transition_to(SROIState.COMPLETED, "Success")
        
        # Verify final state
        self.assertEqual(protocol.current_state, SROIState.COMPLETED)
        # INIT->ACTIVE, ACTIVE->VALIDATING, VALIDATING->COMPLETED = 3 transitions
        self.assertEqual(len(protocol.transition_history), 3)
        
        # Verify metrics maintained
        self.assertEqual(protocol.metrics.roi_value, 10.0)
        self.assertEqual(protocol.metrics.sovereignty_index, 0.95)
    
    def test_critical_recovery_flow(self):
        """Test critical state detection and recovery"""
        protocol = SROISovereignProtocol(
            operation_id="INTEGRATION-002",
            log_dir=self.temp_dir
        )
        
        # Start operation
        protocol.transition_to(SROIState.ACTIVE, "Start")
        
        # Trigger critical condition
        protocol.update_sovereignty_index(0.3)
        self.assertEqual(protocol.current_state, SROIState.CRITICAL)
        
        # Recover
        protocol.update_sovereignty_index(0.9)
        protocol.metrics.threshold_status = "normal"
        protocol.transition_to(SROIState.ACTIVE, "Recovery")
        
        # Complete successfully
        protocol.update_validation_score(0.95)
        protocol.transition_to(SROIState.VALIDATING, "Final validation")
        protocol.transition_to(SROIState.COMPLETED, "Complete")
        
        # Verify recovery succeeded
        self.assertEqual(protocol.current_state, SROIState.COMPLETED)
        
        # Verify critical notifications were generated
        critical = protocol.notifier.get_notifications("CRITICAL")
        self.assertGreater(len(critical), 0)
    
    def test_failure_flow(self):
        """Test operation failure flow"""
        protocol = SROISovereignProtocol(
            operation_id="INTEGRATION-003",
            log_dir=self.temp_dir
        )
        
        # Start and fail
        protocol.transition_to(SROIState.ACTIVE, "Start")
        protocol.update_roi(-50.0)  # Severe ROI problem
        protocol.transition_to(SROIState.FAILED, "Unrecoverable error")
        
        # Verify terminal state
        self.assertEqual(protocol.current_state, SROIState.FAILED)
        
        # Cannot transition from FAILED
        success = protocol.transition_to(SROIState.ACTIVE, "Try to restart")
        self.assertFalse(success)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("S-ROI SOVEREIGN PROTOCOL - UNIT TESTS")
    print("="*70 + "\n")
    
    # Run tests
    unittest.main(verbosity=2)
