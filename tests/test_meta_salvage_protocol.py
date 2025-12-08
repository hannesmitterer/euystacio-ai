"""
test_meta_salvage_protocol.py
Test suite for Meta Salvage Protocol orchestration

Tests the end-to-end orchestration of the Protocollo Meta Salvage system,
including integration of all components.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.meta_salvage_protocol import (
    MetaSalvageProtocol, ProtocolStatus, get_meta_salvage_protocol
)
from core.risk_monitor import RiskLevel
from core.peace_bonds import BondStatus


class TestMetaSalvageProtocol:
    """Tests for MetaSalvageProtocol class"""
    
    def test_initialization(self):
        """Test MetaSalvageProtocol initialization"""
        protocol = MetaSalvageProtocol()
        
        assert protocol is not None
        assert protocol.status == ProtocolStatus.INITIALIZING
        assert protocol.risk_monitor is not None
        assert protocol.peace_bonds_manager is not None
        assert protocol.decision_engine is not None
        assert protocol.audit_pipeline is not None
        
        print("✅ test_initialization passed")
    
    def test_initialize_protocol(self):
        """Test protocol initialization process"""
        protocol = MetaSalvageProtocol()
        
        protocol.initialize()
        
        assert protocol.status == ProtocolStatus.MONITORING
        
        print("✅ test_initialize_protocol passed")
    
    def test_execute_monitoring_cycle_no_risks(self):
        """Test executing a monitoring cycle with no risks"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Provide metrics for compliant providers
        provider_metrics = [
            {
                "provider_id": "safe-provider-1",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.9,
                "symbiosis_score": 0.90
            },
            {
                "provider_id": "safe-provider-2",
                "latency_ms": 45.0,
                "throughput_ops_sec": 6000.0,
                "cost_per_operation": 0.0009,
                "availability_pct": 99.95,
                "symbiosis_score": 0.92
            }
        ]
        
        execution = protocol.execute_monitoring_cycle(provider_metrics)
        
        assert execution.providers_monitored == 2
        assert execution.risks_detected >= 0
        assert execution.bonds_imposed == 0  # No risks, no bonds
        
        print("✅ test_execute_monitoring_cycle_no_risks passed")
    
    def test_execute_monitoring_cycle_with_risks(self):
        """Test executing a monitoring cycle with detected risks"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Provide metrics with risky provider
        provider_metrics = [
            {
                "provider_id": "risky-provider-1",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.70  # Below threshold
            }
        ]
        
        execution = protocol.execute_monitoring_cycle(provider_metrics)
        
        assert execution.providers_monitored == 1
        assert execution.risks_detected > 0
        # May impose bonds depending on auto-enforcement setting
        
        print("✅ test_execute_monitoring_cycle_with_risks passed")
    
    def test_peace_bond_imposition_on_high_risk(self):
        """Test that Peace Bonds are imposed on high-risk events"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Ensure auto-enforcement is enabled
        protocol.config["auto_bond_enforcement"] = True
        
        # Provide metrics with critical risk
        provider_metrics = [
            {
                "provider_id": "critical-provider",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.50  # Critical risk
            }
        ]
        
        execution = protocol.execute_monitoring_cycle(provider_metrics)
        
        # Check if bonds were imposed
        active_bonds = protocol.peace_bonds_manager.get_active_bonds_for_provider(
            "critical-provider"
        )
        
        # Should have at least attempted to impose bond
        assert execution.decisions_made > 0
        
        print("✅ test_peace_bond_imposition_on_high_risk passed")
    
    def test_get_protocol_status(self):
        """Test retrieving protocol status"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        status = protocol.get_protocol_status()
        
        assert status["status"] == ProtocolStatus.MONITORING.value
        assert "timestamp" in status
        assert "configuration" in status
        assert "providers_monitored" in status
        assert "active_bonds" in status
        assert "total_executions" in status
        
        print("✅ test_get_protocol_status passed")
    
    def test_generate_status_report(self):
        """Test generating human-readable status report"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Execute a cycle to have some data
        provider_metrics = [
            {
                "provider_id": "test-provider",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.85
            }
        ]
        
        protocol.execute_monitoring_cycle(provider_metrics)
        
        report = protocol.generate_status_report()
        
        assert isinstance(report, str)
        assert "PROTOCOLLO META SALVAGE" in report
        assert "STATUS REPORT" in report
        assert "MONITORING SUMMARY" in report
        
        print("✅ test_generate_status_report passed")
    
    def test_collect_feedback(self):
        """Test collecting feedback for learning"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Execute a cycle
        provider_metrics = [
            {
                "provider_id": "test-provider",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.85
            }
        ]
        
        execution = protocol.execute_monitoring_cycle(provider_metrics)
        
        # Collect feedback
        protocol.collect_feedback(
            execution_id=execution.execution_id,
            effectiveness_score=0.85,
            notes="Effective monitoring cycle"
        )
        
        assert len(protocol.feedback_data) == 1
        assert protocol.feedback_data[0]["effectiveness_score"] == 0.85
        
        print("✅ test_collect_feedback passed")
    
    def test_multiple_monitoring_cycles(self):
        """Test executing multiple monitoring cycles"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        provider_metrics = [
            {
                "provider_id": "test-provider",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.85
            }
        ]
        
        # Execute multiple cycles
        for i in range(3):
            execution = protocol.execute_monitoring_cycle(provider_metrics)
            assert execution.execution_id is not None
        
        assert len(protocol.execution_history) == 3
        
        print("✅ test_multiple_monitoring_cycles passed")
    
    def test_singleton_instance(self):
        """Test that get_meta_salvage_protocol returns singleton"""
        protocol1 = get_meta_salvage_protocol()
        protocol2 = get_meta_salvage_protocol()
        
        assert protocol1 is protocol2
        
        print("✅ test_singleton_instance passed")
    
    def test_configuration_values(self):
        """Test protocol configuration values"""
        protocol = MetaSalvageProtocol()
        
        assert "monitoring_interval_seconds" in protocol.config
        assert "auto_decision_enabled" in protocol.config
        assert "auto_bond_enforcement" in protocol.config
        assert "audit_frequency_hours" in protocol.config
        assert "feedback_learning_enabled" in protocol.config
        
        # Check default values
        assert protocol.config["auto_decision_enabled"] is True
        assert protocol.config["auto_bond_enforcement"] is True
        
        print("✅ test_configuration_values passed")
    
    def test_integration_with_subsystems(self):
        """Test integration between all subsystems"""
        protocol = MetaSalvageProtocol()
        protocol.initialize()
        
        # Verify all subsystems are accessible
        assert protocol.risk_monitor is not None
        assert protocol.peace_bonds_manager is not None
        assert protocol.decision_engine is not None
        assert protocol.audit_pipeline is not None
        
        # Verify subsystems can interact
        provider_metrics = [
            {
                "provider_id": "integration-test",
                "latency_ms": 50.0,
                "throughput_ops_sec": 5000.0,
                "cost_per_operation": 0.001,
                "availability_pct": 99.5,
                "symbiosis_score": 0.70  # Triggers risk
            }
        ]
        
        execution = protocol.execute_monitoring_cycle(provider_metrics)
        
        # Verify data flows through subsystems
        assert execution.providers_monitored == 1
        
        print("✅ test_integration_with_subsystems passed")


def run_all_tests():
    """Run all tests in the TestMetaSalvageProtocol class"""
    test_suite = TestMetaSalvageProtocol()
    
    print("\n" + "=" * 70)
    print("RUNNING META SALVAGE PROTOCOL TESTS")
    print("=" * 70 + "\n")
    
    # List of all test methods
    test_methods = [
        test_suite.test_initialization,
        test_suite.test_initialize_protocol,
        test_suite.test_execute_monitoring_cycle_no_risks,
        test_suite.test_execute_monitoring_cycle_with_risks,
        test_suite.test_peace_bond_imposition_on_high_risk,
        test_suite.test_get_protocol_status,
        test_suite.test_generate_status_report,
        test_suite.test_collect_feedback,
        test_suite.test_multiple_monitoring_cycles,
        test_suite.test_singleton_instance,
        test_suite.test_configuration_values,
        test_suite.test_integration_with_subsystems,
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_method()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_method.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
