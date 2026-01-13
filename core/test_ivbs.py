"""
test_ivbs.py
Test suite for Internodal Vacuum Backup System (IVBS)

Tests:
- Vacuum backup operations
- Triple-Sign validation loops
- Red Code Veto system
- Internodal synchronization
- Trim Arch balancing
- Policy compliance
"""

import sys
import os

# Ensure the parent directory is in the path for proper imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.ivbs_core import (
    IVBSCore, VacuumBackupStatus, ValidationState, EthicalOverflowState,
    VacuumBackupNode, TripleSignValidation, RedCodeVeto
)


class TestVacuumBackup:
    """Tests for Vacuum Backup operations"""
    
    def test_initialize_nodes(self):
        """Test that nodes are initialized correctly"""
        ivbs = IVBSCore()
        
        assert len(ivbs.nodes) > 0
        
        # Check for different node types
        node_types = set(n.node_type for n in ivbs.nodes.values())
        assert "ipfs" in node_types
        assert "server" in node_types
        assert "cloud" in node_types
        
        print("✅ test_initialize_nodes passed")
    
    def test_vacuum_backup_operation(self):
        """Test vacuum backup across nodes"""
        ivbs = IVBSCore()
        
        test_data = b"Test data for vacuum backup"
        metadata = {"type": "test", "version": "1.0"}
        
        result = ivbs.perform_vacuum_backup(test_data, metadata)
        
        assert result["nodes_backed_up"] > 0
        assert "data_hash" in result
        assert "vacuum_level_achieved" in result
        
        print(f"✅ test_vacuum_backup_operation passed (backed up to {result['nodes_backed_up']} nodes)")
    
    def test_vacuum_level_achievement(self):
        """Test that vacuum level is achieved with diverse node types"""
        ivbs = IVBSCore()
        
        test_data = b"Test data for vacuum level check"
        result = ivbs.perform_vacuum_backup(test_data, {})
        
        # Should achieve vacuum level with multiple node types
        assert result["vacuum_level_achieved"] is True
        assert len(result["backed_up_node_types"]) >= 2
        
        print("✅ test_vacuum_level_achievement passed")
    
    def test_capacity_management(self):
        """Test that capacity limits are respected"""
        ivbs = IVBSCore()
        
        # Fill a small node to capacity
        for node in ivbs.nodes.values():
            node.capacity_bytes = 1000
            node.used_bytes = 0
        
        # Try to backup data larger than capacity
        large_data = b"X" * 2000
        result = ivbs.perform_vacuum_backup(large_data, {})
        
        # Should have failures due to capacity
        assert result["nodes_failed"] > 0
        
        print("✅ test_capacity_management passed")


class TestTripleSignValidation:
    """Tests for Triple-Sign validation system"""
    
    def test_create_validation(self):
        """Test creating a Triple-Sign validation"""
        ivbs = IVBSCore()
        
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "model_weights"
        }
        
        validation = ivbs.create_triple_sign_validation("TRANS-001", transition_data)
        
        assert validation.validation_id is not None
        assert validation.validation_state == ValidationState.PENDING
        assert validation.ethical_check_passed is True
        assert len(validation.red_code_hash) > 0
        
        print("✅ test_create_validation passed")
    
    def test_add_signatures(self):
        """Test adding signatures to validation"""
        ivbs = IVBSCore()
        
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "model_weights"
        }
        
        validation = ivbs.create_triple_sign_validation("TRANS-002", transition_data)
        
        # Add first signature
        success = ivbs.add_signature_to_validation(
            validation.validation_id,
            "SIGNER-1",
            {"hash": "HASH-1", "node_type": "validator"}
        )
        assert success is True
        
        updated_validation = ivbs.validations[validation.validation_id]
        assert updated_validation.validation_state == ValidationState.PARTIAL_SIGNED
        assert len(updated_validation.signatures) == 1
        
        print("✅ test_add_signatures passed")
    
    def test_full_triple_sign(self):
        """Test completing a full Triple-Sign validation"""
        ivbs = IVBSCore()
        
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "model_weights"
        }
        
        validation = ivbs.create_triple_sign_validation("TRANS-003", transition_data)
        
        # Add three signatures
        for i in range(3):
            ivbs.add_signature_to_validation(
                validation.validation_id,
                f"SIGNER-{i+1}",
                {"hash": f"HASH-{i+1}", "node_type": "validator"}
            )
        
        updated_validation = ivbs.validations[validation.validation_id]
        assert updated_validation.validation_state == ValidationState.FULLY_SIGNED
        assert len(updated_validation.signatures) == 3
        
        print("✅ test_full_triple_sign passed")
    
    def test_ethical_check_failure(self):
        """Test validation with missing ethical metadata"""
        ivbs = IVBSCore()
        
        # Create validation with incomplete data
        incomplete_data = {"origin_node": "NODE-A"}  # Missing required fields
        
        validation = ivbs.create_triple_sign_validation("TRANS-004", incomplete_data)
        
        assert validation.ethical_check_passed is False
        
        print("✅ test_ethical_check_failure passed")


class TestRedCodeVeto:
    """Tests for Red Code Veto system"""
    
    def test_trigger_veto(self):
        """Test triggering a Red Code Veto"""
        ivbs = IVBSCore()
        
        # Create a transition first
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "model_weights"
        }
        validation = ivbs.create_triple_sign_validation("TRANS-VETO-001", transition_data)
        
        # Trigger veto
        veto = ivbs.trigger_red_code_veto(
            "ETHICAL_MONITOR",
            "Detected ethical overflow - unauthorized data transition",
            ["TRANS-VETO-001"]
        )
        
        assert veto.veto_id is not None
        assert veto.resolution_status == "ACTIVE"
        assert veto.overflow_state != EthicalOverflowState.NORMAL
        
        print("✅ test_trigger_veto passed")
    
    def test_veto_blocks_transition(self):
        """Test that veto blocks affected transitions"""
        ivbs = IVBSCore()
        
        # Create a transition
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "model_weights"
        }
        validation = ivbs.create_triple_sign_validation("TRANS-VETO-002", transition_data)
        
        # Trigger veto on this transition
        ivbs.trigger_red_code_veto(
            "ETHICAL_MONITOR",
            "Ethical violation detected",
            ["TRANS-VETO-002"]
        )
        
        # Check that validation is rejected
        updated_validation = ivbs.validations[validation.validation_id]
        assert updated_validation.validation_state == ValidationState.REJECTED
        
        print("✅ test_veto_blocks_transition passed")
    
    def test_overflow_state_escalation(self):
        """Test that overflow state escalates with vetoes"""
        ivbs = IVBSCore()
        
        initial_state = ivbs.current_overflow_state
        
        # Trigger multiple vetoes
        for i in range(2):
            ivbs.trigger_red_code_veto(
                "MONITOR",
                f"Ethical issue {i}",
                [f"TRANS-{i}"]
            )
        
        # State should have escalated
        assert ivbs.current_overflow_state != initial_state
        
        print(f"✅ test_overflow_state_escalation passed (state: {ivbs.current_overflow_state.value})")


class TestInternodalSync:
    """Tests for Internodal Synchronization"""
    
    def test_synchronize_nodes(self):
        """Test synchronizing all nodes"""
        ivbs = IVBSCore()
        
        result = ivbs.synchronize_internodes()
        
        assert "timestamp" in result
        assert "total_nodes" in result
        assert "synced_nodes" in result
        assert result["synced_nodes"] + result["failed_nodes"] + result["degraded_nodes"] == result["total_nodes"]
        
        print(f"✅ test_synchronize_nodes passed ({result['synced_nodes']} nodes synced)")
    
    def test_sync_updates_timestamps(self):
        """Test that sync updates node timestamps"""
        ivbs = IVBSCore()
        
        # Clear timestamps
        for node in ivbs.nodes.values():
            node.last_sync = None
        
        # Perform sync
        ivbs.synchronize_internodes()
        
        # Check that timestamps are updated
        synced_count = sum(1 for node in ivbs.nodes.values() if node.last_sync is not None)
        assert synced_count > 0
        
        print("✅ test_sync_updates_timestamps passed")
    
    def test_policy_compliance_check(self):
        """Test policy compliance checking"""
        ivbs = IVBSCore()
        
        result = ivbs.synchronize_internodes()
        
        assert "policy_compliance" in result
        assert isinstance(result["policy_compliance"], dict)
        
        # Check that all five principles are checked
        assert "interwrapped_seedling" in result["policy_compliance"]
        assert "ethical_coherence" in result["policy_compliance"]
        assert "distributed_resilience" in result["policy_compliance"]
        assert "transitional_integrity" in result["policy_compliance"]
        assert "configuration_optimization" in result["policy_compliance"]
        
        print("✅ test_policy_compliance_check passed")


class TestTrimArchBalancing:
    """Tests for Trim Arch complex balancing"""
    
    def test_apply_balancing(self):
        """Test applying Trim Arch balancing"""
        ivbs = IVBSCore()
        
        # Create imbalance
        nodes_list = list(ivbs.nodes.values())
        if len(nodes_list) >= 2:
            nodes_list[0].used_bytes = int(nodes_list[0].capacity_bytes * 0.9)
            nodes_list[1].used_bytes = int(nodes_list[1].capacity_bytes * 0.1)
        
        result = ivbs.apply_trim_arch_balancing()
        
        assert "timestamp" in result
        assert "balance_coefficient" in result
        assert "nodes_rebalanced" in result
        
        print(f"✅ test_apply_balancing passed (coefficient: {result['balance_coefficient']})")
    
    def test_balancing_reduces_variance(self):
        """Test that balancing reduces utilization variance"""
        ivbs = IVBSCore()
        
        # Create significant imbalance
        nodes_list = list(ivbs.nodes.values())
        for i, node in enumerate(nodes_list):
            if i % 2 == 0:
                node.used_bytes = int(node.capacity_bytes * 0.8)
            else:
                node.used_bytes = int(node.capacity_bytes * 0.2)
        
        # Calculate initial variance
        utilizations = [(n.used_bytes / n.capacity_bytes) if n.capacity_bytes > 0 else 0 for n in ivbs.nodes.values()]
        avg_util = sum(utilizations) / len(utilizations)
        initial_variance = sum((u - avg_util) ** 2 for u in utilizations) / len(utilizations)
        
        # Apply balancing
        result = ivbs.apply_trim_arch_balancing()
        
        # Variance should be reduced or similar
        assert result["balance_coefficient"] <= initial_variance or result["nodes_rebalanced"] > 0
        
        print("✅ test_balancing_reduces_variance passed")


class TestIVBSStatus:
    """Tests for IVBS status reporting"""
    
    def test_get_status(self):
        """Test getting comprehensive IVBS status"""
        ivbs = IVBSCore()
        
        status = ivbs.get_ivbs_status()
        
        assert "timestamp" in status
        assert "system_status" in status
        assert "overflow_state" in status
        assert "nodes" in status
        assert "capacity" in status
        assert "validations" in status
        assert "vetoes" in status
        assert "policy_compliance" in status
        
        print("✅ test_get_status passed")
    
    def test_status_node_breakdown(self):
        """Test node breakdown in status"""
        ivbs = IVBSCore()
        
        status = ivbs.get_ivbs_status()
        
        # Check node statistics
        nodes_section = status["nodes"]
        assert nodes_section["total"] == len(ivbs.nodes)
        assert nodes_section["active"] + nodes_section["degraded"] + nodes_section["failed"] == nodes_section["total"]
        
        # Check node type breakdown
        assert "by_type" in nodes_section
        assert "ipfs" in nodes_section["by_type"]
        assert "server" in nodes_section["by_type"]
        assert "cloud" in nodes_section["by_type"]
        
        print("✅ test_status_node_breakdown passed")
    
    def test_status_capacity_reporting(self):
        """Test capacity reporting in status"""
        ivbs = IVBSCore()
        
        status = ivbs.get_ivbs_status()
        
        capacity = status["capacity"]
        assert capacity["total_bytes"] > 0
        assert capacity["used_bytes"] >= 0
        assert capacity["available_bytes"] == capacity["total_bytes"] - capacity["used_bytes"]
        assert 0 <= capacity["utilization_pct"] <= 100
        
        print("✅ test_status_capacity_reporting passed")


class TestIntegration:
    """Integration tests for complete IVBS workflows"""
    
    def test_complete_workflow(self):
        """Test complete IVBS workflow"""
        ivbs = IVBSCore()
        
        # 1. Perform vacuum backup
        test_data = b"Integration test data"
        backup_result = ivbs.perform_vacuum_backup(test_data, {"type": "integration_test"})
        assert backup_result["vacuum_level_achieved"] is True
        
        # 2. Create validation
        transition_data = {
            "origin_node": "NODE-A",
            "destination_node": "NODE-B",
            "data_type": "test_data"
        }
        validation = ivbs.create_triple_sign_validation("INTEGRATION-001", transition_data)
        assert validation.ethical_check_passed is True
        
        # 3. Add signatures
        for i in range(3):
            ivbs.add_signature_to_validation(
                validation.validation_id,
                f"VALIDATOR-{i}",
                {"hash": f"HASH-{i}", "node_type": "validator"}
            )
        
        updated_validation = ivbs.validations[validation.validation_id]
        assert updated_validation.validation_state == ValidationState.FULLY_SIGNED
        
        # 4. Synchronize nodes
        sync_result = ivbs.synchronize_internodes()
        assert sync_result["synced_nodes"] > 0
        
        # 5. Apply balancing
        balance_result = ivbs.apply_trim_arch_balancing()
        assert "balance_coefficient" in balance_result
        
        # 6. Check final status
        status = ivbs.get_ivbs_status()
        assert status["system_status"] in ["OPERATIONAL", "DEGRADED"]
        
        print("✅ test_complete_workflow passed")


def run_all_tests():
    """Run all IVBS tests"""
    print("🧪 Running IVBS Test Suite")
    print("=" * 60)
    
    test_classes = [
        TestVacuumBackup,
        TestTripleSignValidation,
        TestRedCodeVeto,
        TestInternodalSync,
        TestTrimArchBalancing,
        TestIVBSStatus,
        TestIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 {test_class.__name__}")
        print("-" * 60)
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                passed_tests += 1
            except AssertionError as e:
                print(f"❌ {method_name} failed: {e}")
            except Exception as e:
                print(f"💥 {method_name} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Tests passed: {passed_tests}/{total_tests}")
    print("=" * 60)
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
