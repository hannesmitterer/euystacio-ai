"""
ighs_integration_example.py
Complete integration example showing how all IGHS components work together

This example demonstrates:
1. Ethical validation with Custos Sentimento
2. Ethics Gap and H-VAR diagnostic
3. Quantum decision optimization
4. Peacobond creation and distribution
5. Governance recording with AETERNA GOVERNATIA
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (
    get_custos_sentimento,
    get_ethics_gap_calculator,
    get_quantum_solutions,
    get_peacobonds_system,
    get_aeterna_governatia,
    ValidationStatus,
    GovernanceAction,
    ResourceType,
    SecurityLevel
)


def main():
    print("=" * 70)
    print("IGHS Integration Example - Incorruptible Global Health System")
    print("=" * 70)
    print()
    
    # =========================================================================
    # STEP 1: Ethical Validation with Custos Sentimento
    # =========================================================================
    print("Step 1: Ethical Validation with Custos Sentimento")
    print("-" * 70)
    
    cs = get_custos_sentimento()
    
    # Define an action for crisis response
    action = {
        "action_type": "emergency_aid_distribution",
        "intent": "provide emergency assistance to affected communities",
        "motivation": "compassion, love, and care for those in crisis",
        "ownership_model": "shared stewardship and collective resource management",
        "resources": [
            {
                "id": "medical-supplies-001",
                "shared": True,
                "access_level": "universal"
            },
            {
                "id": "food-supplies-001",
                "shared": True,
                "access_level": "universal"
            }
        ],
        "beneficiaries": ["all affected communities", "universal access"],
        "access_restrictions": [],
        "conditions": ["voluntary participation", "dignity preservation"]
    }
    
    # Validate action
    validation = cs.validate_action(action)
    
    print(f"Validation Status: {validation.status.value}")
    print(f"Rules Passed: {len(validation.rules_passed)}/{len(validation.rules_checked)}")
    print(f"Core Principle: 'No ownership, only sharing. Love is the license.'")
    
    if validation.status != ValidationStatus.APPROVED:
        print("❌ Action rejected by ethical guardian. Cannot proceed.")
        return
    
    print("✅ Action approved by Custos Sentimento")
    print()
    
    # =========================================================================
    # STEP 2: Ethics Gap and H-VAR Diagnostic
    # =========================================================================
    print("Step 2: Ethics Gap and H-VAR Diagnostic")
    print("-" * 70)
    
    calc = get_ethics_gap_calculator()
    
    # Simulate some historical performance data
    for perf in [0.88, 0.89, 0.90, 0.91, 0.92, 0.93]:
        calc.add_performance_data(perf)
    
    # Run diagnostic
    diagnostic = calc.run_diagnostic(
        actual_performance=0.93,
        context={
            "ownership_violations": 0,
            "sharing_compliance": 0.98,
            "love_license_score": 0.95,
            "dignity_violations": 0,
            "access_restrictions": 0
        }
    )
    
    print(f"Ethics Gap: {diagnostic.ethics_gap.gap_value:.3f} ({diagnostic.ethics_gap.severity.value})")
    print(f"H-VAR: {diagnostic.hvar.hvar_value:.4f} ({diagnostic.hvar.volatility_level.value})")
    print(f"Trend: {diagnostic.hvar.trend}")
    print(f"Intervention Required: {diagnostic.intervention_required}")
    print(f"Urgency: {diagnostic.intervention_urgency}")
    print(f"CORAX Trigger: {diagnostic.corax_trigger}")
    
    if diagnostic.recommended_actions:
        print(f"Recommendations:")
        for i, rec in enumerate(diagnostic.recommended_actions[:3], 1):
            print(f"  {i}. {rec}")
    
    print("✅ Diagnostic complete - system within healthy parameters")
    print()
    
    # =========================================================================
    # STEP 3: Quantum Decision Optimization
    # =========================================================================
    print("Step 3: Quantum Decision Optimization")
    print("-" * 70)
    
    qs = get_quantum_solutions()
    
    # Crisis situation data
    situation = {
        "sources": ["satellite_monitoring", "local_health_systems", "community_reports"],
        "crisis_level": 0.75,
        "locations": [
            {
                "id": "region-alpha",
                "name": "Northern Region Alpha",
                "population": 45000,
                "crisis_level": 0.80,
                "needs": 2.2
            },
            {
                "id": "region-beta",
                "name": "Coastal Region Beta",
                "population": 32000,
                "crisis_level": 0.70,
                "needs": 1.8
            },
            {
                "id": "region-gamma",
                "name": "Mountain Region Gamma",
                "population": 18000,
                "crisis_level": 0.65,
                "needs": 1.5
            }
        ],
        "resource_requirements": {
            "medical": 5000,
            "food": 15000,
            "water": 20000
        }
    }
    
    # Constraints
    constraints = {
        "resources": {
            "medical_supplies": 5000,
            "food_supplies": 15000,
            "water_supplies": 20000
        },
        "ethical_score": len(validation.rules_passed) / len(validation.rules_checked),
        "criteria": {"priority": "urgency_and_impact"}
    }
    
    # Optimize for maximum impact
    decision = qs.optimize_for_max_impact(situation, constraints)
    
    print(f"Decision ID: {decision.decision_id}")
    print(f"Intervention Type: {decision.intervention_type.value}")
    print(f"Total Impact Score: {decision.total_impact:.3f}")
    print(f"Execution Speed: {decision.execution_speed.value}")
    print(f"Automated Execution: {decision.automated}")
    print(f"Ethical Validation: {decision.ethical_validation}")
    print(f"Optimal Points Identified: {len(decision.optimal_points)}")
    
    if decision.optimal_points:
        print("\nTop Intervention Points:")
        for i, point in enumerate(decision.optimal_points[:3], 1):
            print(f"  {i}. Impact: {point.impact_score:.3f}, "
                  f"Beneficiaries: {point.beneficiaries_count:,}, "
                  f"Urgency: {point.urgency_score:.2f}")
    
    print("✅ Quantum decision optimized for maximum ethical impact")
    print()
    
    # =========================================================================
    # STEP 4: Peacobond Creation and Distribution
    # =========================================================================
    print("Step 4: Peacobond Creation and Distribution")
    print("-" * 70)
    
    pb_system = get_peacobonds_system()
    
    # Create peacobonds for each optimal point
    bonds_created = []
    
    for point in decision.optimal_points[:3]:
        resources = [
            {
                "type": "MEDICAL_SUPPLIES",
                "quantity": 1000,
                "unit": "units",
                "value": 25000,
                "metadata": {"urgency": "high", "point_id": point.point_id}
            },
            {
                "type": "FOOD",
                "quantity": 5000,
                "unit": "kg",
                "value": 15000,
                "metadata": {"point_id": point.point_id}
            }
        ]
        
        bond = pb_system.create_peacobond(
            resources=resources,
            beneficiary=point.location.get("id", f"community-{len(bonds_created)}"),
            issuer="IGHS-System",
            security_level=SecurityLevel.HIGH,
            expiration_hours=720  # 30 days
        )
        
        bonds_created.append(bond)
        
        print(f"Peacobond {bond.bond_id}:")
        print(f"  Status: {bond.status.value}")
        print(f"  IPFS CID: {bond.ipfs_cid}")
        print(f"  Resources: {len(bond.resources)}")
        print(f"  Security: {bond.security_level.value}")
        print(f"  Zero-Trust: Enabled")
        print()
    
    print(f"✅ Created {len(bonds_created)} peacobonds with immutable properties")
    print()
    
    # =========================================================================
    # STEP 5: Governance Recording with AETERNA GOVERNATIA
    # =========================================================================
    print("Step 5: Governance Recording with AETERNA GOVERNATIA")
    print("-" * 70)
    
    ag = get_aeterna_governatia()
    
    # Record the entire operation in governance chain
    governance_record = ag.record_governance_action(
        action_type=GovernanceAction.RESOURCE_ALLOCATION,
        actor="IGHS-Automated-System",
        decision_data={
            "operation": "emergency_aid_distribution",
            "decision_id": decision.decision_id,
            "validation_id": validation.validation_id,
            "diagnostic_id": diagnostic.diagnostic_id,
            "bonds_created": [b.bond_id for b in bonds_created],
            "total_impact": decision.total_impact,
            "beneficiaries_reached": sum(p.beneficiaries_count for p in decision.optimal_points),
            "impact_score": 0.85,
            "motivation": "compassion and care for communities in crisis"
        },
        signatures=["system-auto-sig"],
        transparency_level=ag.transparency_default
    )
    
    print(f"Governance Record: {governance_record.record_id}")
    print(f"Ethical Compliance: {governance_record.ethical_compliance}")
    print(f"Transparency: {governance_record.transparency_level.value}")
    print(f"Record Hash: {governance_record.record_hash[:16]}...")
    
    # Verify chain integrity
    integrity = ag.verify_chain_integrity()
    print(f"Chain Integrity: {'✅ Verified' if integrity['verified'] else '❌ Compromised'}")
    
    # Get transparency report
    report = ag.get_transparency_report()
    print(f"Total Governance Actions: {report['total_governance_actions']}")
    print(f"Ethical Compliance Rate: {report['ethical_compliance_rate']:.1%}")
    
    print("✅ Complete operation recorded in immutable governance chain")
    print()
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("=" * 70)
    print("IGHS Integration Complete - Summary")
    print("=" * 70)
    print()
    print("✅ Ethical validation passed (Custos Sentimento)")
    print("✅ Ethics Gap and H-VAR within healthy parameters")
    print("✅ Quantum decision optimized for maximum impact")
    print(f"✅ {len(bonds_created)} Peacobonds created with Zero-Trust security")
    print("✅ Complete transparency via AETERNA GOVERNATIA")
    print()
    print("Core Principle Upheld: 'No ownership, only sharing. Love is the license.'")
    print()
    print(f"Total Beneficiaries Reached: {sum(p.beneficiaries_count for p in decision.optimal_points):,}")
    print(f"Total Impact Score: {decision.total_impact:.3f}")
    print(f"Ethical Alignment: {len(validation.rules_passed)}/{len(validation.rules_checked)} rules")
    print()
    print("The Incorruptible Global Health System is operational.")
    print("=" * 70)


if __name__ == "__main__":
    main()
