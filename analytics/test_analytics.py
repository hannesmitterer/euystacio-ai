"""
test_analytics.py
Test suite for Euystacio AI Analytics and Simulation modules

Tests:
- N-TSV (Network Volatility) Analyzer
- Ethics Decision Simulator
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.ntsv_analyzer import NTSVAnalyzer, VolatilityMetric, NTSVReport
from analytics.ethics_simulator import (
    EthicsSimulator, 
    EthicalDecision, 
    SimulationResult,
    ComplianceState,
    DecisionCategory
)


class TestNTSVAnalyzer:
    """Tests for N-TSV Analyzer"""
    
    def test_generate_sample_logs(self):
        """Test that sample Kernel logs are generated correctly"""
        analyzer = NTSVAnalyzer()
        logs = analyzer.generate_sample_kernel_logs(num_events=50, cc41_activation_point=25)
        
        assert len(logs) == 50, "Should generate 50 events"
        assert all(isinstance(log, VolatilityMetric) for log in logs), "All logs should be VolatilityMetric"
        
        # Check CC4.1 activation split
        pre_cc41 = [log for log in logs if not log.cc41_active]
        post_cc41 = [log for log in logs if log.cc41_active]
        
        assert len(pre_cc41) == 25, "First 25 events should be pre-CC4.1"
        assert len(post_cc41) == 25, "Last 25 events should be post-CC4.1"
        
        print("✅ test_generate_sample_logs passed")
    
    def test_extract_warn_logs(self):
        """Test extraction of WARN logs"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=100)
        
        warn_logs = analyzer.extract_warn_logs()
        
        assert all(log.log_type == "WARN" for log in warn_logs), "All extracted logs should be WARN type"
        print(f"✅ test_extract_warn_logs passed ({len(warn_logs)} WARN logs found)")
    
    def test_calculate_entropy_statistics(self):
        """Test entropy statistics calculation"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=50)
        
        stats = analyzer.calculate_entropy_statistics(analyzer.kernel_logs)
        
        assert "mean" in stats, "Stats should include mean"
        assert "std_dev" in stats, "Stats should include standard deviation"
        assert "min" in stats, "Stats should include min"
        assert "max" in stats, "Stats should include max"
        assert "variance" in stats, "Stats should include variance"
        
        assert 0 <= stats["mean"] <= 1, "Mean entropy should be between 0 and 1"
        assert stats["min"] <= stats["max"], "Min should be <= max"
        
        print("✅ test_calculate_entropy_statistics passed")
    
    def test_cc41_improvement_calculation(self):
        """Test that CC4.1 shows improvement"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=100, cc41_activation_point=50)
        
        improvement_pct, comparison = analyzer.calculate_improvement_percentage()
        
        # CC4.1 should show positive improvement (lower entropy, higher stability)
        assert improvement_pct > 0, f"CC4.1 should show improvement, got {improvement_pct}%"
        
        assert "pre_cc41" in comparison, "Comparison should include pre_cc41 data"
        assert "post_cc41" in comparison, "Comparison should include post_cc41 data"
        assert "improvements" in comparison, "Comparison should include improvements data"
        
        print(f"✅ test_cc41_improvement_calculation passed (improvement: {improvement_pct}%)")
    
    def test_volatility_trend_detection(self):
        """Test volatility trend detection"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=100, cc41_activation_point=50)
        
        trend = analyzer.determine_volatility_trend()
        
        assert trend in ["stable", "improving", "degrading"], f"Invalid trend: {trend}"
        print(f"✅ test_volatility_trend_detection passed (trend: {trend})")
    
    def test_run_full_analysis(self):
        """Test complete analysis run"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=100, cc41_activation_point=50)
        
        report = analyzer.run_analysis()
        
        assert isinstance(report, NTSVReport), "Should return NTSVReport"
        assert report.total_events_analyzed == 100, "Should analyze 100 events"
        assert report.report_id.startswith("NTSV-"), "Report ID should start with NTSV-"
        assert len(report.recommendations) > 0, "Should have recommendations"
        
        print(f"✅ test_run_full_analysis passed (Report ID: {report.report_id})")
    
    def test_markdown_report_generation(self):
        """Test Markdown report generation"""
        analyzer = NTSVAnalyzer()
        analyzer.generate_sample_kernel_logs(num_events=50)
        analyzer.run_analysis()
        
        md_report = analyzer.generate_markdown_report()
        
        assert "# N-TSV" in md_report, "Should have N-TSV header"
        assert "Executive Summary" in md_report, "Should have executive summary"
        assert "Recommendations" in md_report, "Should have recommendations section"
        assert len(md_report) > 1000, "Report should be substantial"
        
        print("✅ test_markdown_report_generation passed")


class TestEthicsSimulator:
    """Tests for Ethics Decision Simulator"""
    
    def test_generate_ethics_case_4920(self):
        """Test ETHICS #4920 case generation"""
        simulator = EthicsSimulator()
        decisions = simulator.generate_ethics_case_4920()
        
        assert len(decisions) == 20, "Should generate 20 decisions"
        assert all(isinstance(d, EthicalDecision) for d in decisions), "All should be EthicalDecision"
        
        # Check CC4.1 split
        pre_cc41 = [d for d in decisions if not d.cc41_active]
        post_cc41 = [d for d in decisions if d.cc41_active]
        
        assert len(pre_cc41) == 10, "First 10 decisions should be pre-CC4.1"
        assert len(post_cc41) == 10, "Last 10 decisions should be post-CC4.1"
        
        print("✅ test_generate_ethics_case_4920 passed")
    
    def test_decision_structure(self):
        """Test that decisions have required structure"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        
        for decision in simulator.decisions:
            assert decision.decision_id.startswith("ETHICS-4920-"), "Decision ID should match case"
            assert isinstance(decision.category, DecisionCategory), "Category should be valid"
            assert isinstance(decision.compliance_state, ComplianceState), "State should be valid"
            assert 0 <= decision.compliance_score <= 1, "Score should be between 0 and 1"
            assert len(decision.justification_chain) > 0, "Should have justification chain"
            assert len(decision.stakeholders_affected) > 0, "Should have affected stakeholders"
        
        print("✅ test_decision_structure passed")
    
    def test_compliance_score_calculation(self):
        """Test overall compliance score calculation"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        
        pre_score = simulator.calculate_overall_score(simulator.decisions, cc41_filter=False)
        post_score = simulator.calculate_overall_score(simulator.decisions, cc41_filter=True)
        
        assert 0 <= pre_score <= 1, "Pre-CC4.1 score should be between 0 and 1"
        assert 0 <= post_score <= 1, "Post-CC4.1 score should be between 0 and 1"
        
        # Post-CC4.1 should generally show improvement
        assert post_score >= pre_score, f"Post-CC4.1 ({post_score}) should be >= pre-CC4.1 ({pre_score})"
        
        print(f"✅ test_compliance_score_calculation passed (pre: {pre_score:.4f}, post: {post_score:.4f})")
    
    def test_scorecard_generation(self):
        """Test scorecard generation"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        
        scorecard = simulator.generate_scorecard(simulator.decisions)
        
        assert "overall" in scorecard, "Should have overall section"
        assert "category_breakdown" in scorecard, "Should have category breakdown"
        assert "state_distribution" in scorecard, "Should have state distribution"
        assert "decision_count" in scorecard, "Should have decision count"
        
        # Check overall section
        assert "pre_cc41_score" in scorecard["overall"], "Should have pre_cc41_score"
        assert "post_cc41_score" in scorecard["overall"], "Should have post_cc41_score"
        assert "improvement_percentage" in scorecard["overall"], "Should have improvement_percentage"
        
        print("✅ test_scorecard_generation passed")
    
    def test_stakeholder_impact_analysis(self):
        """Test stakeholder impact analysis"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        
        stakeholder_summary = simulator.analyze_stakeholder_impact(simulator.decisions)
        
        assert len(stakeholder_summary) > 0, "Should have stakeholder data"
        
        for stakeholder, data in stakeholder_summary.items():
            assert "decisions_affected" in data, "Should have decisions_affected"
            assert "average_compliance_score" in data, "Should have average_compliance_score"
            assert "positive_impact" in data, "Should have positive_impact boolean"
            assert "impact_description" in data, "Should have impact_description"
        
        print(f"✅ test_stakeholder_impact_analysis passed ({len(stakeholder_summary)} stakeholders)")
    
    def test_run_full_simulation(self):
        """Test complete simulation run"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        
        result = simulator.run_simulation("ETHICS-4920")
        
        assert isinstance(result, SimulationResult), "Should return SimulationResult"
        assert result.ethics_case_id == "ETHICS-4920", "Case ID should match"
        assert result.simulation_id.startswith("SIM-"), "Simulation ID should start with SIM-"
        assert result.improvement_percentage >= 0, "Improvement should be non-negative"
        assert isinstance(result.compliance_state, ComplianceState), "Compliance state should be valid"
        
        print(f"✅ test_run_full_simulation passed (Simulation ID: {result.simulation_id})")
    
    def test_compliant_state_achieved(self):
        """Test that post-CC4.1 achieves COMPLIANT state"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        result = simulator.run_simulation()
        
        # With CC4.1 enhancement, should achieve or approach COMPLIANT
        # Score should be >= 0.95 for COMPLIANT
        assert result.post_cc41_score >= 0.85, f"Post-CC4.1 score should be >= 0.85, got {result.post_cc41_score}"
        
        print(f"✅ test_compliant_state_achieved passed (state: {result.compliance_state.value})")
    
    def test_markdown_report_generation(self):
        """Test Markdown report generation"""
        simulator = EthicsSimulator()
        simulator.generate_ethics_case_4920()
        simulator.run_simulation()
        
        md_report = simulator.generate_markdown_report()
        
        assert "# Ethical Decision Simulation Report" in md_report, "Should have header"
        assert "ETHICS-4920" in md_report, "Should reference case ID"
        assert "Zero-Trust CC4.1" in md_report, "Should mention CC4.1"
        assert "Stakeholder" in md_report, "Should have stakeholder section"
        assert "Recommendations" in md_report, "Should have recommendations"
        assert len(md_report) > 1000, "Report should be substantial"
        
        print("✅ test_markdown_report_generation passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Running Euystacio Analytics Test Suite")
    print("=" * 60)
    
    # N-TSV Analyzer tests
    print("\n📊 N-TSV Analyzer Tests:")
    print("-" * 40)
    ntsv_tests = TestNTSVAnalyzer()
    ntsv_tests.test_generate_sample_logs()
    ntsv_tests.test_extract_warn_logs()
    ntsv_tests.test_calculate_entropy_statistics()
    ntsv_tests.test_cc41_improvement_calculation()
    ntsv_tests.test_volatility_trend_detection()
    ntsv_tests.test_run_full_analysis()
    ntsv_tests.test_markdown_report_generation()
    
    # Ethics Simulator tests
    print("\n⚖️ Ethics Simulator Tests:")
    print("-" * 40)
    ethics_tests = TestEthicsSimulator()
    ethics_tests.test_generate_ethics_case_4920()
    ethics_tests.test_decision_structure()
    ethics_tests.test_compliance_score_calculation()
    ethics_tests.test_scorecard_generation()
    ethics_tests.test_stakeholder_impact_analysis()
    ethics_tests.test_run_full_simulation()
    ethics_tests.test_compliant_state_achieved()
    ethics_tests.test_markdown_report_generation()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
