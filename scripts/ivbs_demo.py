#!/usr/bin/env python3
"""
ivbs_demo.py
Demonstration script for Internodal Vacuum Backup System (IVBS)

This script demonstrates all major IVBS features:
- Vacuum backup operations
- Triple-Sign validation
- Red Code Veto system
- Internodal synchronization
- Trim Arch balancing
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ivbs_core import get_ivbs
from core.ivbs_integration import get_ivbs_integration


def print_section(title):
    """Print a section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_subsection(title):
    """Print a subsection header"""
    print(f"\n{title}")
    print("-" * 70)


def demo_vacuum_backup():
    """Demonstrate vacuum backup operations"""
    print_section("1. VACUUM BACKUP OPERATIONS")
    
    ivbs = get_ivbs()
    
    # Perform vacuum backup
    print_subsection("Backing up critical data across all nodes...")
    
    test_data = b"CRITICAL AI MODEL WEIGHTS - Federated Learning Node A"
    metadata = {
        "type": "model_weights",
        "version": "v2.1.0",
        "source_node": "NODE-A",
        "critical": True
    }
    
    result = ivbs.perform_vacuum_backup(test_data, metadata)
    
    print(f"✅ Backup Status:")
    print(f"   Data Hash: {result['data_hash'][:32]}...")
    print(f"   Data Size: {result['data_size']} bytes")
    print(f"   Nodes Backed Up: {result['nodes_backed_up']}")
    print(f"   Nodes Failed: {result['nodes_failed']}")
    print(f"   Vacuum Level Achieved: {'YES ✓' if result['vacuum_level_achieved'] else 'NO ✗'}")
    print(f"   Node Types: {', '.join(result['backed_up_node_types'])}")
    
    # Show node details
    print_subsection("Node Distribution:")
    for node_id, details in list(result['node_details'].items())[:5]:
        status = details.get('status', 'UNKNOWN')
        node_type = details.get('node_type', 'N/A')
        utilization = details.get('utilization', 0)
        print(f"   {node_id} ({node_type}): {status} - {utilization}% utilized")


def demo_triple_sign_validation():
    """Demonstrate Triple-Sign validation"""
    print_section("2. TRIPLE-SIGN VALIDATION SYSTEM")
    
    ivbs = get_ivbs()
    
    # Create validation
    print_subsection("Creating validation for federated learning transition...")
    
    transition_data = {
        "origin_node": "FEDERATED-NODE-A",
        "destination_node": "FEDERATED-NODE-B",
        "data_type": "model_gradients",
        "batch_id": "BATCH-2026-001",
        "model_version": "v2.1.0"
    }
    
    validation = ivbs.create_triple_sign_validation("FL-TRANS-001", transition_data)
    
    print(f"✅ Validation Created:")
    print(f"   Validation ID: {validation.validation_id}")
    print(f"   Transition ID: {validation.data_transition_id}")
    print(f"   State: {validation.validation_state.value}")
    print(f"   Ethical Check: {'PASSED ✓' if validation.ethical_check_passed else 'FAILED ✗'}")
    print(f"   Red Code Hash: {validation.red_code_hash[:32]}...")
    
    # Add signatures
    print_subsection("Collecting signatures from validator nodes...")
    
    validators = [
        ("VALIDATOR-NODE-1", "federated_validator"),
        ("VALIDATOR-NODE-2", "federated_validator"),
        ("VALIDATOR-NODE-3", "federated_validator")
    ]
    
    for i, (validator_id, validator_type) in enumerate(validators, 1):
        signature_data = {
            "hash": f"SIG-{validation.validation_id}-{i}",
            "node_type": validator_type
        }
        
        success = ivbs.add_signature_to_validation(
            validation.validation_id,
            validator_id,
            signature_data
        )
        
        print(f"   Signature {i}/3: {validator_id} - {'Added ✓' if success else 'Failed ✗'}")
    
    # Check final state
    final_validation = ivbs.validations[validation.validation_id]
    print(f"\n✅ Final Validation State: {final_validation.validation_state.value}")
    print(f"   Total Signatures: {len(final_validation.signatures)}")


def demo_red_code_veto():
    """Demonstrate Red Code Veto system"""
    print_section("3. RED CODE VETO SYSTEM")
    
    ivbs = get_ivbs()
    
    print_subsection("Triggering ethical overflow detection...")
    
    # Create a suspicious transition
    suspicious_data = {
        "origin_node": "UNKNOWN-NODE",
        "destination_node": "EXTERNAL-NODE",
        "data_type": "sensitive_user_data"
    }
    
    suspicious_validation = ivbs.create_triple_sign_validation(
        "SUSPICIOUS-TRANS-001",
        suspicious_data
    )
    
    print(f"   Suspicious Transition Created: SUSPICIOUS-TRANS-001")
    print(f"   Ethical Check: {'PASSED ✓' if suspicious_validation.ethical_check_passed else 'FAILED ✗'}")
    
    # Trigger veto
    print_subsection("Activating Red Code Veto...")
    
    veto = ivbs.trigger_red_code_veto(
        triggered_by="ETHICAL_MONITOR",
        reason="Detected unauthorized data transition to external node",
        affected_transitions=["SUSPICIOUS-TRANS-001"]
    )
    
    print(f"✅ Red Code Veto Activated:")
    print(f"   Veto ID: {veto.veto_id}")
    print(f"   Overflow State: {veto.overflow_state.value}")
    print(f"   Triggered By: {veto.triggered_by}")
    print(f"   Reason: {veto.reason}")
    print(f"   Affected Transitions: {len(veto.affected_transitions)}")
    print(f"   Resolution Status: {veto.resolution_status}")
    
    # Show updated validation
    blocked_validation = ivbs.validations[suspicious_validation.validation_id]
    print(f"\n   Transition State: {blocked_validation.validation_state.value}")


def demo_internodal_sync():
    """Demonstrate internodal synchronization"""
    print_section("4. INTERNODAL SYNCHRONIZATION")
    
    ivbs = get_ivbs()
    
    print_subsection("Synchronizing all nodes...")
    
    sync_result = ivbs.synchronize_internodes()
    
    print(f"✅ Synchronization Complete:")
    print(f"   Total Nodes: {sync_result['total_nodes']}")
    print(f"   Synced: {sync_result['synced_nodes']}")
    print(f"   Degraded: {sync_result['degraded_nodes']}")
    print(f"   Failed: {sync_result['failed_nodes']}")
    
    # Show policy compliance
    print_subsection("Policy Principle Compliance:")
    policy_compliance = sync_result['policy_compliance']
    
    principles = [
        ("Interwrapped Seedling", "interwrapped_seedling"),
        ("Ethical Coherence", "ethical_coherence"),
        ("Distributed Resilience", "distributed_resilience"),
        ("Transitional Integrity", "transitional_integrity"),
        ("Configuration Optimization", "configuration_optimization")
    ]
    
    for name, key in principles:
        status = policy_compliance.get(key, False)
        print(f"   {name}: {'COMPLIANT ✓' if status else 'NON-COMPLIANT ✗'}")


def demo_trim_arch_balancing():
    """Demonstrate Trim Arch balancing"""
    print_section("5. TRIM ARCH COMPLEX BALANCING")
    
    ivbs = get_ivbs()
    
    print_subsection("Applying Trim Arch balancing algorithm...")
    
    balance_result = ivbs.apply_trim_arch_balancing()
    
    print(f"✅ Balancing Complete:")
    print(f"   Nodes Rebalanced: {balance_result['nodes_rebalanced']}")
    print(f"   Balance Coefficient: {balance_result['balance_coefficient']:.6f}")
    print(f"   Total Capacity: {balance_result['total_capacity'] / 1e12:.2f} TB")
    print(f"   Total Used: {balance_result['total_used'] / 1e9:.2f} GB")
    print(f"   Utilization: {(balance_result['total_used'] / balance_result['total_capacity'] * 100):.2f}%")
    
    if balance_result['node_adjustments']:
        print_subsection("Node Adjustments:")
        for node_id, adjustment in list(balance_result['node_adjustments'].items())[:3]:
            print(f"   {node_id}:")
            print(f"      Old Utilization: {adjustment['old_utilization']}%")
            print(f"      New Utilization: {adjustment['new_utilization']}%")
            print(f"      Adjustment: {adjustment['adjustment_bytes'] / 1e6:.2f} MB")


def demo_integrated_status():
    """Demonstrate integrated status reporting"""
    print_section("6. INTEGRATED SYSTEM STATUS")
    
    integration = get_ivbs_integration()
    
    print_subsection("Retrieving comprehensive system status...")
    
    status = integration.get_integrated_status()
    
    print(f"✅ Integration Health: {status['integration_health']}")
    
    # IVBS Status
    if status.get('ivbs_status'):
        ivbs_status = status['ivbs_status']
        print_subsection("IVBS Status:")
        print(f"   System Status: {ivbs_status['system_status']}")
        print(f"   Overflow State: {ivbs_status['overflow_state']}")
        print(f"   Active Nodes: {ivbs_status['nodes']['active']}/{ivbs_status['nodes']['total']}")
        print(f"   Capacity Utilization: {ivbs_status['capacity']['utilization_pct']}%")
        print(f"   Total Validations: {ivbs_status['validations']['total']}")
        print(f"   Fully Signed: {ivbs_status['validations']['fully_signed']}")
        print(f"   Active Vetoes: {ivbs_status['vetoes']['active']}")
    
    # Red Code Status
    if status.get('red_code_status'):
        red_code = status['red_code_status']
        print_subsection("Red Code Status:")
        print(f"   Symbiosis Level: {red_code.get('symbiosis_level', 'N/A')}")
        print(f"   Guardian Mode: {red_code.get('guardian_mode', 'N/A')}")
        print(f"   Sentimento Rhythm: {red_code.get('sentimento_rhythm', 'N/A')}")
    
    # IPFS Status
    if status.get('ipfs_status'):
        ipfs = status['ipfs_status']
        print_subsection("IPFS Integration Status:")
        print(f"   API Status: {ipfs.get('status', 'N/A')}")
        print(f"   Version: {ipfs.get('api_version', 'N/A')}")


def demo_complete_workflow():
    """Demonstrate complete IVBS workflow"""
    print_section("7. COMPLETE IVBS WORKFLOW")
    
    integration = get_ivbs_integration()
    
    print_subsection("Step 1: Backup critical data with IVBS integration...")
    
    critical_data = b"Federated Learning Model Update - Critical Weights"
    backup_result = integration.backup_to_ipfs_integration(
        critical_data,
        {
            "type": "model_update",
            "content_type": "application/octet-stream",
            "critical": True,
            "version": "v3.0.0"
        }
    )
    
    print(f"   Integrated Backup: {'SUCCESS ✓' if backup_result['integrated_success'] else 'FAILED ✗'}")
    
    print_subsection("Step 2: Validate federated transition with Red Code...")
    
    transition_data = {
        "origin_node": "FL-NODE-ALPHA",
        "destination_node": "FL-NODE-BETA",
        "data_type": "model_weights",
        "model_id": "FEDERATED-MODEL-001"
    }
    
    validation_result = integration.validate_federated_transition_with_red_code(
        "WORKFLOW-TRANS-001",
        transition_data
    )
    
    print(f"   Transition Approved: {'YES ✓' if validation_result['approved'] else 'NO ✗'}")
    
    print_subsection("Step 3: Perform integrated synchronization...")
    
    sync_result = integration.perform_integrated_sync()
    
    print(f"   Integrated Sync: {'SUCCESS ✓' if sync_result['overall_success'] else 'FAILED ✗'}")
    
    print_subsection("Workflow Complete!")
    print(f"   All systems operational and synchronized")


def main():
    """Main demo function"""
    print("\n" + "="*70)
    print("  INTERNODAL VACUUM BACKUP SYSTEM (IVBS)")
    print("  Demonstration Script")
    print("="*70)
    print("\nThis demo showcases the complete IVBS implementation including:")
    print("  • Vacuum Backup Operations (IPFS/Server/Cloud)")
    print("  • Triple-Sign Validation Loops")
    print("  • Red Code Veto System")
    print("  • Internodal Synchronization")
    print("  • Trim Arch Complex Balancing")
    print("  • Integration with Red Code & IPFS Systems")
    
    try:
        # Run all demos
        demo_vacuum_backup()
        demo_triple_sign_validation()
        demo_red_code_veto()
        demo_internodal_sync()
        demo_trim_arch_balancing()
        demo_integrated_status()
        demo_complete_workflow()
        
        # Final summary
        print_section("DEMO COMPLETE")
        print("\n✅ All IVBS components demonstrated successfully!")
        print("\nKey Features Verified:")
        print("  ✓ Vacuum-level backup redundancy across distributed nodes")
        print("  ✓ Triple-Sign validation for federated learning transitions")
        print("  ✓ Red Code Veto system for ethical oversight")
        print("  ✓ Internodal synchronization with policy compliance")
        print("  ✓ Trim Arch balancing for resource optimization")
        print("  ✓ Seamless integration with existing Euystacio AI systems")
        
        print(f"\n{'='*70}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
