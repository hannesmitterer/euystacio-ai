"""
test_ighs_components.py
Test suite for IGHS (Incorruptible Global Health System) Components

Tests:
- Ethics Metrics Calculator (Ethics Gap and H-VAR)
- Quantum-Inspired Optimizer
- Integration tests
"""

import sys
import os

# Ensure the parent directory is in the path for proper imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.ethics_metrics import (
    EthicsMetricsCalculator,
    DimensionType,
    DimensionState,
    DataSource
)
from core.quantum_optimization import (
    QuantumInspiredOptimizer,
    Intervention,
    InterventionType,
    EthicalConstraintType,
    OptimizationConstraints
)
from datetime import datetime, timezone


class TestEthicsMetrics:
    """Tests for Ethics Metrics Calculator"""
    
    def test_ethics_gap_calculation(self):
        """Test basic ethics gap calculation"""
        calculator = EthicsMetricsCalculator()
        
        # Create dimension states
        dimension_states = {
            DimensionType.HEALTH_ACCESS: DimensionState(
                dimension=DimensionType.HEALTH_ACCESS,
                current_value=0.70,
                ideal_value=1.0,
                weight=0.20,
                confidence=0.90,
                timestamp=datetime.now(timezone.utc).isoformat()
            ),
            DimensionType.ECONOMIC_EQUITY: DimensionState(
                dimension=DimensionType.ECONOMIC_EQUITY,
                current_value=0.60,
                ideal_value=1.0,
                weight=0.18,
                confidence=0.85,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        }
        
        # Calculate ethics gap
        result = calculator.calculate_ethics_gap(dimension_states)
        
        # Verify results
        assert result.total_gap > 0, "Ethics gap should be positive"
        assert result.total_gap == result.euclidean_distance, "Total gap should equal Euclidean distance"
        assert 0 <= result.overall_confidence <= 1, "Confidence should be between 0 and 1"
        assert result.worst_dimension in dimension_states, "Worst dimension should be in input"
        
        print("✅ test_ethics_gap_calculation passed")
    
    def test_hvar_calculation(self):
        """Test H-VAR calculation with sufficient data"""
        calculator = EthicsMetricsCalculator()
        
        # Generate enough data points
        for i in range(40):
            dimension_states = {
                DimensionType.HEALTH_ACCESS: DimensionState(
                    dimension=DimensionType.HEALTH_ACCESS,
                    current_value=0.70 + (i * 0.001),
                    ideal_value=1.0,
                    weight=0.20,
                    confidence=0.90,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            }
            calculator.calculate_ethics_gap(dimension_states)
        
        # Calculate H-VAR
        hvar_result = calculator.calculate_hvar()
        
        assert hvar_result is not None, "H-VAR should be calculated with sufficient data"
        assert hvar_result.h_var >= 0, "H-VAR should be non-negative"
        assert hvar_result.trend in ["stable", "increasing", "decreasing"], "Trend should be valid"
        assert isinstance(hvar_result.requires_attention, bool), "Attention flag should be boolean"
        
        print(f"✅ test_hvar_calculation passed (H-VAR: {hvar_result.h_var:.4f}, trend: {hvar_result.trend})")
    
    def test_intervention_priorities(self):
        """Test intervention priority generation"""
        calculator = EthicsMetricsCalculator()
        
        # Create dimension states with varying gaps
        dimension_states = {
            DimensionType.HEALTH_ACCESS: DimensionState(
                dimension=DimensionType.HEALTH_ACCESS,
                current_value=0.50,  # Large gap
                ideal_value=1.0,
                weight=0.20,
                confidence=0.90,
                timestamp=datetime.now(timezone.utc).isoformat()
            ),
            DimensionType.EDUCATION_ACCESS: DimensionState(
                dimension=DimensionType.EDUCATION_ACCESS,
                current_value=0.90,  # Small gap
                ideal_value=1.0,
                weight=0.15,
                confidence=0.95,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        }
        
        calculator.calculate_ethics_gap(dimension_states)
        priorities = calculator.get_intervention_priorities()
        
        assert len(priorities) > 0, "Should have priorities"
        assert priorities[0]["priority_score"] >= priorities[-1]["priority_score"], "Should be sorted by priority"
        assert "recommended_action" in priorities[0], "Should have recommended action"
        
        print("✅ test_intervention_priorities passed")
    
    def test_pca_analysis(self):
        """Test PCA analysis with sufficient data"""
        calculator = EthicsMetricsCalculator()
        
        # Generate data with all dimensions
        for i in range(30):
            dimension_states = {}
            for dim in DimensionType:
                dimension_states[dim] = DimensionState(
                    dimension=dim,
                    current_value=0.60 + (i * 0.005),
                    ideal_value=1.0,
                    weight=calculator.dimension_weights[dim],
                    confidence=0.90,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            calculator.calculate_ethics_gap(dimension_states)
        
        # Perform PCA
        pca_result = calculator.perform_pca_analysis(n_components=2)
        
        assert "error" not in pca_result, "PCA should succeed with sufficient data"
        assert pca_result["n_components"] == 2, "Should have requested number of components"
        assert len(pca_result["explained_variance"]) == 2, "Should have variance for each component"
        # Note: explained variance is ratio, cumulative should be <= 1.0
        assert pca_result["cumulative_variance"][-1] <= 1.0, "Cumulative variance should be <= 1.0"
        
        print(f"✅ test_pca_analysis passed (variance explained: {pca_result['cumulative_variance'][-1]:.2%})")


class TestQuantumOptimization:
    """Tests for Quantum-Inspired Optimizer"""
    
    def test_ethical_compliance_check(self):
        """Test that only ethically compliant interventions are selected"""
        optimizer = QuantumInspiredOptimizer()
        
        # Create interventions with varying compliance
        compliant_intervention = Intervention(
            intervention_id="INT-COMPLIANT",
            intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
            target_dimension="HEALTH_ACCESS",
            estimated_impact=0.30,
            cost=500000,
            implementation_time=180,
            leverage_score=0.85,
            region="Region-A",
            population_affected=50000,
            ethical_compliance={
                EthicalConstraintType.NO_FORCED_RELOCATION: True,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                EthicalConstraintType.NO_COERCION: True,
                EthicalConstraintType.LOCAL_AUTONOMY: True
            }
        )
        
        non_compliant_intervention = Intervention(
            intervention_id="INT-NON-COMPLIANT",
            intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
            target_dimension="HEALTH_ACCESS",
            estimated_impact=0.40,
            cost=400000,
            implementation_time=150,
            leverage_score=0.90,
            region="Region-B",
            population_affected=60000,
            ethical_compliance={
                EthicalConstraintType.NO_FORCED_RELOCATION: False,  # Violation
                EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                EthicalConstraintType.NO_COERCION: True,
                EthicalConstraintType.LOCAL_AUTONOMY: True
            }
        )
        
        # Define constraints requiring all ethical constraints
        constraints = OptimizationConstraints(
            max_budget=1000000,
            max_time=200,
            min_ethical_compliance=1.0,
            required_constraints=[
                EthicalConstraintType.NO_FORCED_RELOCATION,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION,
                EthicalConstraintType.NO_COERCION,
                EthicalConstraintType.LOCAL_AUTONOMY
            ]
        )
        
        # Run optimization
        result = optimizer.optimize(
            available_interventions=[compliant_intervention, non_compliant_intervention],
            constraints=constraints,
            current_ethics_gap=0.50,
            current_hvar=0.08,
            max_iterations=20
        )
        
        # Verify only compliant interventions selected
        assert result.ethical_compliance, "Result should be ethically compliant"
        for intervention in result.selected_interventions:
            assert intervention.is_ethically_compliant(), "All selected interventions must be compliant"
            assert intervention.intervention_id != "INT-NON-COMPLIANT", "Non-compliant intervention should not be selected"
        
        print("✅ test_ethical_compliance_check passed")
    
    def test_budget_constraint(self):
        """Test that budget constraints are respected"""
        optimizer = QuantumInspiredOptimizer()
        
        # Create interventions
        interventions = [
            Intervention(
                intervention_id=f"INT-{i}",
                intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
                target_dimension="HEALTH_ACCESS",
                estimated_impact=0.20,
                cost=300000,
                implementation_time=100,
                leverage_score=0.80,
                region="Region-A",
                population_affected=40000,
                ethical_compliance={
                    EthicalConstraintType.NO_FORCED_RELOCATION: True,
                    EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                    EthicalConstraintType.NO_COERCION: True,
                    EthicalConstraintType.LOCAL_AUTONOMY: True
                }
            )
            for i in range(5)
        ]
        
        # Set budget constraint
        budget = 700000
        constraints = OptimizationConstraints(
            max_budget=budget,
            max_time=200,
            min_ethical_compliance=1.0,
            required_constraints=[
                EthicalConstraintType.NO_FORCED_RELOCATION,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION
            ]
        )
        
        # Run optimization
        result = optimizer.optimize(
            available_interventions=interventions,
            constraints=constraints,
            current_ethics_gap=0.45,
            current_hvar=0.07,
            max_iterations=30
        )
        
        # Verify budget constraint
        assert result.total_cost <= budget, f"Total cost {result.total_cost} should not exceed budget {budget}"
        assert result.constraints_satisfied, "All constraints should be satisfied"
        
        print(f"✅ test_budget_constraint passed (used ${result.total_cost:,.2f} of ${budget:,.2f})")
    
    def test_leverage_point_identification(self):
        """Test identification of high-leverage interventions"""
        optimizer = QuantumInspiredOptimizer()
        
        # Create interventions with varying leverage scores
        interventions = []
        for i in range(10):
            interventions.append(Intervention(
                intervention_id=f"INT-{i}",
                intervention_type=InterventionType.EDUCATION_SYSTEMS,
                target_dimension="EDUCATION_ACCESS",
                estimated_impact=0.15 + (i * 0.02),
                cost=200000 + (i * 10000),
                implementation_time=120,
                leverage_score=0.50 + (i * 0.05),
                region="Region-A",
                population_affected=30000,
                ethical_compliance={
                    EthicalConstraintType.NO_FORCED_RELOCATION: True,
                    EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                    EthicalConstraintType.NO_COERCION: True,
                    EthicalConstraintType.LOCAL_AUTONOMY: True
                }
            ))
        
        # Identify leverage points
        leverage_points = optimizer.identify_leverage_points(interventions, top_n=3)
        
        assert len(leverage_points) <= 3, "Should return at most 3 leverage points"
        assert len(leverage_points) > 0, "Should identify leverage points"
        
        # Verify sorted by leverage score
        for i in range(len(leverage_points) - 1):
            assert leverage_points[i]["leverage_score"] >= leverage_points[i+1]["leverage_score"], \
                "Should be sorted by leverage score descending"
        
        print(f"✅ test_leverage_point_identification passed (top leverage: {leverage_points[0]['leverage_score']:.4f})")
    
    def test_optimization_improves_metrics(self):
        """Test that optimization actually improves ethics gap and H-VAR"""
        optimizer = QuantumInspiredOptimizer()
        
        # Create effective interventions
        interventions = [
            Intervention(
                intervention_id=f"INT-{i}",
                intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
                target_dimension="HEALTH_ACCESS",
                estimated_impact=0.25,
                cost=400000,
                implementation_time=150,
                leverage_score=0.85,
                region="Region-A",
                population_affected=50000,
                ethical_compliance={
                    EthicalConstraintType.NO_FORCED_RELOCATION: True,
                    EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                    EthicalConstraintType.NO_COERCION: True,
                    EthicalConstraintType.LOCAL_AUTONOMY: True
                }
            )
            for i in range(3)
        ]
        
        constraints = OptimizationConstraints(
            max_budget=1000000,
            max_time=200,
            min_ethical_compliance=1.0,
            required_constraints=[
                EthicalConstraintType.NO_FORCED_RELOCATION,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION
            ]
        )
        
        current_ethics_gap = 0.50
        current_hvar = 0.08
        
        result = optimizer.optimize(
            available_interventions=interventions,
            constraints=constraints,
            current_ethics_gap=current_ethics_gap,
            current_hvar=current_hvar,
            max_iterations=50
        )
        
        # Verify improvements
        assert result.ethics_gap_reduction > 0, "Should reduce ethics gap"
        assert result.hvar_reduction > 0, "Should reduce H-VAR"
        assert result.overall_score > 0, "Should have positive optimization score"
        
        print(f"✅ test_optimization_improves_metrics passed "
              f"(gap reduction: {result.ethics_gap_reduction:.4f}, "
              f"hvar reduction: {result.hvar_reduction:.4f})")


class TestIntegration:
    """Integration tests for IGHS components"""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from metrics to optimization"""
        # 1. Calculate ethics metrics
        calculator = EthicsMetricsCalculator()
        
        dimension_states = {}
        for dim in DimensionType:
            dimension_states[dim] = DimensionState(
                dimension=dim,
                current_value=0.65,
                ideal_value=1.0,
                weight=calculator.dimension_weights[dim],
                confidence=0.90,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        
        # Generate some history
        for _ in range(30):
            calculator.calculate_ethics_gap(dimension_states)
        
        gap_result = calculator.calculate_ethics_gap(dimension_states)
        hvar_result = calculator.calculate_hvar()
        
        # 2. Get intervention priorities
        priorities = calculator.get_intervention_priorities()
        
        # 3. Create interventions based on priorities
        interventions = []
        for i, priority in enumerate(priorities[:3]):
            interventions.append(Intervention(
                intervention_id=f"INT-PRIORITY-{i}",
                intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
                target_dimension=priority["dimension"],
                estimated_impact=0.30,
                cost=500000,
                implementation_time=180,
                leverage_score=priority["priority_score"],
                region="Region-A",
                population_affected=50000,
                ethical_compliance={
                    EthicalConstraintType.NO_FORCED_RELOCATION: True,
                    EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                    EthicalConstraintType.NO_COERCION: True,
                    EthicalConstraintType.LOCAL_AUTONOMY: True
                }
            ))
        
        # 4. Optimize intervention selection
        optimizer = QuantumInspiredOptimizer()
        
        constraints = OptimizationConstraints(
            max_budget=1200000,
            max_time=200,
            min_ethical_compliance=1.0,
            required_constraints=[
                EthicalConstraintType.NO_FORCED_RELOCATION,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION,
                EthicalConstraintType.NO_COERCION,
                EthicalConstraintType.LOCAL_AUTONOMY
            ]
        )
        
        result = optimizer.optimize(
            available_interventions=interventions,
            constraints=constraints,
            current_ethics_gap=gap_result.total_gap,
            current_hvar=hvar_result.h_var if hvar_result else 0.08,
            max_iterations=50
        )
        
        # 5. Verify complete workflow
        assert gap_result.total_gap > 0, "Should have calculated ethics gap"
        assert len(priorities) > 0, "Should have priorities"
        assert result.ethical_compliance, "Optimized solution should be compliant"
        assert result.constraints_satisfied, "Optimized solution should satisfy constraints"
        assert result.ethics_gap_reduction > 0, "Should plan to reduce ethics gap"
        
        print(f"✅ test_end_to_end_workflow passed")
        print(f"   Ethics Gap: {gap_result.total_gap:.4f}")
        print(f"   Selected Interventions: {len(result.selected_interventions)}")
        print(f"   Planned Gap Reduction: {result.ethics_gap_reduction:.4f}")
        print(f"   Total Cost: ${result.total_cost:,.2f}")


def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("IGHS Component Test Suite")
    print("=" * 60)
    
    # Ethics Metrics Tests
    print("\n📊 Testing Ethics Metrics Calculator...")
    ethics_tests = TestEthicsMetrics()
    ethics_tests.test_ethics_gap_calculation()
    ethics_tests.test_hvar_calculation()
    ethics_tests.test_intervention_priorities()
    ethics_tests.test_pca_analysis()
    
    # Quantum Optimization Tests
    print("\n⚛️ Testing Quantum-Inspired Optimizer...")
    optimizer_tests = TestQuantumOptimization()
    optimizer_tests.test_ethical_compliance_check()
    optimizer_tests.test_budget_constraint()
    optimizer_tests.test_leverage_point_identification()
    optimizer_tests.test_optimization_improves_metrics()
    
    # Integration Tests
    print("\n🔗 Testing Integration...")
    integration_tests = TestIntegration()
    integration_tests.test_end_to_end_workflow()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
