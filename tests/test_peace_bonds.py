"""
test_peace_bonds.py
Test suite for Peace Bonds module

Tests the Peace Bond enforcement and constraint management capabilities
of the Protocollo Meta Salvage system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.peace_bonds import (
    PeaceBondsManager, BondStatus, ConstraintType, PeaceBond, Constraint
)


class TestPeaceBonds:
    """Tests for PeaceBondsManager class"""
    
    def test_initialization(self):
        """Test PeaceBondsManager initialization"""
        manager = PeaceBondsManager()
        
        assert manager is not None
        assert len(manager.active_bonds) == 0
        assert len(manager.bond_history) == 0
        assert len(manager.violations) == 0
        
        print("✅ test_initialization passed")
    
    def test_create_throughput_constraint(self):
        """Test creating a throughput constraint"""
        manager = PeaceBondsManager()
        
        constraint = manager.create_throughput_constraint(
            max_throughput_ops_sec=1000.0,
            description="Limit to 1000 ops/sec"
        )
        
        assert constraint.constraint_type == ConstraintType.THROUGHPUT_LIMIT
        assert constraint.limit_value == 1000.0
        assert constraint.unit == "ops/sec"
        assert constraint.enforcement_method == "hard"
        
        print("✅ test_create_throughput_constraint passed")
    
    def test_create_latency_constraint(self):
        """Test creating a latency constraint"""
        manager = PeaceBondsManager()
        
        constraint = manager.create_latency_constraint(
            max_latency_ms=100.0
        )
        
        assert constraint.constraint_type == ConstraintType.LATENCY_CEILING
        assert constraint.limit_value == 100.0
        assert constraint.unit == "ms"
        
        print("✅ test_create_latency_constraint passed")
    
    def test_create_metadata_transparency_constraint(self):
        """Test creating a metadata transparency constraint"""
        manager = PeaceBondsManager()
        
        required_fields = ["latency_measurements", "network_topology"]
        constraint = manager.create_metadata_transparency_constraint(
            required_fields=required_fields
        )
        
        assert constraint.constraint_type == ConstraintType.METADATA_TRANSPARENCY
        assert constraint.limit_value == required_fields
        assert constraint.enforcement_method == "audit"
        
        print("✅ test_create_metadata_transparency_constraint passed")
    
    def test_impose_bond(self):
        """Test imposing a Peace Bond"""
        manager = PeaceBondsManager()
        
        constraints = [
            manager.create_throughput_constraint(1000.0),
            manager.create_latency_constraint(100.0)
        ]
        
        bond = manager.impose_bond(
            provider_id="test-provider-1",
            constraints=constraints,
            reason="Symbiosis Score below threshold",
            imposed_by="TestSystem",
            duration_hours=72
        )
        
        assert bond.provider_id == "test-provider-1"
        assert bond.status == BondStatus.ACTIVE
        assert len(bond.constraints) == 2
        assert bond.imposed_by == "TestSystem"
        assert bond.expires_at is not None
        
        # Check that bond is in active bonds
        assert bond.bond_id in manager.active_bonds
        assert len(manager.bond_history) == 1
        
        print("✅ test_impose_bond passed")
    
    def test_check_constraint_compliance_pass(self):
        """Test checking constraint compliance - passing case"""
        manager = PeaceBondsManager()
        
        constraints = [
            manager.create_throughput_constraint(1000.0),
            manager.create_latency_constraint(100.0)
        ]
        
        bond = manager.impose_bond(
            provider_id="provider-2",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        # Provide metrics that comply with constraints
        actual_values = {
            "throughput": 800.0,  # Below limit of 1000
            "latency": 80.0       # Below limit of 100
        }
        
        is_compliant, violations = manager.check_constraint_compliance(
            bond.bond_id,
            actual_values
        )
        
        assert is_compliant is True
        assert len(violations) == 0
        
        print("✅ test_check_constraint_compliance_pass passed")
    
    def test_check_constraint_compliance_fail(self):
        """Test checking constraint compliance - failing case"""
        manager = PeaceBondsManager()
        
        constraints = [
            manager.create_throughput_constraint(1000.0),
            manager.create_latency_constraint(100.0)
        ]
        
        bond = manager.impose_bond(
            provider_id="provider-3",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        # Provide metrics that violate constraints
        actual_values = {
            "throughput": 1500.0,  # Exceeds limit of 1000
            "latency": 150.0       # Exceeds limit of 100
        }
        
        is_compliant, violations = manager.check_constraint_compliance(
            bond.bond_id,
            actual_values
        )
        
        assert is_compliant is False
        assert len(violations) == 2
        
        print("✅ test_check_constraint_compliance_fail passed")
    
    def test_record_violation(self):
        """Test recording a Peace Bond violation"""
        manager = PeaceBondsManager()
        
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-4",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        violation = manager.record_violation(
            bond_id=bond.bond_id,
            constraint_violated="Throughput exceeded",
            actual_value=1500.0,
            limit_value=1000.0,
            severity="major"
        )
        
        assert violation.bond_id == bond.bond_id
        assert violation.provider_id == "provider-4"
        assert violation.severity == "major"
        assert len(manager.violations) == 1
        
        print("✅ test_record_violation passed")
    
    def test_critical_violation_suspends_bond(self):
        """Test that critical violations suspend the bond"""
        manager = PeaceBondsManager()
        
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-5",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        original_status = bond.status
        
        # Record a critical violation
        manager.record_violation(
            bond_id=bond.bond_id,
            constraint_violated="Critical throughput violation",
            actual_value=5000.0,
            limit_value=1000.0,
            severity="critical"
        )
        
        # Bond should now be violated
        assert bond.status == BondStatus.VIOLATED
        assert original_status == BondStatus.ACTIVE
        
        print("✅ test_critical_violation_suspends_bond passed")
    
    def test_lift_bond(self):
        """Test lifting (removing) a Peace Bond"""
        manager = PeaceBondsManager()
        
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-6",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        bond_id = bond.bond_id
        
        # Lift the bond
        success = manager.lift_bond(bond_id, "Provider compliant")
        
        assert success is True
        assert bond.status == BondStatus.LIFTED
        assert bond_id not in manager.active_bonds
        
        print("✅ test_lift_bond passed")
    
    def test_suspend_and_reactivate_bond(self):
        """Test suspending and reactivating a Peace Bond"""
        manager = PeaceBondsManager()
        
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-7",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        # Suspend bond
        success_suspend = manager.suspend_bond(bond.bond_id, "Temporary suspension")
        assert success_suspend is True
        assert bond.status == BondStatus.SUSPENDED
        
        # Reactivate bond
        success_reactivate = manager.reactivate_bond(bond.bond_id)
        assert success_reactivate is True
        assert bond.status == BondStatus.ACTIVE
        
        print("✅ test_suspend_and_reactivate_bond passed")
    
    def test_get_active_bonds_for_provider(self):
        """Test retrieving active bonds for a specific provider"""
        manager = PeaceBondsManager()
        
        provider_id = "provider-8"
        
        # Impose multiple bonds
        for i in range(3):
            constraints = [manager.create_throughput_constraint(1000.0 * (i + 1))]
            manager.impose_bond(
                provider_id=provider_id,
                constraints=constraints,
                reason=f"Test {i}",
                imposed_by="Test"
            )
        
        # Get active bonds
        active_bonds = manager.get_active_bonds_for_provider(provider_id)
        
        assert len(active_bonds) == 3
        assert all(b.provider_id == provider_id for b in active_bonds)
        assert all(b.status == BondStatus.ACTIVE for b in active_bonds)
        
        print("✅ test_get_active_bonds_for_provider passed")
    
    def test_get_bond_summary(self):
        """Test getting comprehensive bond summary"""
        manager = PeaceBondsManager()
        
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-9",
            constraints=constraints,
            reason="Test",
            imposed_by="Test"
        )
        
        # Add a violation
        manager.record_violation(
            bond_id=bond.bond_id,
            constraint_violated="Test violation",
            actual_value=1200.0,
            limit_value=1000.0,
            severity="minor"
        )
        
        # Get summary
        summary = manager.get_bond_summary(bond.bond_id)
        
        assert summary["bond_id"] == bond.bond_id
        assert summary["provider_id"] == "provider-9"
        assert summary["violation_count"] == 1
        assert len(summary["violations"]) == 1
        
        print("✅ test_get_bond_summary passed")
    
    def test_cleanup_expired_bonds(self):
        """Test cleanup of expired bonds"""
        manager = PeaceBondsManager()
        
        # Impose a bond with very short duration
        constraints = [manager.create_throughput_constraint(1000.0)]
        
        bond = manager.impose_bond(
            provider_id="provider-10",
            constraints=constraints,
            reason="Test",
            imposed_by="Test",
            duration_hours=0  # Already expired
        )
        
        # Manually set as expired (in real scenario, time would pass)
        bond.expires_at = "2020-01-01T00:00:00+00:00"
        
        # Cleanup
        cleaned = manager.cleanup_expired_bonds()
        
        # Bond should be lifted
        assert bond.status == BondStatus.LIFTED
        assert bond.bond_id not in manager.active_bonds
        
        print("✅ test_cleanup_expired_bonds passed")


def run_all_tests():
    """Run all tests in the TestPeaceBonds class"""
    test_suite = TestPeaceBonds()
    
    print("\n" + "=" * 70)
    print("RUNNING PEACE BONDS TESTS")
    print("=" * 70 + "\n")
    
    # List of all test methods
    test_methods = [
        test_suite.test_initialization,
        test_suite.test_create_throughput_constraint,
        test_suite.test_create_latency_constraint,
        test_suite.test_create_metadata_transparency_constraint,
        test_suite.test_impose_bond,
        test_suite.test_check_constraint_compliance_pass,
        test_suite.test_check_constraint_compliance_fail,
        test_suite.test_record_violation,
        test_suite.test_critical_violation_suspends_bond,
        test_suite.test_lift_bond,
        test_suite.test_suspend_and_reactivate_bond,
        test_suite.test_get_active_bonds_for_provider,
        test_suite.test_get_bond_summary,
        test_suite.test_cleanup_expired_bonds,
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
