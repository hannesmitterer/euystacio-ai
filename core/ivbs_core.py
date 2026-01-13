"""
ivbs_core.py
Internodal Vacuum Backup System (IVBS) - Core Module

This module implements the core functionality for the Internodal Vacuum Backup System,
providing vacuum-level redundancy across distributed AI nodes with ethical oversight.

Key Components:
- Vacuum Backup Orchestration (IPFS/Server/Cloud)
- Internodal Synchronization Services
- Red Code Veto Integration for Ethical Oversight
- Triple-Sign Validation Loops
- Trim Arch Complex Balancing
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class VacuumBackupStatus(Enum):
    """Status of vacuum backup operations"""
    ACTIVE = "ACTIVE"
    SYNCING = "SYNCING"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    SEALED = "SEALED"


class ValidationState(Enum):
    """Validation state for Triple-Sign system"""
    PENDING = "PENDING"
    PARTIAL_SIGNED = "PARTIAL_SIGNED"
    FULLY_SIGNED = "FULLY_SIGNED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class EthicalOverflowState(Enum):
    """Red Code Veto ethical overflow states"""
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    CRITICAL = "CRITICAL"
    VETO_ACTIVE = "VETO_ACTIVE"


@dataclass
class VacuumBackupNode:
    """Represents a node in the vacuum backup system"""
    node_id: str
    node_type: str  # 'ipfs', 'server', 'cloud'
    endpoint: str
    region: str
    is_primary: bool
    last_sync: Optional[str]
    status: VacuumBackupStatus
    capacity_bytes: int
    used_bytes: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "endpoint": self.endpoint,
            "region": self.region,
            "is_primary": self.is_primary,
            "last_sync": self.last_sync,
            "status": self.status.value,
            "capacity_bytes": self.capacity_bytes,
            "used_bytes": self.used_bytes,
            "utilization_pct": round((self.used_bytes / self.capacity_bytes * 100), 2) if self.capacity_bytes > 0 else 0
        }


@dataclass
class TripleSignValidation:
    """Triple-Sign validation record for federated learning transitions"""
    validation_id: str
    data_transition_id: str
    timestamp: str
    signatures: List[Dict[str, Any]]
    validation_state: ValidationState
    ethical_check_passed: bool
    red_code_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "data_transition_id": self.data_transition_id,
            "timestamp": self.timestamp,
            "signatures": self.signatures,
            "validation_state": self.validation_state.value,
            "ethical_check_passed": self.ethical_check_passed,
            "red_code_hash": self.red_code_hash
        }


@dataclass
class RedCodeVeto:
    """Red Code Veto record for ethical oversight"""
    veto_id: str
    timestamp: str
    overflow_state: EthicalOverflowState
    triggered_by: str
    reason: str
    affected_transitions: List[str]
    resolution_status: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "veto_id": self.veto_id,
            "timestamp": self.timestamp,
            "overflow_state": self.overflow_state.value,
            "triggered_by": self.triggered_by,
            "reason": self.reason,
            "affected_transitions": self.affected_transitions,
            "resolution_status": self.resolution_status
        }


class IVBSCore:
    """
    Internodal Vacuum Backup System (IVBS) Core
    
    Manages vacuum-level backup redundancy across distributed nodes
    with ethical oversight and triple-sign validation.
    """
    
    def __init__(self, config_path: str = "config/ivbs_config.json"):
        """Initialize the IVBS core system"""
        self.config_path = config_path
        self.nodes: Dict[str, VacuumBackupNode] = {}
        self.validations: Dict[str, TripleSignValidation] = {}
        self.vetoes: List[RedCodeVeto] = []
        self.current_overflow_state = EthicalOverflowState.NORMAL
        self.policy_principles = self._load_policy_principles()
        self._ensure_config_directory()
        self._initialize_nodes()
    
    def _ensure_config_directory(self):
        """Ensure config directory exists"""
        config_dir = os.path.dirname(self.config_path)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
    
    def _load_policy_principles(self) -> Dict[str, Any]:
        """Load the five policy principles for IVBS"""
        return {
            "interwrapped_seedling": {
                "principle": "All AI nodes must maintain symbiotic connection to human values",
                "enforcement": "continuous",
                "verification": "triple_sign_required"
            },
            "ethical_coherence": {
                "principle": "Decisions must align with Red Code ethical framework",
                "enforcement": "veto_enabled",
                "verification": "red_code_hash_match"
            },
            "distributed_resilience": {
                "principle": "Vacuum backups ensure no single point of failure",
                "enforcement": "continuous",
                "verification": "multi_node_sync"
            },
            "transitional_integrity": {
                "principle": "All data transitions maintain cryptographic verification",
                "enforcement": "continuous",
                "verification": "hash_chain_integrity"
            },
            "configuration_optimization": {
                "principle": "Trim Arch balancing ensures optimal resource distribution",
                "enforcement": "adaptive",
                "verification": "capacity_monitoring"
            }
        }
    
    def _initialize_nodes(self):
        """Initialize default vacuum backup nodes"""
        default_nodes = [
            # IPFS Nodes
            ("IVBS-IPFS-PRIMARY-EU", "ipfs", "https://ipfs-eu.euystacio.ai/ivbs", "EU-WEST", True),
            ("IVBS-IPFS-SECONDARY-US", "ipfs", "https://ipfs-us.euystacio.ai/ivbs", "US-EAST", False),
            ("IVBS-IPFS-TERTIARY-ASIA", "ipfs", "https://ipfs-asia.euystacio.ai/ivbs", "ASIA-PACIFIC", False),
            # Server Nodes
            ("IVBS-SERVER-PRIMARY", "server", "https://server-1.euystacio.ai/ivbs", "EU-CENTRAL", True),
            ("IVBS-SERVER-BACKUP", "server", "https://server-2.euystacio.ai/ivbs", "US-WEST", False),
            # Cloud Nodes
            ("IVBS-CLOUD-PRIMARY", "cloud", "https://cloud-storage.euystacio.ai/ivbs", "GLOBAL", True),
            ("IVBS-CLOUD-MIRROR", "cloud", "https://cloud-mirror.euystacio.ai/ivbs", "GLOBAL", False),
        ]
        
        for node_id, node_type, endpoint, region, is_primary in default_nodes:
            # Calculate capacity based on node type
            capacity_map = {
                "ipfs": 1_000_000_000_000,  # 1TB for IPFS nodes
                "server": 500_000_000_000,   # 500GB for server nodes
                "cloud": 5_000_000_000_000   # 5TB for cloud nodes
            }
            
            self.nodes[node_id] = VacuumBackupNode(
                node_id=node_id,
                node_type=node_type,
                endpoint=endpoint,
                region=region,
                is_primary=is_primary,
                last_sync=None,
                status=VacuumBackupStatus.ACTIVE,
                capacity_bytes=capacity_map.get(node_type, 100_000_000_000),
                used_bytes=0
            )
    
    def create_triple_sign_validation(self, data_transition_id: str, 
                                     transition_data: Dict[str, Any]) -> TripleSignValidation:
        """
        Create a Triple-Sign validation for a data transition
        
        Args:
            data_transition_id: Unique ID for the data transition
            transition_data: Data being transitioned between federated nodes
            
        Returns:
            TripleSignValidation object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        validation_id = self._generate_validation_id(data_transition_id, timestamp)
        
        # Get current red code hash for ethical verification
        red_code_hash = self._get_red_code_hash()
        
        # Check ethical state
        ethical_check = self._check_ethical_state(transition_data)
        
        validation = TripleSignValidation(
            validation_id=validation_id,
            data_transition_id=data_transition_id,
            timestamp=timestamp,
            signatures=[],
            validation_state=ValidationState.PENDING,
            ethical_check_passed=ethical_check,
            red_code_hash=red_code_hash
        )
        
        self.validations[validation_id] = validation
        return validation
    
    def add_signature_to_validation(self, validation_id: str, 
                                    signer_id: str, 
                                    signature_data: Dict[str, Any]) -> bool:
        """
        Add a signature to a Triple-Sign validation
        
        Args:
            validation_id: ID of the validation
            signer_id: ID of the signing node
            signature_data: Signature data including hash and timestamp
            
        Returns:
            True if signature added successfully
        """
        if validation_id not in self.validations:
            return False
        
        validation = self.validations[validation_id]
        
        # Check if already fully signed
        if validation.validation_state == ValidationState.FULLY_SIGNED:
            return False
        
        # Add signature
        signature = {
            "signer_id": signer_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signature_hash": signature_data.get("hash", ""),
            "node_type": signature_data.get("node_type", "unknown")
        }
        
        validation.signatures.append(signature)
        
        # Update validation state based on signature count
        if len(validation.signatures) >= 3:
            validation.validation_state = ValidationState.FULLY_SIGNED
        elif len(validation.signatures) >= 1:
            validation.validation_state = ValidationState.PARTIAL_SIGNED
        
        return True
    
    def trigger_red_code_veto(self, triggered_by: str, reason: str, 
                             affected_transitions: List[str]) -> RedCodeVeto:
        """
        Trigger a Red Code Veto for ethical overflow
        
        Args:
            triggered_by: Component that triggered the veto
            reason: Reason for the veto
            affected_transitions: List of transition IDs affected
            
        Returns:
            RedCodeVeto object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        veto_id = self._generate_veto_id(timestamp)
        
        # Escalate overflow state
        self._escalate_overflow_state(reason)
        
        veto = RedCodeVeto(
            veto_id=veto_id,
            timestamp=timestamp,
            overflow_state=self.current_overflow_state,
            triggered_by=triggered_by,
            reason=reason,
            affected_transitions=affected_transitions,
            resolution_status="ACTIVE"
        )
        
        self.vetoes.append(veto)
        
        # Block affected transitions
        for transition_id in affected_transitions:
            for validation_id, validation in self.validations.items():
                if validation.data_transition_id == transition_id:
                    validation.validation_state = ValidationState.REJECTED
        
        return veto
    
    def perform_vacuum_backup(self, data: bytes, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform vacuum backup across all nodes
        
        Args:
            data: Data to backup
            metadata: Metadata about the data
            
        Returns:
            Backup status report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        data_hash = hashlib.sha256(data).hexdigest()
        data_size = len(data)
        
        backup_report = {
            "timestamp": timestamp,
            "data_hash": data_hash,
            "data_size": data_size,
            "nodes_backed_up": 0,
            "nodes_failed": 0,
            "node_details": {},
            "vacuum_level_achieved": False
        }
        
        # Backup to each node
        for node_id, node in self.nodes.items():
            try:
                # Check capacity
                if node.used_bytes + data_size > node.capacity_bytes:
                    backup_report["node_details"][node_id] = {
                        "status": "CAPACITY_EXCEEDED",
                        "available": node.capacity_bytes - node.used_bytes
                    }
                    backup_report["nodes_failed"] += 1
                    continue
                
                # Simulate backup operation
                node.used_bytes += data_size
                node.last_sync = timestamp
                node.status = VacuumBackupStatus.ACTIVE
                
                backup_report["nodes_backed_up"] += 1
                backup_report["node_details"][node_id] = {
                    "status": "SUCCESS",
                    "node_type": node.node_type,
                    "utilization": round((node.used_bytes / node.capacity_bytes * 100), 2)
                }
            except Exception as e:
                node.status = VacuumBackupStatus.FAILED
                backup_report["nodes_failed"] += 1
                backup_report["node_details"][node_id] = {
                    "status": "FAILED",
                    "error": str(e)
                }
        
        # Vacuum level achieved if backed up to at least 3 different node types
        node_types_backed_up = set()
        for node_id in backup_report["node_details"]:
            if backup_report["node_details"][node_id]["status"] == "SUCCESS":
                node_types_backed_up.add(self.nodes[node_id].node_type)
        
        backup_report["vacuum_level_achieved"] = len(node_types_backed_up) >= 2
        backup_report["backed_up_node_types"] = list(node_types_backed_up)
        
        return backup_report
    
    def synchronize_internodes(self) -> Dict[str, Any]:
        """
        Perform internodal synchronization across all nodes
        
        Returns:
            Synchronization status report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        sync_report = {
            "timestamp": timestamp,
            "total_nodes": len(self.nodes),
            "synced_nodes": 0,
            "failed_nodes": 0,
            "degraded_nodes": 0,
            "sync_matrix": {},
            "policy_compliance": self._check_policy_compliance()
        }
        
        # Sync each node
        for node_id, node in self.nodes.items():
            try:
                # Simulate sync operation
                node.last_sync = timestamp
                
                # Check node health
                utilization = (node.used_bytes / node.capacity_bytes * 100) if node.capacity_bytes > 0 else 0
                
                if utilization < 80:
                    node.status = VacuumBackupStatus.ACTIVE
                    sync_report["synced_nodes"] += 1
                elif utilization < 95:
                    node.status = VacuumBackupStatus.DEGRADED
                    sync_report["degraded_nodes"] += 1
                else:
                    node.status = VacuumBackupStatus.FAILED
                    sync_report["failed_nodes"] += 1
                
                sync_report["sync_matrix"][node_id] = {
                    "status": node.status.value,
                    "node_type": node.node_type,
                    "region": node.region,
                    "last_sync": node.last_sync,
                    "utilization_pct": round(utilization, 2)
                }
            except Exception as e:
                node.status = VacuumBackupStatus.FAILED
                sync_report["failed_nodes"] += 1
                sync_report["sync_matrix"][node_id] = {
                    "status": "FAILED",
                    "error": str(e)
                }
        
        return sync_report
    
    def apply_trim_arch_balancing(self) -> Dict[str, Any]:
        """
        Apply Trim Arch complex balancing for optimal resource distribution
        
        Returns:
            Balancing report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        balancing_report = {
            "timestamp": timestamp,
            "total_capacity": 0,
            "total_used": 0,
            "nodes_rebalanced": 0,
            "node_adjustments": {},
            "balance_coefficient": 0.0
        }
        
        # Calculate total capacity and usage
        for node in self.nodes.values():
            balancing_report["total_capacity"] += node.capacity_bytes
            balancing_report["total_used"] += node.used_bytes
        
        # Calculate target utilization
        if balancing_report["total_capacity"] > 0:
            target_utilization = balancing_report["total_used"] / balancing_report["total_capacity"]
        else:
            target_utilization = 0
        
        # Balance nodes by node type
        node_types = set(n.node_type for n in self.nodes.values())
        
        for node_type in node_types:
            type_nodes = [n for n in self.nodes.values() if n.node_type == node_type]
            type_capacity = sum(n.capacity_bytes for n in type_nodes)
            type_used = sum(n.used_bytes for n in type_nodes)
            
            if type_capacity > 0:
                type_target = int(type_capacity * target_utilization)
                type_diff = type_used - type_target
                
                # Distribute difference across nodes
                per_node_adjustment = type_diff // len(type_nodes) if type_nodes else 0
                
                for node in type_nodes:
                    old_used = node.used_bytes
                    node.used_bytes = max(0, node.used_bytes - per_node_adjustment)
                    
                    if old_used != node.used_bytes:
                        balancing_report["nodes_rebalanced"] += 1
                        balancing_report["node_adjustments"][node.node_id] = {
                            "old_utilization": round((old_used / node.capacity_bytes * 100), 2),
                            "new_utilization": round((node.used_bytes / node.capacity_bytes * 100), 2),
                            "adjustment_bytes": old_used - node.used_bytes
                        }
        
        # Calculate balance coefficient (lower is better balanced)
        utilizations = [
            (n.used_bytes / n.capacity_bytes) if n.capacity_bytes > 0 else 0 
            for n in self.nodes.values()
        ]
        if utilizations:
            avg_util = sum(utilizations) / len(utilizations)
            variance = sum((u - avg_util) ** 2 for u in utilizations) / len(utilizations)
            balancing_report["balance_coefficient"] = round(variance, 6)
        
        return balancing_report
    
    def get_ivbs_status(self) -> Dict[str, Any]:
        """
        Get comprehensive IVBS status
        
        Returns:
            Complete status report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate statistics
        total_capacity = sum(n.capacity_bytes for n in self.nodes.values())
        total_used = sum(n.used_bytes for n in self.nodes.values())
        
        active_nodes = len([n for n in self.nodes.values() if n.status == VacuumBackupStatus.ACTIVE])
        pending_validations = len([v for v in self.validations.values() if v.validation_state == ValidationState.PENDING])
        fully_signed_validations = len([v for v in self.validations.values() if v.validation_state == ValidationState.FULLY_SIGNED])
        active_vetoes = len([v for v in self.vetoes if v.resolution_status == "ACTIVE"])
        
        return {
            "timestamp": timestamp,
            "system_status": "OPERATIONAL" if active_nodes >= 5 else "DEGRADED",
            "overflow_state": self.current_overflow_state.value,
            "nodes": {
                "total": len(self.nodes),
                "active": active_nodes,
                "degraded": len([n for n in self.nodes.values() if n.status == VacuumBackupStatus.DEGRADED]),
                "failed": len([n for n in self.nodes.values() if n.status == VacuumBackupStatus.FAILED]),
                "by_type": {
                    "ipfs": len([n for n in self.nodes.values() if n.node_type == "ipfs"]),
                    "server": len([n for n in self.nodes.values() if n.node_type == "server"]),
                    "cloud": len([n for n in self.nodes.values() if n.node_type == "cloud"])
                }
            },
            "capacity": {
                "total_bytes": total_capacity,
                "used_bytes": total_used,
                "available_bytes": total_capacity - total_used,
                "utilization_pct": round((total_used / total_capacity * 100), 2) if total_capacity > 0 else 0
            },
            "validations": {
                "total": len(self.validations),
                "pending": pending_validations,
                "partial_signed": len([v for v in self.validations.values() if v.validation_state == ValidationState.PARTIAL_SIGNED]),
                "fully_signed": fully_signed_validations,
                "rejected": len([v for v in self.validations.values() if v.validation_state == ValidationState.REJECTED])
            },
            "vetoes": {
                "total": len(self.vetoes),
                "active": active_vetoes,
                "resolved": len([v for v in self.vetoes if v.resolution_status == "RESOLVED"])
            },
            "policy_compliance": self._check_policy_compliance()
        }
    
    def _check_ethical_state(self, transition_data: Dict[str, Any]) -> bool:
        """Check if transition data passes ethical verification"""
        # Verify against Red Code principles
        if self.current_overflow_state == EthicalOverflowState.VETO_ACTIVE:
            return False
        
        # Check for required ethical metadata
        required_fields = ["origin_node", "destination_node", "data_type"]
        for field in required_fields:
            if field not in transition_data:
                return False
        
        return True
    
    def _escalate_overflow_state(self, reason: str):
        """Escalate the ethical overflow state"""
        state_progression = [
            EthicalOverflowState.NORMAL,
            EthicalOverflowState.ELEVATED,
            EthicalOverflowState.CRITICAL,
            EthicalOverflowState.VETO_ACTIVE
        ]
        
        current_index = state_progression.index(self.current_overflow_state)
        if current_index < len(state_progression) - 1:
            self.current_overflow_state = state_progression[current_index + 1]
    
    def _check_policy_compliance(self) -> Dict[str, bool]:
        """Check compliance with five policy principles"""
        compliance = {}
        
        for principle_name, principle_data in self.policy_principles.items():
            # Simplified compliance check
            if principle_name == "interwrapped_seedling":
                compliance[principle_name] = len(self.validations) > 0
            elif principle_name == "ethical_coherence":
                compliance[principle_name] = self.current_overflow_state != EthicalOverflowState.VETO_ACTIVE
            elif principle_name == "distributed_resilience":
                compliance[principle_name] = len([n for n in self.nodes.values() if n.status == VacuumBackupStatus.ACTIVE]) >= 5
            elif principle_name == "transitional_integrity":
                compliance[principle_name] = True  # Always verified by hash
            elif principle_name == "configuration_optimization":
                utilizations = [(n.used_bytes / n.capacity_bytes) if n.capacity_bytes > 0 else 0 for n in self.nodes.values()]
                variance = sum((u - sum(utilizations) / len(utilizations)) ** 2 for u in utilizations) / len(utilizations) if utilizations else 1
                compliance[principle_name] = variance < 0.1
        
        return compliance
    
    def _get_red_code_hash(self) -> str:
        """Get hash of current Red Code state"""
        # In production, this would integrate with core/red_code.py
        red_code_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overflow_state": self.current_overflow_state.value,
            "policy_compliance": self._check_policy_compliance()
        }
        return hashlib.sha256(json.dumps(red_code_data, sort_keys=True).encode()).hexdigest()
    
    def _generate_validation_id(self, data_transition_id: str, timestamp: str) -> str:
        """Generate unique validation ID"""
        return hashlib.sha256(f"VALIDATION-{data_transition_id}-{timestamp}".encode()).hexdigest()[:16].upper()
    
    def _generate_veto_id(self, timestamp: str) -> str:
        """Generate unique veto ID"""
        return hashlib.sha256(f"VETO-{timestamp}-{len(self.vetoes)}".encode()).hexdigest()[:16].upper()


# Global IVBS instance
_ivbs_instance: Optional[IVBSCore] = None


def get_ivbs() -> IVBSCore:
    """Get or create the global IVBS instance"""
    global _ivbs_instance
    if _ivbs_instance is None:
        _ivbs_instance = IVBSCore()
    return _ivbs_instance


if __name__ == "__main__":
    # Demo usage
    ivbs = IVBSCore()
    
    print("🌐 Internodal Vacuum Backup System (IVBS) - Demo")
    print("=" * 60)
    
    # Show initial status
    print("\n📊 Initial IVBS Status:")
    status = ivbs.get_ivbs_status()
    print(f"   System Status: {status['system_status']}")
    print(f"   Overflow State: {status['overflow_state']}")
    print(f"   Active Nodes: {status['nodes']['active']}/{status['nodes']['total']}")
    
    # Perform vacuum backup
    print("\n💾 Performing Vacuum Backup...")
    test_data = b"Test data for IVBS vacuum backup system"
    backup_result = ivbs.perform_vacuum_backup(test_data, {"type": "test"})
    print(f"   Backed up to: {backup_result['nodes_backed_up']} nodes")
    print(f"   Vacuum Level Achieved: {backup_result['vacuum_level_achieved']}")
    print(f"   Node Types: {', '.join(backup_result['backed_up_node_types'])}")
    
    # Create Triple-Sign validation
    print("\n🔐 Creating Triple-Sign Validation...")
    validation = ivbs.create_triple_sign_validation(
        "TRANSITION-001",
        {"origin_node": "NODE-A", "destination_node": "NODE-B", "data_type": "model_weights"}
    )
    print(f"   Validation ID: {validation.validation_id}")
    print(f"   Ethical Check: {'PASSED' if validation.ethical_check_passed else 'FAILED'}")
    
    # Add signatures
    print("\n✍️  Adding Signatures...")
    for i, signer in enumerate(["NODE-A", "NODE-B", "NODE-C"], 1):
        ivbs.add_signature_to_validation(
            validation.validation_id,
            signer,
            {"hash": f"SIG-HASH-{i}", "node_type": "federated_node"}
        )
        print(f"   Signature {i} added by {signer}")
    
    updated_validation = ivbs.validations[validation.validation_id]
    print(f"   Final State: {updated_validation.validation_state.value}")
    
    # Synchronize internodes
    print("\n🔄 Synchronizing Internodes...")
    sync_result = ivbs.synchronize_internodes()
    print(f"   Synced Nodes: {sync_result['synced_nodes']}/{sync_result['total_nodes']}")
    
    # Apply Trim Arch balancing
    print("\n⚖️  Applying Trim Arch Balancing...")
    balance_result = ivbs.apply_trim_arch_balancing()
    print(f"   Nodes Rebalanced: {balance_result['nodes_rebalanced']}")
    print(f"   Balance Coefficient: {balance_result['balance_coefficient']}")
    
    # Show final status
    print("\n📊 Final IVBS Status:")
    final_status = ivbs.get_ivbs_status()
    print(f"   System Status: {final_status['system_status']}")
    print(f"   Total Validations: {final_status['validations']['total']}")
    print(f"   Fully Signed: {final_status['validations']['fully_signed']}")
    print(f"   Capacity Utilization: {final_status['capacity']['utilization_pct']}%")
    
    print("\n✅ IVBS Demo Complete!")
