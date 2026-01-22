"""
test_resonance_and_stealth.py
Test suite for enhanced S-ROI Sovereign Protocol (Stealth Mode + Resonance Tracking)

Tests:
- Resonance tracking and state changes
- WARNING state for near-threshold values
- Cooldown mechanism for stealth activation
- State change logging
- Integration between resonance and stealth systems
"""

import sys
import os
import time

# Ensure the parent directory is in the path
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.resonance_tracker import ResonanceTracker, ResonanceState, ResonanceReading, StateChangeLog
from core.stealth_mode import StealthMode, StealthLevel


class TestResonanceTracker:
    """Tests for Resonance Tracker"""
    
    def test_resonance_recording(self):
        """Test basic resonance recording"""
        tracker = ResonanceTracker()
        
        state = tracker.record_resonance(0.65, source="test")
        
        assert tracker.current_resonance == 0.65
        assert state == ResonanceState.NORMAL
        assert len(tracker.resonance_history) == 1
        
        print("✅ test_resonance_recording passed")
    
    def test_state_transitions(self):
        """Test resonance state transitions"""
        tracker = ResonanceTracker(
            warning_threshold=0.75,
            critical_threshold=0.9,
            stable_threshold=0.95
        )
        
        # NORMAL state
        state = tracker.record_resonance(0.5, source="normal")
        assert state == ResonanceState.NORMAL
        
        # WARNING state
        state = tracker.record_resonance(0.76, source="warning")
        assert state == ResonanceState.WARNING
        assert len(tracker.state_change_log) == 1
        
        # CRITICAL state
        state = tracker.record_resonance(0.91, source="critical")
        assert state == ResonanceState.CRITICAL
        assert len(tracker.state_change_log) == 2
        
        # STABLE state
        state = tracker.record_resonance(0.96, source="stable")
        assert state == ResonanceState.STABLE
        assert len(tracker.state_change_log) == 3
        
        print("✅ test_state_transitions passed")
    
    def test_warning_zone_detection(self):
        """Test WARNING zone detection"""
        tracker = ResonanceTracker(warning_threshold=0.75, critical_threshold=0.9)
        
        # Below warning
        tracker.record_resonance(0.7, source="test")
        assert not tracker.is_in_warning_zone()
        
        # In warning zone
        tracker.record_resonance(0.8, source="test")
        assert tracker.is_in_warning_zone()
        assert not tracker.is_critical()
        
        # Above warning zone (critical)
        tracker.record_resonance(0.95, source="test")
        assert not tracker.is_in_warning_zone()
        assert tracker.is_critical()
        
        print("✅ test_warning_zone_detection passed")
    
    def test_state_change_logging(self):
        """Test state change logging"""
        tracker = ResonanceTracker()
        
        # Record values to trigger state changes
        tracker.record_resonance(0.5, source="initial")
        tracker.record_resonance(0.8, source="increase")  # NORMAL -> WARNING
        tracker.record_resonance(0.95, source="peak")     # WARNING -> STABLE
        
        # Check log entries
        assert len(tracker.state_change_log) == 2
        
        # Verify log structure
        first_change = tracker.state_change_log[0]
        assert first_change.previous_state == "NORMAL"
        assert first_change.new_state == "WARNING"
        assert first_change.trigger == "increase"
        
        print("✅ test_state_change_logging passed")
    
    def test_resonance_statistics(self):
        """Test statistics calculation"""
        tracker = ResonanceTracker()
        
        # Record several values
        values = [0.5, 0.6, 0.7, 0.8, 0.9]
        for val in values:
            tracker.record_resonance(val, source="test")
        
        stats = tracker.get_statistics()
        
        assert stats["total_readings"] == 5
        assert stats["min_resonance"] == 0.5
        assert stats["max_resonance"] == 0.9
        assert 0.6 < stats["average_resonance"] < 0.8
        
        print("✅ test_resonance_statistics passed")
    
    def test_average_resonance_calculation(self):
        """Test average resonance over time window"""
        tracker = ResonanceTracker()
        
        # Record some values
        tracker.record_resonance(0.5, source="test")
        tracker.record_resonance(0.7, source="test")
        tracker.record_resonance(0.9, source="test")
        
        avg = tracker.calculate_average_resonance()
        
        assert avg is not None
        assert 0.6 < avg < 0.8
        
        print(f"✅ test_average_resonance_calculation passed (avg: {avg:.2f})")
    
    def test_history_trimming(self):
        """Test that history is trimmed at max size"""
        tracker = ResonanceTracker()
        tracker.max_history_size = 10
        
        # Record more than max
        for i in range(15):
            tracker.record_resonance(0.5 + i * 0.01, source="test")
        
        # Should be trimmed to max
        assert len(tracker.resonance_history) == 10
        
        print("✅ test_history_trimming passed")
    
    def test_log_export(self):
        """Test exporting logs to file"""
        import tempfile
        import json
        
        tracker = ResonanceTracker()
        tracker.record_resonance(0.8, source="test")
        
        # Export to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            tracker.export_logs(filepath)
            
            # Verify file was created and is valid JSON
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert "export_timestamp" in data
            assert "current_status" in data
            assert "statistics" in data
            
            print("✅ test_log_export passed")
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)


class TestStealthModeCooldown:
    """Tests for Stealth Mode cooldown mechanism"""
    
    def test_cooldown_initialization(self):
        """Test cooldown is initialized correctly"""
        stealth = StealthMode(stealth_cooldown_seconds=30.0)
        
        assert stealth.stealth_cooldown_seconds == 30.0
        assert stealth.last_stealth_activation is None
        
        print("✅ test_cooldown_initialization passed")
    
    def test_first_activation_allowed(self):
        """Test that first activation is always allowed"""
        stealth = StealthMode(stealth_cooldown_seconds=60.0)
        
        can_activate, reason = stealth.can_activate_stealth()
        
        assert can_activate is True
        assert "No previous activation" in reason
        
        print("✅ test_first_activation_allowed passed")
    
    def test_cooldown_blocks_activation(self):
        """Test that cooldown blocks rapid re-activation"""
        stealth = StealthMode(stealth_cooldown_seconds=10.0)
        
        # First activation
        stealth.activate_full_stealth()
        
        # Immediate attempt should be blocked
        can_activate, reason = stealth.can_activate_stealth()
        
        assert can_activate is False
        assert "Cooldown active" in reason
        
        print("✅ test_cooldown_blocks_activation passed")
    
    def test_cooldown_expires(self):
        """Test that cooldown expires after time period"""
        stealth = StealthMode(stealth_cooldown_seconds=1.0)  # 1 second for testing
        
        # First activation
        stealth.activate_full_stealth()
        
        # Wait for cooldown to expire
        time.sleep(1.5)
        
        # Should be allowed now
        can_activate, reason = stealth.can_activate_stealth()
        
        assert can_activate is True
        assert "Cooldown expired" in reason
        
        print("✅ test_cooldown_expires passed")
    
    def test_force_activation_bypasses_cooldown(self):
        """Test that force=True bypasses cooldown"""
        stealth = StealthMode(stealth_cooldown_seconds=60.0)
        
        # First activation
        stealth.activate_full_stealth()
        
        # Deactivate
        stealth.deactivate_stealth()
        
        # Force activation should work immediately
        stealth.activate_full_stealth(force=True)
        
        assert stealth.stealth_level == StealthLevel.INVISIBLE
        
        print("✅ test_force_activation_bypasses_cooldown passed")
    
    def test_cooldown_info_in_status(self):
        """Test that cooldown info is included in status"""
        stealth = StealthMode(stealth_cooldown_seconds=30.0)
        
        # Activate stealth
        stealth.activate_full_stealth()
        
        status = stealth.get_stealth_status()
        
        assert "cooldown" in status
        cooldown_info = status["cooldown"]
        
        assert "last_activation" in cooldown_info
        assert "cooldown_active" in cooldown_info
        assert "cooldown_remaining_seconds" in cooldown_info
        assert cooldown_info["cooldown_active"] is True
        
        print("✅ test_cooldown_info_in_status passed")


class TestStealthModeResonanceIntegration:
    """Tests for integration between Stealth Mode and Resonance Tracking"""
    
    def test_resonance_tracker_initialized(self):
        """Test that resonance tracker is initialized with stealth mode"""
        stealth = StealthMode()
        
        assert stealth.resonance_tracker is not None
        assert isinstance(stealth.resonance_tracker, ResonanceTracker)
        
        print("✅ test_resonance_tracker_initialized passed")
    
    def test_stealth_activation_records_resonance(self):
        """Test that stealth activation records resonance"""
        stealth = StealthMode()
        
        initial_count = len(stealth.resonance_tracker.resonance_history)
        
        stealth.activate_full_stealth()
        
        # Should have recorded resonance
        assert len(stealth.resonance_tracker.resonance_history) > initial_count
        
        # Should be high resonance
        current = stealth.resonance_tracker.current_resonance
        assert current is not None
        assert current > 0.9
        
        print("✅ test_stealth_activation_records_resonance passed")
    
    def test_ponte_amoris_operations_record_resonance(self):
        """Test that Ponte Amoris operations record resonance"""
        stealth = StealthMode()
        
        initial_count = len(stealth.resonance_tracker.resonance_history)
        
        # Close Ponte Amoris
        stealth.close_ponte_amoris()
        
        assert len(stealth.resonance_tracker.resonance_history) > initial_count
        
        # Open Ponte Amoris
        stealth.open_ponte_amoris()
        
        assert len(stealth.resonance_tracker.resonance_history) > initial_count + 1
        
        print("✅ test_ponte_amoris_operations_record_resonance passed")
    
    def test_resonance_status_in_stealth_status(self):
        """Test that resonance info is included in stealth status"""
        stealth = StealthMode()
        
        # Record some resonance
        stealth.resonance_tracker.record_resonance(0.8, source="test")
        
        status = stealth.get_stealth_status()
        
        assert "resonance_status" in status
        assert "resonance_statistics" in status
        
        res_status = status["resonance_status"]
        assert "current_resonance" in res_status
        assert "current_state" in res_status
        
        print("✅ test_resonance_status_in_stealth_status passed")
    
    def test_update_stealth_level_from_resonance(self):
        """Test automatic stealth level adjustment from resonance"""
        stealth = StealthMode()
        
        # Set WARNING resonance
        stealth.resonance_tracker.record_resonance(0.78, source="test")
        
        # Update stealth level
        stealth.update_stealth_level_from_resonance()
        
        # Should be in WARNING state
        assert stealth.stealth_level == StealthLevel.WARNING
        
        print("✅ test_update_stealth_level_from_resonance passed")
    
    def test_warning_stealth_level_exists(self):
        """Test that WARNING stealth level exists"""
        # Verify enum has WARNING level
        assert hasattr(StealthLevel, 'WARNING')
        assert StealthLevel.WARNING.value == "WARNING"
        
        print("✅ test_warning_stealth_level_exists passed")


class TestStealthModeStateChangeLogging:
    """Tests for state change logging"""
    
    def test_state_changes_logged(self):
        """Test that stealth state changes are logged via resonance"""
        stealth = StealthMode()
        
        initial_log_size = len(stealth.resonance_tracker.state_change_log)
        
        # Activate stealth (should record high resonance -> state change)
        stealth.activate_full_stealth()
        
        # Deactivate stealth (should record low resonance -> state change)
        stealth.deactivate_stealth()
        
        # Should have logged state changes
        assert len(stealth.resonance_tracker.state_change_log) > initial_log_size
        
        print("✅ test_state_changes_logged passed")
    
    def test_get_state_change_history(self):
        """Test retrieving state change history"""
        stealth = StealthMode()
        
        # Trigger some state changes
        stealth.resonance_tracker.record_resonance(0.5, source="low")
        stealth.resonance_tracker.record_resonance(0.8, source="medium")
        stealth.resonance_tracker.record_resonance(0.96, source="high")
        
        history = stealth.resonance_tracker.get_state_change_history(10)
        
        assert isinstance(history, list)
        assert len(history) > 0
        
        # Verify structure
        for entry in history:
            assert "previous_state" in entry
            assert "new_state" in entry
            assert "resonance_value" in entry
            assert "trigger" in entry
        
        print("✅ test_get_state_change_history passed")


def run_all_tests():
    """Run all tests for enhanced S-ROI Sovereign Protocol"""
    print("\n" + "=" * 70)
    print("🧪 Running Enhanced S-ROI Sovereign Protocol Test Suite")
    print("=" * 70)
    
    # Resonance Tracker tests
    print("\n📊 Resonance Tracker Tests:")
    print("-" * 50)
    rt_tests = TestResonanceTracker()
    rt_tests.test_resonance_recording()
    rt_tests.test_state_transitions()
    rt_tests.test_warning_zone_detection()
    rt_tests.test_state_change_logging()
    rt_tests.test_resonance_statistics()
    rt_tests.test_average_resonance_calculation()
    rt_tests.test_history_trimming()
    rt_tests.test_log_export()
    
    # Stealth Mode Cooldown tests
    print("\n⏱️  Stealth Mode Cooldown Tests:")
    print("-" * 50)
    cd_tests = TestStealthModeCooldown()
    cd_tests.test_cooldown_initialization()
    cd_tests.test_first_activation_allowed()
    cd_tests.test_cooldown_blocks_activation()
    cd_tests.test_cooldown_expires()
    cd_tests.test_force_activation_bypasses_cooldown()
    cd_tests.test_cooldown_info_in_status()
    
    # Integration tests
    print("\n🔗 Stealth Mode & Resonance Integration Tests:")
    print("-" * 50)
    int_tests = TestStealthModeResonanceIntegration()
    int_tests.test_resonance_tracker_initialized()
    int_tests.test_stealth_activation_records_resonance()
    int_tests.test_ponte_amoris_operations_record_resonance()
    int_tests.test_resonance_status_in_stealth_status()
    int_tests.test_update_stealth_level_from_resonance()
    int_tests.test_warning_stealth_level_exists()
    
    # State change logging tests
    print("\n📝 State Change Logging Tests:")
    print("-" * 50)
    log_tests = TestStealthModeStateChangeLogging()
    log_tests.test_state_changes_logged()
    log_tests.test_get_state_change_history()
    
    print("\n" + "=" * 70)
    print("✅ All Enhanced S-ROI Sovereign Protocol tests passed!")
    print("=" * 70)
    print("\nImplemented Features:")
    print("  ✓ Resonance tracking with state management")
    print("  ✓ WARNING state for near-threshold values")
    print("  ✓ Cooldown mechanism for stealth activation")
    print("  ✓ Comprehensive state change logging")
    print("  ✓ Modular code structure")
    print("  ✓ Full integration between components")
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
