"""
test_operational_components.py
Test suite for Euystacio AI Operational Components

Tests:
- Threshold Monitor (QEK, H-VAR metrics)
- Governance Compliance Manager
- IPFS Integrity Manager
- Coronation Simulator
"""

import sys
import os

# Ensure the parent directory is in the path for proper imports
# This is necessary when running the test file directly
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.threshold_monitor import (
    ThresholdMonitor, MetricType, AlertLevel, MetricSnapshot, Alert, DriftPrediction
)
from core.governance_compliance import (
    GovernanceComplianceManager, SignatureStatus, QuorumStatus, ReminderType
)
from core.ipfs_integrity import (
    IPFSIntegrityManager, SyncStatus, IntegrityStatus
)
from core.coronation_simulator import (
    CoronationSimulator, SimulationMode, LoadLevel, SimulationStatus
)


class TestThresholdMonitor:
    """Tests for Threshold Monitor"""
    
    def test_record_metric_qek(self):
        """Test recording QEK metrics"""
        monitor = ThresholdMonitor()
        
        snapshot = monitor.record_metric(MetricType.QEK, 0.95)
        
        assert snapshot.metric_type == MetricType.QEK
        assert snapshot.value == 0.95
        assert snapshot.within_limits is True
        assert 0 <= snapshot.deviation_pct <= 100
        
        print("✅ test_record_metric_qek passed")
    
    def test_record_metric_hvar(self):
        """Test recording H-VAR metrics"""
        monitor = ThresholdMonitor()
        
        snapshot = monitor.record_metric(MetricType.H_VAR, 0.05)
        
        assert snapshot.metric_type == MetricType.H_VAR
        assert snapshot.value == 0.05
        assert snapshot.within_limits is True
        
        print("✅ test_record_metric_hvar passed")
    
    def test_threshold_alert_generation(self):
        """Test that alerts are generated for threshold breaches"""
        monitor = ThresholdMonitor()
        
        # Record a value below QEK minimum (0.85)
        monitor.record_metric(MetricType.QEK, 0.80)
        
        # Should have generated an alert
        assert len(monitor.alerts) > 0
        assert monitor.alerts[-1].level in [AlertLevel.WARNING, AlertLevel.CRITICAL]
        
        print("✅ test_threshold_alert_generation passed")
    
    def test_drift_prediction(self):
        """Test drift prediction functionality"""
        monitor = ThresholdMonitor()
        
        # Generate enough data points
        for i in range(20):
            monitor.record_metric(MetricType.QEK, 0.93 + (i * 0.001))
        
        prediction = monitor.predict_drift(MetricType.QEK)
        
        assert prediction is not None
        assert isinstance(prediction, DriftPrediction)
        assert prediction.current_trend in ["stable", "drifting_up", "drifting_down"]
        assert 0 <= prediction.confidence <= 1
        
        print(f"✅ test_drift_prediction passed (trend: {prediction.current_trend})")
    
    def test_ethisches_ideal_check(self):
        """Test Ethisches Ideal limits check"""
        monitor = ThresholdMonitor()
        
        # Record some values
        monitor.record_metric(MetricType.QEK, 0.94)
        monitor.record_metric(MetricType.H_VAR, 0.04)
        monitor.record_metric(MetricType.ETHISCHES_IDEAL, 0.99)
        
        result = monitor.check_ethisches_ideal_limits()
        
        assert "overall_compliant" in result
        assert "metrics" in result
        assert MetricType.QEK.value in result["metrics"]
        assert MetricType.H_VAR.value in result["metrics"]
        
        print("✅ test_ethisches_ideal_check passed")
    
    def test_dashboard_data(self):
        """Test dashboard data generation"""
        monitor = ThresholdMonitor()
        
        # Record multiple values
        for _ in range(10):
            monitor.record_metric(MetricType.QEK, 0.93)
            monitor.record_metric(MetricType.H_VAR, 0.04)
        
        data = monitor.get_monitoring_dashboard_data()
        
        assert "timestamp" in data
        assert "metrics" in data
        assert "ethisches_status" in data
        
        print("✅ test_dashboard_data passed")


class TestGovernanceCompliance:
    """Tests for Governance Compliance Manager"""
    
    def test_default_council_initialization(self):
        """Test that default council members are initialized"""
        manager = GovernanceComplianceManager()
        
        assert len(manager.council_members) >= 5
        assert "C001" in manager.council_members
        
        print("✅ test_default_council_initialization passed")
    
    def test_submit_signature(self):
        """Test signature submission"""
        manager = GovernanceComplianceManager()
        
        success, message = manager.submit_signature(
            "C001", 
            "I approve the Coronation Day protocol",
            "GPG_SIGNATURE_12345"
        )
        
        assert success is True
        assert manager.council_members["C001"].signature_status in [
            SignatureStatus.SUBMITTED, SignatureStatus.VERIFIED
        ]
        
        print("✅ test_submit_signature passed")
    
    def test_quorum_check(self):
        """Test quorum checking"""
        manager = GovernanceComplianceManager()
        
        quorum = manager.check_quorum()
        
        assert "status" in quorum
        assert "total_members" in quorum
        assert "verified_count" in quorum
        assert "quorum_met" in quorum
        
        print("✅ test_quorum_check passed")
    
    def test_generate_reminders(self):
        """Test reminder generation"""
        manager = GovernanceComplianceManager()
        
        reminders = manager.generate_reminders()
        
        assert len(reminders) > 0
        assert all(r.reminder_type in ReminderType for r in reminders)
        
        print(f"✅ test_generate_reminders passed ({len(reminders)} reminders)")
    
    def test_saul_log_integrity(self):
        """Test SAUL log chain integrity"""
        manager = GovernanceComplianceManager()
        
        # Perform some actions to generate SAUL entries
        manager.submit_signature("C001", "Test signature", "GPG_SIG")
        manager.submit_signature("C002", "Test signature 2", "GPG_SIG_2")
        
        integrity = manager._verify_saul_integrity()
        
        assert "valid" in integrity
        assert "entries" in integrity
        assert integrity["valid"] is True
        
        print("✅ test_saul_log_integrity passed")
    
    def test_compliance_check(self):
        """Test real-time compliance check"""
        manager = GovernanceComplianceManager()
        
        compliance = manager.run_real_time_compliance_check()
        
        assert "check_id" in compliance
        assert "quorum_status" in compliance
        assert "saul_integrity" in compliance
        assert "overall_compliance" in compliance
        
        print("✅ test_compliance_check passed")


class TestIPFSIntegrity:
    """Tests for IPFS Integrity Manager"""
    
    def test_default_nodes_initialization(self):
        """Test that default IPFS nodes are initialized"""
        manager = IPFSIntegrityManager()
        
        assert len(manager.nodes) >= 3
        
        # Check for primary node
        primary_nodes = [n for n in manager.nodes.values() if n.is_primary]
        assert len(primary_nodes) >= 1
        
        print("✅ test_default_nodes_initialization passed")
    
    def test_add_content(self):
        """Test adding content to IPFS"""
        manager = IPFSIntegrityManager()
        
        content = manager.add_content(
            b"Test content for IPFS",
            "text/plain",
            {"test": True}
        )
        
        assert content.cid.startswith("Qm")
        assert content.size_bytes == len(b"Test content for IPFS")
        assert len(content.pinned_nodes) > 0
        
        print("✅ test_add_content passed")
    
    def test_sync_nodes(self):
        """Test node synchronization"""
        manager = IPFSIntegrityManager()
        
        result = manager.sync_nodes()
        
        assert "nodes_synced" in result
        assert "nodes_failed" in result
        assert result["nodes_synced"] > 0
        
        print(f"✅ test_sync_nodes passed ({result['nodes_synced']} synced)")
    
    def test_content_integrity_verification(self):
        """Test content integrity verification"""
        manager = IPFSIntegrityManager()
        
        # Add content
        content = manager.add_content(b"Integrity test content", "text/plain")
        
        # Sync nodes
        manager.sync_nodes()
        
        # Verify integrity
        audit = manager.verify_content_integrity(content.cid)
        
        assert audit.ipfs_status == IntegrityStatus.VALID
        assert audit.saul_status == IntegrityStatus.VALID
        assert audit.cross_verification is True
        
        print("✅ test_content_integrity_verification passed")
    
    def test_seedbringer_redundancy(self):
        """Test Seedbringer redundancy status"""
        manager = IPFSIntegrityManager()
        
        # Add and sync content
        manager.add_content(b"Seedbringer data", "application/octet-stream")
        manager.sync_nodes()
        
        status = manager.get_seedbringer_redundancy_status()
        
        assert "seedbringer_status" in status
        assert "replication_factor" in status
        assert status["replication_factor"] > 0
        
        print("✅ test_seedbringer_redundancy passed")
    
    def test_api_status(self):
        """Test API status reporting"""
        manager = IPFSIntegrityManager()
        
        status = manager.get_api_status()
        
        assert status["status"] == "OPERATIONAL"
        assert "endpoints" in status
        assert "ipfs_gateway" in status["endpoints"]
        assert "saul_integration" in status["endpoints"]
        
        print("✅ test_api_status passed")


class TestCoronationSimulator:
    """Tests for Coronation Simulator"""
    
    def test_default_scenarios_initialization(self):
        """Test that default scenarios are initialized"""
        simulator = CoronationSimulator()
        
        assert len(simulator.scenarios) >= 5
        assert "SCEN-001" in simulator.scenarios
        
        print("✅ test_default_scenarios_initialization passed")
    
    def test_run_simulation(self):
        """Test running a simulation"""
        simulator = CoronationSimulator()
        
        result = simulator.run_simulation("SCEN-001")
        
        assert result.status == SimulationStatus.COMPLETED
        assert result.scenario_id == "SCEN-001"
        assert "response_time" in result.metrics_summary
        
        print("✅ test_run_simulation passed")
    
    def test_metrics_collection(self):
        """Test that metrics are collected during simulation"""
        simulator = CoronationSimulator()
        
        simulator.run_simulation("SCEN-001")
        
        assert len(simulator.metrics_history) > 0
        
        metrics = simulator.metrics_history[-1]
        assert metrics.response_time_ms > 0
        assert 0 <= metrics.cpu_utilization <= 1
        
        print("✅ test_metrics_collection passed")
    
    def test_threshold_checking(self):
        """Test threshold checking in simulation"""
        simulator = CoronationSimulator()
        
        result = simulator.run_simulation("SCEN-001")
        
        assert "passed_thresholds" in result.to_dict()
        # Baseline test should typically pass
        
        print(f"✅ test_threshold_checking passed (passed: {result.passed_thresholds})")
    
    def test_capacity_planning(self):
        """Test capacity planning generation"""
        simulator = CoronationSimulator()
        
        # Run a simulation first
        simulator.run_simulation("SCEN-001")
        
        capacity = simulator.get_capacity_planning()
        
        assert "recommended_capacity" in capacity
        assert "scaling_strategy" in capacity
        assert "coronation_workshop_target" in capacity
        
        print("✅ test_capacity_planning passed")
    
    def test_stress_test_bottleneck_detection(self):
        """Test that bottlenecks are detected in stress tests"""
        simulator = CoronationSimulator()
        
        # Run extreme load test
        result = simulator.run_simulation("SCEN-005")
        
        # Extreme test should likely find some bottlenecks
        assert isinstance(result.bottlenecks, list)
        assert len(result.recommendations) > 0
        
        print(f"✅ test_stress_test_bottleneck_detection passed ({len(result.bottlenecks)} bottlenecks)")
    
    def test_markdown_report_generation(self):
        """Test Markdown report generation"""
        simulator = CoronationSimulator()
        
        # Run some simulations
        simulator.run_simulation("SCEN-001")
        simulator.run_simulation("SCEN-002")
        
        report = simulator.generate_markdown_report()
        
        assert "Coronation Workshop Simulation Report" in report
        assert "Executive Summary" in report
        assert "Performance Thresholds" in report
        
        print("✅ test_markdown_report_generation passed")
    
    def test_dashboard_data(self):
        """Test dashboard data generation"""
        simulator = CoronationSimulator()
        
        simulator.run_simulation("SCEN-001")
        
        data = simulator.get_dashboard_data()
        
        assert "scenarios" in data
        assert "recent_results" in data
        assert "capacity_planning" in data
        assert "thresholds" in data
        
        print("✅ test_dashboard_data passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Running Euystacio Operational Components Test Suite")
    print("=" * 60)
    
    # Threshold Monitor tests
    print("\n📊 Threshold Monitor Tests:")
    print("-" * 40)
    tm_tests = TestThresholdMonitor()
    tm_tests.test_record_metric_qek()
    tm_tests.test_record_metric_hvar()
    tm_tests.test_threshold_alert_generation()
    tm_tests.test_drift_prediction()
    tm_tests.test_ethisches_ideal_check()
    tm_tests.test_dashboard_data()
    
    # Governance Compliance tests
    print("\n🏛️ Governance Compliance Tests:")
    print("-" * 40)
    gc_tests = TestGovernanceCompliance()
    gc_tests.test_default_council_initialization()
    gc_tests.test_submit_signature()
    gc_tests.test_quorum_check()
    gc_tests.test_generate_reminders()
    gc_tests.test_saul_log_integrity()
    gc_tests.test_compliance_check()
    
    # IPFS Integrity tests
    print("\n🌐 IPFS Integrity Tests:")
    print("-" * 40)
    ipfs_tests = TestIPFSIntegrity()
    ipfs_tests.test_default_nodes_initialization()
    ipfs_tests.test_add_content()
    ipfs_tests.test_sync_nodes()
    ipfs_tests.test_content_integrity_verification()
    ipfs_tests.test_seedbringer_redundancy()
    ipfs_tests.test_api_status()
    
    # Coronation Simulator tests
    print("\n🎭 Coronation Simulator Tests:")
    print("-" * 40)
    cs_tests = TestCoronationSimulator()
    cs_tests.test_default_scenarios_initialization()
    cs_tests.test_run_simulation()
    cs_tests.test_metrics_collection()
    cs_tests.test_threshold_checking()
    cs_tests.test_capacity_planning()
    cs_tests.test_stress_test_bottleneck_detection()
    cs_tests.test_markdown_report_generation()
    cs_tests.test_dashboard_data()
    
    print("\n" + "=" * 60)
    print("✅ All operational component tests passed!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
