"""
test_risk_monitor.py
Test suite for Risk Monitor module

Tests the continuous monitoring and risk identification capabilities
of the Protocollo Meta Salvage system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk_monitor import (
    RiskMonitor, RiskLevel, RiskType, RiskEvent, SymbiosisScoreSnapshot
)


class TestRiskMonitor:
    """Tests for RiskMonitor class"""
    
    def test_initialization(self):
        """Test RiskMonitor initialization"""
        monitor = RiskMonitor()
        
        assert monitor is not None
        assert monitor.thresholds["symbiosis_min"] == 0.75
        assert monitor.thresholds["latency_max_ms"] == 100.0
        assert len(monitor.risk_events) == 0
        
        print("✅ test_initialization passed")
    
    def test_record_provider_metrics(self):
        """Test recording provider metrics"""
        monitor = RiskMonitor()
        
        metrics = monitor.record_provider_metrics(
            provider_id="test-provider-1",
            latency_ms=50.0,
            throughput_ops_sec=5000.0,
            cost_per_operation=0.001,
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        assert metrics.provider_id == "test-provider-1"
        assert metrics.latency_ms == 50.0
        assert metrics.throughput_ops_sec == 5000.0
        assert metrics.symbiosis_score == 0.85
        
        # Check that metrics are stored
        assert "test-provider-1" in monitor.provider_metrics
        assert len(monitor.provider_metrics["test-provider-1"]) == 1
        
        print("✅ test_record_provider_metrics passed")
    
    def test_symbiosis_score_tracking(self):
        """Test Symbiosis Score tracking and trend detection"""
        monitor = RiskMonitor()
        
        # Record first score
        snapshot1 = monitor.record_symbiosis_score("provider-1", 0.90)
        assert snapshot1.score == 0.90
        assert snapshot1.trend == "stable"
        assert snapshot1.previous_score is None
        
        # Record improving score
        snapshot2 = monitor.record_symbiosis_score("provider-1", 0.95)
        assert snapshot2.score == 0.95
        assert snapshot2.trend == "improving"
        assert snapshot2.previous_score == 0.90
        
        # Record declining score
        snapshot3 = monitor.record_symbiosis_score("provider-1", 0.85)
        assert snapshot3.score == 0.85
        assert snapshot3.trend == "declining"
        
        print("✅ test_symbiosis_score_tracking passed")
    
    def test_symbiosis_decline_risk_detection(self):
        """Test risk detection when Symbiosis Score declines"""
        monitor = RiskMonitor()
        
        # Record score below threshold
        monitor.record_symbiosis_score("provider-2", 0.70)
        
        # Check that risk event was created
        risks = monitor.get_active_risks(provider_id="provider-2", hours=1)
        
        assert len(risks) > 0
        risk = risks[0]
        assert risk.risk_type == RiskType.SYMBIOSIS_DECLINE
        assert risk.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]
        assert risk.peace_bond_required is True
        
        print("✅ test_symbiosis_decline_risk_detection passed")
    
    def test_latency_manipulation_detection(self):
        """Test detection of latency manipulation"""
        monitor = RiskMonitor()
        
        provider_id = "provider-3"
        
        # Record initial metrics
        monitor.record_provider_metrics(
            provider_id=provider_id,
            latency_ms=80.0,
            throughput_ops_sec=5000.0,
            cost_per_operation=0.001,
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        # Record metrics with significant latency increase
        monitor.record_provider_metrics(
            provider_id=provider_id,
            latency_ms=150.0,  # 87.5% increase
            throughput_ops_sec=5000.0,
            cost_per_operation=0.001,
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        # Check for latency manipulation risk
        risks = monitor.get_active_risks(provider_id=provider_id, hours=1)
        latency_risks = [r for r in risks if r.risk_type == RiskType.LATENCY_MANIPULATION]
        
        assert len(latency_risks) > 0
        risk = latency_risks[0]
        assert risk.peace_bond_required is True
        
        print("✅ test_latency_manipulation_detection passed")
    
    def test_cost_manipulation_detection(self):
        """Test detection of cost manipulation"""
        monitor = RiskMonitor()
        
        provider_id = "provider-4"
        
        # Record initial metrics
        monitor.record_provider_metrics(
            provider_id=provider_id,
            latency_ms=50.0,
            throughput_ops_sec=5000.0,
            cost_per_operation=0.001,
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        # Record metrics with significant cost increase
        monitor.record_provider_metrics(
            provider_id=provider_id,
            latency_ms=50.0,
            throughput_ops_sec=5000.0,
            cost_per_operation=0.0015,  # 50% increase
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        # Check for cost manipulation risk
        risks = monitor.get_active_risks(provider_id=provider_id, hours=1)
        cost_risks = [r for r in risks if r.risk_type == RiskType.COST_MANIPULATION]
        
        assert len(cost_risks) > 0
        
        print("✅ test_cost_manipulation_detection passed")
    
    def test_get_provider_status(self):
        """Test retrieving comprehensive provider status"""
        monitor = RiskMonitor()
        
        provider_id = "provider-5"
        
        # Record some metrics
        monitor.record_provider_metrics(
            provider_id=provider_id,
            latency_ms=50.0,
            throughput_ops_sec=5000.0,
            cost_per_operation=0.001,
            availability_pct=99.5,
            symbiosis_score=0.85
        )
        
        monitor.record_symbiosis_score(provider_id, 0.85)
        
        # Get status
        status = monitor.get_provider_status(provider_id)
        
        assert status["provider_id"] == provider_id
        assert status["latest_metrics"] is not None
        assert status["latest_symbiosis"] is not None
        assert "active_risks" in status
        assert "risk_count" in status
        
        print("✅ test_get_provider_status passed")
    
    def test_get_all_providers_summary(self):
        """Test getting summary of all monitored providers"""
        monitor = RiskMonitor()
        
        # Record metrics for multiple providers
        for i in range(1, 4):
            provider_id = f"provider-{i}"
            monitor.record_provider_metrics(
                provider_id=provider_id,
                latency_ms=50.0 + i * 10,
                throughput_ops_sec=5000.0,
                cost_per_operation=0.001,
                availability_pct=99.5,
                symbiosis_score=0.85
            )
        
        # Get summary
        summary = monitor.get_all_providers_summary()
        
        assert len(summary) == 3
        assert all("provider_id" in s for s in summary)
        
        print("✅ test_get_all_providers_summary passed")
    
    def test_risk_level_filtering(self):
        """Test filtering risks by level"""
        monitor = RiskMonitor()
        
        # Create a high-risk event (score below 0.6 should be HIGH)
        monitor.record_symbiosis_score("provider-6", 0.55)
        
        # Get all risks first to see what was created
        all_risks = monitor.get_active_risks(provider_id="provider-6", hours=1)
        
        assert len(all_risks) > 0, "No risks detected"
        
        # Check that we can filter by the actual risk level that was created
        detected_level = all_risks[0].risk_level
        filtered_risks = monitor.get_active_risks(risk_level=detected_level, hours=1)
        
        assert len(filtered_risks) > 0
        assert all(r.risk_level == detected_level for r in filtered_risks)
        
        print("✅ test_risk_level_filtering passed")


def run_all_tests():
    """Run all tests in the TestRiskMonitor class"""
    test_suite = TestRiskMonitor()
    
    print("\n" + "=" * 70)
    print("RUNNING RISK MONITOR TESTS")
    print("=" * 70 + "\n")
    
    # List of all test methods
    test_methods = [
        test_suite.test_initialization,
        test_suite.test_record_provider_metrics,
        test_suite.test_symbiosis_score_tracking,
        test_suite.test_symbiosis_decline_risk_detection,
        test_suite.test_latency_manipulation_detection,
        test_suite.test_cost_manipulation_detection,
        test_suite.test_get_provider_status,
        test_suite.test_get_all_providers_summary,
        test_suite.test_risk_level_filtering,
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
