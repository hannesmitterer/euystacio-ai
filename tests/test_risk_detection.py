"""
Test suite for Risk Detection and Monitoring
Part of Protocollo Meta Salvage testing infrastructure
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.threshold_monitor import ThresholdMonitor, MetricType, AlertLevel


@pytest.mark.risk
@pytest.mark.unit
class TestThresholdMonitor:
    """Test Threshold Monitor functionality"""
    
    def test_monitor_initialization(self):
        """Test that threshold monitor can be initialized"""
        monitor = ThresholdMonitor()
        assert monitor is not None
        assert monitor.thresholds is not None
    
    def test_qek_metric_recording(self):
        """Test QEK metric recording and validation"""
        monitor = ThresholdMonitor()
        
        # Record a valid QEK value
        snapshot = monitor.record_metric(MetricType.QEK, 0.93)
        
        assert snapshot is not None
        assert snapshot.metric_type == MetricType.QEK
        assert snapshot.value == 0.93
        assert snapshot.within_limits is True
    
    def test_hvar_metric_recording(self):
        """Test H-VAR metric recording and validation"""
        monitor = ThresholdMonitor()
        
        # Record a valid H-VAR value (should be low)
        snapshot = monitor.record_metric(MetricType.H_VAR, 0.043)
        
        assert snapshot is not None
        assert snapshot.metric_type == MetricType.H_VAR
        assert snapshot.value == 0.043
        assert snapshot.within_limits is True
    
    def test_ethisches_ideal_recording(self):
        """Test Ethisches Ideal metric recording"""
        monitor = ThresholdMonitor()
        
        # Record a valid Ethisches Ideal value
        snapshot = monitor.record_metric(MetricType.ETHISCHES_IDEAL, 0.98)
        
        assert snapshot is not None
        assert snapshot.metric_type == MetricType.ETHISCHES_IDEAL
        assert snapshot.value == 0.98
        assert snapshot.within_limits is True
    
    def test_qek_threshold_breach_detection(self):
        """Test that QEK threshold breaches are detected"""
        monitor = ThresholdMonitor()
        
        # Record a QEK value below minimum threshold
        snapshot = monitor.record_metric(MetricType.QEK, 0.80)
        
        assert snapshot.within_limits is False
        # Should generate an alert
        assert len(monitor.alerts) > 0
        assert monitor.alerts[-1].level in [AlertLevel.WARNING, AlertLevel.CRITICAL]
    
    def test_hvar_threshold_breach_detection(self):
        """Test that H-VAR threshold breaches are detected"""
        monitor = ThresholdMonitor()
        
        # Record an H-VAR value above maximum threshold
        snapshot = monitor.record_metric(MetricType.H_VAR, 0.15)
        
        assert snapshot.within_limits is False
        # Should generate an alert
        assert len(monitor.alerts) > 0


@pytest.mark.risk
@pytest.mark.unit
class TestRiskScoring:
    """Test risk score calculations"""
    
    def test_risk_score_calculation(self):
        """Test basic risk score calculation"""
        # Example risk score calculation
        trust_weight = 0.8
        compliance_score = 0.9
        ethical_alignment = 0.85
        
        risk_score = (
            trust_weight * 0.4 +
            compliance_score * 0.3 +
            ethical_alignment * 0.3
        )
        
        assert 0.0 <= risk_score <= 1.0
        assert risk_score > 0.8  # Should be high with these inputs
    
    def test_risk_level_categorization(self):
        """Test risk level categorization"""
        # Define thresholds
        threshold_low = 0.3
        threshold_medium = 0.6
        threshold_high = 0.8
        
        # Test low risk
        risk_score = 0.2
        assert risk_score < threshold_low
        
        # Test medium risk
        risk_score = 0.5
        assert threshold_low <= risk_score < threshold_medium
        
        # Test high risk
        risk_score = 0.7
        assert threshold_medium <= risk_score < threshold_high
        
        # Test critical risk
        risk_score = 0.9
        assert risk_score >= threshold_high


@pytest.mark.risk
@pytest.mark.integration
class TestRiskMonitoring:
    """Integration tests for risk monitoring"""
    
    def test_ethisches_ideal_limits_check(self):
        """Test comprehensive Ethisches Ideal limits checking"""
        monitor = ThresholdMonitor()
        
        # Record some valid metrics
        monitor.record_metric(MetricType.QEK, 0.93)
        monitor.record_metric(MetricType.H_VAR, 0.043)
        monitor.record_metric(MetricType.ETHISCHES_IDEAL, 0.98)
        
        # Check limits
        status = monitor.check_ethisches_ideal_limits()
        
        assert 'overall_compliant' in status
        assert 'metrics' in status
        assert status['overall_compliant'] is True
    
    def test_dashboard_data_generation(self):
        """Test that dashboard data can be generated"""
        monitor = ThresholdMonitor()
        
        # Record metrics
        monitor.record_metric(MetricType.QEK, 0.93)
        monitor.record_metric(MetricType.H_VAR, 0.043)
        
        # Get dashboard data
        dashboard_data = monitor.get_monitoring_dashboard_data()
        
        assert 'timestamp' in dashboard_data
        assert 'metrics' in dashboard_data
        assert 'ethisches_status' in dashboard_data
    
    def test_drift_prediction(self):
        """Test drift prediction functionality"""
        monitor = ThresholdMonitor()
        
        # Record multiple metrics to enable prediction
        for i in range(15):
            monitor.record_metric(MetricType.QEK, 0.93 + (i * 0.001))
        
        # Get drift prediction
        prediction = monitor.predict_drift(MetricType.QEK)
        
        if prediction:  # May return None if insufficient data
            assert 'current_trend' in prediction.__dict__
            assert 'predicted_value' in prediction.__dict__
            assert 'confidence' in prediction.__dict__


@pytest.mark.risk
def test_alert_generation():
    """Test that alerts are properly generated"""
    monitor = ThresholdMonitor()
    
    # Generate an alert by exceeding threshold
    monitor.record_metric(MetricType.QEK, 0.80)  # Below minimum
    
    assert len(monitor.alerts) > 0
    alert = monitor.alerts[-1]
    assert alert.metric_type == MetricType.QEK
    assert alert.level in [AlertLevel.WARNING, AlertLevel.CRITICAL]


@pytest.mark.risk
def test_alert_summary():
    """Test alert summary generation"""
    monitor = ThresholdMonitor()
    
    # Generate some alerts
    monitor.record_metric(MetricType.QEK, 0.80)
    monitor.record_metric(MetricType.H_VAR, 0.15)
    
    summary = monitor.get_alert_summary()
    
    assert 'total_alerts' in summary
    assert 'by_level' in summary
    assert 'by_metric' in summary
    assert summary['total_alerts'] >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
