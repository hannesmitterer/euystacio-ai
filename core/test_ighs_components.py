"""
test_ighs_components.py
Test suite for IGHS (Incorruptible Global Health System) Components

Tests:
- Custos Sentimento (AIC) - Ethical AI Governance
- Ethics Gap Calculator - H-VAR and Ethics Gap measurement
- Quantum Solutions - AI decision optimization
- Peacobonds - Immutable aid distribution
- AETERNA GOVERNATIA - Eternal guardianship framework
"""

import sys
import os

# Ensure the parent directory is in the path for proper imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.custos_sentimento import (
    CustosSentimento, EthicalPrincipleType, ValidationStatus
)
from core.ethics_gap_calculator import (
    EthicsGapCalculator, EthicsGapSeverity, VolatilityLevel
)
from core.quantum_solutions import (
    QuantumSolutions, ImpactLevel, DecisionSpeed, InterventionType
)
from core.peacobonds import (
    PeacobandsSystem, PeacobondStatus, ResourceType, SecurityLevel
)
from core.aeterna_governatia import (
    AeternaGovernati, GovernanceAction, TransparencyLevel, CorruptionRisk
)


class TestCustosSentimento:
    """Tests for Custos Sentimento (AIC)"""
    
    def test_initialization(self):
        """Test Custos Sentimento initialization"""
        cs = CustosSentimento()
        
        assert len(cs.ethical_rules) == 5
        assert cs.state.guardian_active is True
        assert cs.state.enforcement_level == "strict"
        
        print("✅ test_initialization passed")
    
    def test_valid_action_approval(self):
        """Test that valid actions are approved"""
        cs = CustosSentimento()
        
        action = {
            "action_type": "distribute_aid",
            "intent": "help communities",
            "motivation": "compassion and love",
            "ownership_model": "shared stewardship",
            "resources": [{"id": "r1", "shared": True, "access_level": "universal"}],
            "beneficiaries": ["all communities"],
            "access_restrictions": [],
            "conditions": []
        }
        
        validation = cs.validate_action(action)
        
        assert validation.status == ValidationStatus.APPROVED
        assert len(validation.rules_passed) == 5
        assert len(validation.rules_failed) == 0
        
        print("✅ test_valid_action_approval passed")
    
    def test_invalid_action_rejection(self):
        """Test that invalid actions are rejected"""
        cs = CustosSentimento()
        
        action = {
            "action_type": "resource_control",
            "intent": "maximize profit",
            "motivation": "financial gain",
            "ownership_model": "exclusive ownership",
            "resources": [{"id": "r1", "shared": False, "access_level": "private"}],
            "beneficiaries": ["shareholders"],
            "access_restrictions": ["wealth requirement"],
            "conditions": []
        }
        
        validation = cs.validate_action(action)
        
        assert validation.status == ValidationStatus.REJECTED
        assert len(validation.rules_failed) > 0
        assert len(validation.enforcement_actions) > 0
        
        print("✅ test_invalid_action_rejection passed")
    
    def test_ethical_enforcement(self):
        """Test ethical enforcement mechanism"""
        cs = CustosSentimento()
        
        action = {
            "action_type": "test",
            "intent": "control",
            "motivation": "profit",
            "ownership_model": "ownership",
            "resources": [],
            "beneficiaries": [],
            "access_restrictions": [],
            "conditions": []
        }
        
        enforcement = cs.enforce_ethical_compliance(action)
        
        assert enforcement["allowed"] is False
        assert enforcement["status"] == ValidationStatus.REJECTED.value
        
        print("✅ test_ethical_enforcement passed")
    
    def test_guardian_status(self):
        """Test guardian status reporting"""
        cs = CustosSentimento()
        
        # Perform some validations
        cs.validate_action({
            "action_type": "test",
            "motivation": "love",
            "ownership_model": "sharing",
            "resources": [],
            "beneficiaries": [],
            "access_restrictions": [],
            "conditions": []
        })
        
        status = cs.get_guardian_status()
        
        assert "core_principle" in status
        assert "No ownership, only sharing" in status["core_principle"]
        assert status["active_rules"] == 5
        assert status["immutable_rules"] == 5
        
        print("✅ test_guardian_status passed")


class TestEthicsGapCalculator:
    """Tests for Ethics Gap Calculator"""
    
    def test_initialization(self):
        """Test Ethics Gap Calculator initialization"""
        calc = EthicsGapCalculator()
        
        assert calc.ethical_ideal_target == 0.95
        assert calc.hvar_threshold == 0.043
        assert calc.hvar_proactive_threshold == 0.042
        
        print("✅ test_initialization passed")
    
    def test_ethics_gap_calculation(self):
        """Test Ethics Gap calculation"""
        calc = EthicsGapCalculator()
        
        gap = calc.calculate_ethics_gap(0.85)
        
        assert abs(gap.gap_value - 0.10) < 0.01  # Allow small floating point differences
        assert gap.severity in [EthicsGapSeverity.MINIMAL, EthicsGapSeverity.LOW]  # Close to boundary
        assert gap.ethical_ideal == 0.95
        assert gap.actual_performance == 0.85
        
        print("✅ test_ethics_gap_calculation passed")
    
    def test_hvar_calculation(self):
        """Test H-VAR calculation"""
        calc = EthicsGapCalculator()
        
        # Add some performance data
        data = [0.90, 0.91, 0.92, 0.93, 0.92, 0.91]
        
        hvar = calc.calculate_hvar(data)
        
        assert hvar.volatility_level in VolatilityLevel
        assert 0.0 <= hvar.hvar_value <= 1.0
        assert hvar.trend in ["increasing", "decreasing", "stable"]
        
        print("✅ test_hvar_calculation passed")
    
    def test_diagnostic_run(self):
        """Test complete diagnostic run"""
        calc = EthicsGapCalculator()
        
        diagnostic = calc.run_diagnostic(0.88)
        
        assert diagnostic.ethics_gap is not None
        assert diagnostic.hvar is not None
        assert isinstance(diagnostic.intervention_required, bool)
        assert diagnostic.intervention_urgency in ["low", "medium", "high", "critical"]
        
        print("✅ test_diagnostic_run passed")
    
    def test_corax_trigger(self):
        """Test CORAX trigger condition"""
        calc = EthicsGapCalculator()
        
        # Create high volatility scenario
        for i in range(10):
            calc.add_performance_data(0.70 + (i * 0.05))
        
        diagnostic = calc.run_diagnostic(0.75)
        
        # Should trigger CORAX due to high H-VAR
        assert diagnostic.corax_trigger is True
        
        print("✅ test_corax_trigger passed")


class TestQuantumSolutions:
    """Tests for Quantum Solutions"""
    
    def test_initialization(self):
        """Test Quantum Solutions initialization"""
        qs = QuantumSolutions()
        
        assert qs.automation_threshold == 0.90
        assert qs.max_decision_time_ms == 100
        
        print("✅ test_initialization passed")
    
    def test_data_capture(self):
        """Test data capture"""
        qs = QuantumSolutions()
        
        capture = qs.capture_data(
            sources=["sensor-001", "sensor-002"],
            raw_data={"locations": [{"id": "loc-1", "population": 1000}]},
            real_time=True
        )
        
        assert capture.real_time is True
        assert len(capture.data_sources) == 2
        assert 0.0 <= capture.data_quality <= 1.0
        
        print("✅ test_data_capture passed")
    
    def test_optimal_points_identification(self):
        """Test optimal points identification"""
        qs = QuantumSolutions()
        
        capture = qs.capture_data(
            sources=["test"],
            raw_data={
                "points": [
                    {
                        "location": {"id": "p1"},
                        "beneficiaries_count": 5000,
                        "urgency": 0.8,
                        "resources_needed": 1.5
                    }
                ]
            }
        )
        
        points = qs.identify_optimal_points(capture)
        
        assert len(points) > 0
        assert points[0].impact_level in ImpactLevel
        assert points[0].beneficiaries_count > 0
        
        print("✅ test_optimal_points_identification passed")
    
    def test_decision_making(self):
        """Test decision making"""
        qs = QuantumSolutions()
        
        # Create optimal points
        capture = qs.capture_data(
            sources=["test"],
            raw_data={
                "points": [
                    {
                        "location": {"id": "p1"},
                        "beneficiaries_count": 1000,
                        "urgency": 0.9,
                        "resources_needed": 1.0
                    }
                ]
            }
        )
        
        points = qs.identify_optimal_points(capture)
        
        decision = qs.make_decision(
            optimal_points=points,
            intervention_type=InterventionType.CRISIS_RESPONSE,
            available_resources={"medical": 10.0},
            ethical_validation_score=0.95
        )
        
        assert decision.intervention_type == InterventionType.CRISIS_RESPONSE
        assert decision.execution_speed in DecisionSpeed
        assert isinstance(decision.automated, bool)
        
        print("✅ test_decision_making passed")
    
    def test_end_to_end_optimization(self):
        """Test end-to-end optimization"""
        qs = QuantumSolutions()
        
        situation = {
            "sources": ["monitoring"],
            "crisis_level": 0.8,
            "locations": [
                {
                    "id": "region-1",
                    "population": 10000,
                    "crisis_level": 0.9,
                    "needs": 2.0
                }
            ]
        }
        
        constraints = {
            "resources": {"aid": 5.0},
            "ethical_score": 0.92
        }
        
        decision = qs.optimize_for_max_impact(situation, constraints)
        
        assert decision is not None
        assert len(decision.optimal_points) >= 0
        
        print("✅ test_end_to_end_optimization passed")


class TestPeacobonds:
    """Tests for Peacobonds System"""
    
    def test_initialization(self):
        """Test Peacobonds system initialization"""
        system = PeacobandsSystem()
        
        assert system.ipfs_enabled is True
        assert system.zero_trust_enabled is True
        assert len(system.ipfs_nodes) >= 3
        
        print("✅ test_initialization passed")
    
    def test_peacobond_creation(self):
        """Test peacobond creation"""
        system = PeacobandsSystem()
        
        resources = [
            {
                "type": "MEDICAL_SUPPLIES",
                "quantity": 100,
                "unit": "units",
                "value": 5000
            }
        ]
        
        bond = system.create_peacobond(
            resources=resources,
            beneficiary="community-001",
            issuer="IGHS-Test",
            security_level=SecurityLevel.HIGH
        )
        
        assert bond.status == PeacobondStatus.ACTIVE
        assert bond.bond_id.startswith("PB-")
        assert bond.ipfs_cid is not None
        assert len(bond.resources) == 1
        
        print("✅ test_peacobond_creation passed")
    
    def test_zero_trust_verification(self):
        """Test Zero-Trust verification"""
        system = PeacobandsSystem()
        
        bond = system.create_peacobond(
            resources=[{"type": "FOOD", "quantity": 50, "unit": "kg", "value": 500}],
            beneficiary="community-002",
            issuer="IGHS-Test"
        )
        
        # Authorized access
        verification = system.verify_access(
            bond_id=bond.bond_id,
            entity_id="community-002",
            credentials={
                "biometric_verified": True,
                "cryptographic_signature": True
            }
        )
        
        assert verification.passed is True
        assert verification.trust_score >= system.trust_threshold
        
        # Unauthorized access
        verification2 = system.verify_access(
            bond_id=bond.bond_id,
            entity_id="unauthorized",
            credentials={}
        )
        
        assert verification2.passed is False
        
        print("✅ test_zero_trust_verification passed")
    
    def test_tamper_detection(self):
        """Test tamper detection and auto-deactivation"""
        system = PeacobandsSystem()
        
        bond = system.create_peacobond(
            resources=[{"type": "WATER", "quantity": 1000, "unit": "liters", "value": 1000}],
            beneficiary="community-003",
            issuer="IGHS-Test"
        )
        
        # Multiple unauthorized access attempts
        for _ in range(3):
            system.verify_access(bond_id=bond.bond_id, entity_id="attacker", credentials={})
        
        # Bond should be deactivated
        assert bond.status == PeacobondStatus.DEACTIVATED
        assert bond.tamper_attempts >= 3
        
        print("✅ test_tamper_detection passed")
    
    def test_system_stats(self):
        """Test system statistics"""
        system = PeacobandsSystem()
        
        # Create a few bonds
        system.create_peacobond(
            resources=[{"type": "MEDICAL_SUPPLIES", "quantity": 10, "unit": "units", "value": 100}],
            beneficiary="test-1",
            issuer="IGHS"
        )
        
        stats = system.get_system_stats()
        
        assert stats["total_bonds"] > 0
        assert "status_breakdown" in stats
        assert stats["ipfs_enabled"] is True
        
        print("✅ test_system_stats passed")


class TestAeternaGovernatia:
    """Tests for AETERNA GOVERNATIA"""
    
    def test_initialization(self):
        """Test AETERNA GOVERNATIA initialization"""
        ag = AeternaGovernati()
        
        assert len(ag.ethical_codes) == 6
        assert ag.max_power_concentration == 0.30
        assert ag.transparency_default == TransparencyLevel.PUBLIC
        
        print("✅ test_initialization passed")
    
    def test_governance_action_recording(self):
        """Test governance action recording"""
        ag = AeternaGovernati()
        
        record = ag.record_governance_action(
            action_type=GovernanceAction.RESOURCE_ALLOCATION,
            actor="entity-test",
            decision_data={
                "resources": {"aid": 1000},
                "impact_score": 0.5,
                "motivation": "help communities"
            }
        )
        
        assert record.record_id.startswith("GR-")
        assert record.ethical_compliance is True
        assert record.record_hash is not None
        
        print("✅ test_governance_action_recording passed")
    
    def test_chain_integrity(self):
        """Test governance chain integrity"""
        ag = AeternaGovernati()
        
        # Record multiple actions
        for i in range(3):
            ag.record_governance_action(
                action_type=GovernanceAction.RESOURCE_ALLOCATION,
                actor=f"entity-{i}",
                decision_data={"impact_score": 0.3}
            )
        
        integrity = ag.verify_chain_integrity()
        
        assert integrity["verified"] is True
        assert integrity["chain_length"] == 3
        assert len(integrity["broken_links"]) == 0
        
        print("✅ test_chain_integrity passed")
    
    def test_power_distribution_audit(self):
        """Test power distribution audit"""
        ag = AeternaGovernati()
        
        # Record actions from same entity
        for _ in range(5):
            ag.record_governance_action(
                action_type=GovernanceAction.POLICY_CHANGE,
                actor="dominant-entity",
                decision_data={"impact_score": 0.15}
            )
        
        audit = ag.audit_power_distribution()
        
        assert "distribution_health" in audit
        assert "entities_tracked" in audit
        assert audit["entities_tracked"] > 0
        
        print("✅ test_power_distribution_audit passed")
    
    def test_ethical_code_enforcement(self):
        """Test ethical code enforcement"""
        ag = AeternaGovernati()
        
        enforcement = ag.enforce_ethical_code(
            code_id="UEC-001",
            violation_data={
                "actor": "violator-entity",
                "violation": "ownership_claim"
            }
        )
        
        assert "actions_taken" in enforcement
        assert len(enforcement["actions_taken"]) > 0
        assert enforcement["immutable_record"] is True
        
        print("✅ test_ethical_code_enforcement passed")
    
    def test_transparency_report(self):
        """Test transparency report generation"""
        ag = AeternaGovernati()
        
        # Record some actions
        ag.record_governance_action(
            action_type=GovernanceAction.RESOURCE_ALLOCATION,
            actor="test-entity",
            decision_data={"impact_score": 0.4}
        )
        
        report = ag.get_transparency_report()
        
        assert report["total_governance_actions"] > 0
        assert 0.0 <= report["ethical_compliance_rate"] <= 1.0
        assert "transparency_breakdown" in report
        assert report["chain_integrity"] is True
        
        print("✅ test_transparency_report passed")


def run_all_tests():
    """Run all IGHS component tests"""
    print("\n" + "=" * 60)
    print("🧪 Running IGHS Components Test Suite")
    print("=" * 60)
    
    # Custos Sentimento tests
    print("\n🛡️ Custos Sentimento (AIC) Tests:")
    print("-" * 40)
    cs_tests = TestCustosSentimento()
    cs_tests.test_initialization()
    cs_tests.test_valid_action_approval()
    cs_tests.test_invalid_action_rejection()
    cs_tests.test_ethical_enforcement()
    cs_tests.test_guardian_status()
    
    # Ethics Gap Calculator tests
    print("\n📊 Ethics Gap Calculator Tests:")
    print("-" * 40)
    eg_tests = TestEthicsGapCalculator()
    eg_tests.test_initialization()
    eg_tests.test_ethics_gap_calculation()
    eg_tests.test_hvar_calculation()
    eg_tests.test_diagnostic_run()
    eg_tests.test_corax_trigger()
    
    # Quantum Solutions tests
    print("\n⚛️ Quantum Solutions Tests:")
    print("-" * 40)
    qs_tests = TestQuantumSolutions()
    qs_tests.test_initialization()
    qs_tests.test_data_capture()
    qs_tests.test_optimal_points_identification()
    qs_tests.test_decision_making()
    qs_tests.test_end_to_end_optimization()
    
    # Peacobonds tests
    print("\n🕊️ Peacobonds Tests:")
    print("-" * 40)
    pb_tests = TestPeacobonds()
    pb_tests.test_initialization()
    pb_tests.test_peacobond_creation()
    pb_tests.test_zero_trust_verification()
    pb_tests.test_tamper_detection()
    pb_tests.test_system_stats()
    
    # AETERNA GOVERNATIA tests
    print("\n⚖️ AETERNA GOVERNATIA Tests:")
    print("-" * 40)
    ag_tests = TestAeternaGovernatia()
    ag_tests.test_initialization()
    ag_tests.test_governance_action_recording()
    ag_tests.test_chain_integrity()
    ag_tests.test_power_distribution_audit()
    ag_tests.test_ethical_code_enforcement()
    ag_tests.test_transparency_report()
    
    print("\n" + "=" * 60)
    print("✅ All IGHS component tests passed!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
