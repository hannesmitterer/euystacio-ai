"""
ivbs_integration.py
Integration layer between IVBS and existing Euystacio AI systems

This module provides integration points between:
- IVBS Core and Red Code System
- IVBS and IPFS Integrity Manager
- IVBS and Backup Systems
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Import IVBS components
from core.ivbs_core import IVBSCore, get_ivbs, EthicalOverflowState, ValidationState

# Import existing systems
try:
    from core.red_code import red_code_system
    RED_CODE_AVAILABLE = True
except ImportError:
    RED_CODE_AVAILABLE = False
    red_code_system = None

try:
    from core.ipfs_integrity import get_ipfs_manager
    IPFS_AVAILABLE = True
except ImportError:
    IPFS_AVAILABLE = False
    get_ipfs_manager = None


class IVBSIntegration:
    """
    Integration layer for IVBS with existing Euystacio AI systems
    """
    
    def __init__(self):
        """Initialize the integration layer"""
        self.ivbs = get_ivbs()
        self.red_code = red_code_system if RED_CODE_AVAILABLE else None
        self.ipfs_manager = get_ipfs_manager() if IPFS_AVAILABLE else None
        self.integration_log = []
    
    def sync_with_red_code(self) -> Dict[str, Any]:
        """
        Synchronize IVBS with Red Code system
        
        Returns:
            Synchronization report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        sync_report = {
            "timestamp": timestamp,
            "red_code_available": RED_CODE_AVAILABLE,
            "sync_successful": False,
            "overflow_state_synced": False,
            "ethical_check_enabled": False
        }
        
        if not RED_CODE_AVAILABLE or not self.red_code:
            sync_report["message"] = "Red Code system not available"
            return sync_report
        
        try:
            # Get current Red Code state
            red_code_state = self.red_code.get_red_code()
            
            # Sync overflow state based on Red Code guardian mode
            if red_code_state.get("guardian_mode", False):
                if self.ivbs.current_overflow_state == EthicalOverflowState.NORMAL:
                    self.ivbs.current_overflow_state = EthicalOverflowState.ELEVATED
                    sync_report["overflow_state_synced"] = True
                    sync_report["action"] = "Elevated overflow state due to Red Code guardian mode"
            
            # Check for Red Code dissonance
            mutation_logic = red_code_state.get("mutation_logic", {})
            dissonance_tracking = mutation_logic.get("dissonance_tracking", [])
            
            if len(dissonance_tracking) > 0:
                # Check for recent high-intensity concerns
                recent_concerns = [
                    d for d in dissonance_tracking 
                    if d.get("tutor_attention_needed", False)
                ]
                
                if len(recent_concerns) > 3:
                    # Trigger Red Code Veto
                    veto = self.ivbs.trigger_red_code_veto(
                        triggered_by="RED_CODE_INTEGRATION",
                        reason=f"Multiple Red Code dissonance events detected ({len(recent_concerns)})",
                        affected_transitions=[]
                    )
                    sync_report["veto_triggered"] = True
                    sync_report["veto_id"] = veto.veto_id
            
            sync_report["sync_successful"] = True
            sync_report["ethical_check_enabled"] = True
            sync_report["red_code_symbiosis_level"] = red_code_state.get("symbiosis_level", 0.1)
            
            self._log_integration_event("RED_CODE_SYNC", sync_report)
            
        except Exception as e:
            sync_report["error"] = str(e)
        
        return sync_report
    
    def backup_to_ipfs_integration(self, data: bytes, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform integrated backup to both IVBS and IPFS Integrity Manager
        
        Args:
            data: Data to backup
            metadata: Metadata about the data
            
        Returns:
            Combined backup report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        combined_report = {
            "timestamp": timestamp,
            "ivbs_backup": None,
            "ipfs_backup": None,
            "integrated_success": False
        }
        
        # Perform IVBS vacuum backup
        try:
            ivbs_result = self.ivbs.perform_vacuum_backup(data, metadata)
            combined_report["ivbs_backup"] = ivbs_result
            
            # Check if IPFS manager is available
            if IPFS_AVAILABLE and self.ipfs_manager:
                # Add content to IPFS
                content_type = metadata.get("content_type", "application/octet-stream")
                ipfs_content = self.ipfs_manager.add_content(data, content_type, metadata)
                
                combined_report["ipfs_backup"] = {
                    "cid": ipfs_content.cid,
                    "pinned_nodes": ipfs_content.pinned_nodes,
                    "integrity_hash": ipfs_content.integrity_hash
                }
                
                # Verify IPFS integrity
                ipfs_audit = self.ipfs_manager.verify_content_integrity(ipfs_content.cid)
                combined_report["ipfs_integrity"] = {
                    "ipfs_status": ipfs_audit.ipfs_status.value,
                    "saul_status": ipfs_audit.saul_status.value,
                    "cross_verification": ipfs_audit.cross_verification
                }
            
            # Determine integrated success
            ivbs_success = ivbs_result.get("vacuum_level_achieved", False)
            ipfs_success = combined_report["ipfs_backup"] is not None if IPFS_AVAILABLE else True
            
            combined_report["integrated_success"] = ivbs_success and ipfs_success
            
            self._log_integration_event("INTEGRATED_BACKUP", combined_report)
            
        except Exception as e:
            combined_report["error"] = str(e)
        
        return combined_report
    
    def validate_federated_transition_with_red_code(
        self, 
        transition_id: str, 
        transition_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate a federated learning transition with integrated Red Code checks
        
        Args:
            transition_id: Unique transition ID
            transition_data: Transition data including origin, destination, data
            
        Returns:
            Validation result with Red Code compliance
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        validation_result = {
            "timestamp": timestamp,
            "transition_id": transition_id,
            "red_code_check": None,
            "triple_sign_validation": None,
            "approved": False
        }
        
        try:
            # Perform Red Code ethical check
            if RED_CODE_AVAILABLE and self.red_code:
                red_code_state = self.red_code.get_red_code()
                
                red_code_check = {
                    "guardian_mode": red_code_state.get("guardian_mode", False),
                    "symbiosis_level": red_code_state.get("symbiosis_level", 0.1),
                    "sentimento_rhythm": red_code_state.get("sentimento_rhythm", True),
                    "passed": True
                }
                
                # Check if guardian mode blocks transition
                if red_code_state.get("guardian_mode", False):
                    data_type = transition_data.get("data_type", "")
                    if data_type in ["sensitive", "critical"]:
                        red_code_check["passed"] = False
                        red_code_check["reason"] = "Guardian mode blocks sensitive transitions"
                
                validation_result["red_code_check"] = red_code_check
            else:
                validation_result["red_code_check"] = {"passed": True, "unavailable": True}
            
            # Create Triple-Sign validation
            validation = self.ivbs.create_triple_sign_validation(
                transition_id,
                transition_data
            )
            
            validation_result["triple_sign_validation"] = {
                "validation_id": validation.validation_id,
                "ethical_check_passed": validation.ethical_check_passed,
                "red_code_hash": validation.red_code_hash,
                "state": validation.validation_state.value
            }
            
            # Determine approval
            red_code_approved = validation_result["red_code_check"]["passed"]
            ethical_check_approved = validation.ethical_check_passed
            
            validation_result["approved"] = red_code_approved and ethical_check_approved
            
            if not validation_result["approved"]:
                # Trigger veto if not approved
                veto = self.ivbs.trigger_red_code_veto(
                    triggered_by="INTEGRATED_VALIDATION",
                    reason="Red Code or ethical check failed",
                    affected_transitions=[transition_id]
                )
                validation_result["veto_triggered"] = True
                validation_result["veto_id"] = veto.veto_id
            
            self._log_integration_event("FEDERATED_VALIDATION", validation_result)
            
        except Exception as e:
            validation_result["error"] = str(e)
        
        return validation_result
    
    def get_integrated_status(self) -> Dict[str, Any]:
        """
        Get comprehensive integrated status across all systems
        
        Returns:
            Combined status report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        integrated_status = {
            "timestamp": timestamp,
            "ivbs_status": None,
            "red_code_status": None,
            "ipfs_status": None,
            "integration_health": "UNKNOWN"
        }
        
        # Get IVBS status
        try:
            integrated_status["ivbs_status"] = self.ivbs.get_ivbs_status()
        except Exception as e:
            integrated_status["ivbs_error"] = str(e)
        
        # Get Red Code status
        if RED_CODE_AVAILABLE and self.red_code:
            try:
                red_code_state = self.red_code.get_red_code()
                integrated_status["red_code_status"] = {
                    "core_truth": red_code_state.get("core_truth", ""),
                    "symbiosis_level": red_code_state.get("symbiosis_level", 0.1),
                    "guardian_mode": red_code_state.get("guardian_mode", False),
                    "sentimento_rhythm": red_code_state.get("sentimento_rhythm", True),
                    "harmony_sync": red_code_state.get("harmony_sync", {})
                }
            except Exception as e:
                integrated_status["red_code_error"] = str(e)
        
        # Get IPFS status
        if IPFS_AVAILABLE and self.ipfs_manager:
            try:
                ipfs_status = self.ipfs_manager.get_api_status()
                integrated_status["ipfs_status"] = ipfs_status
            except Exception as e:
                integrated_status["ipfs_error"] = str(e)
        
        # Determine integration health
        ivbs_healthy = (
            integrated_status.get("ivbs_status", {}).get("system_status") == "OPERATIONAL"
        )
        red_code_healthy = (
            not integrated_status.get("red_code_error") 
            if RED_CODE_AVAILABLE else True
        )
        ipfs_healthy = (
            integrated_status.get("ipfs_status", {}).get("status") == "OPERATIONAL"
            if IPFS_AVAILABLE else True
        )
        
        if ivbs_healthy and red_code_healthy and ipfs_healthy:
            integrated_status["integration_health"] = "HEALTHY"
        elif ivbs_healthy:
            integrated_status["integration_health"] = "DEGRADED"
        else:
            integrated_status["integration_health"] = "CRITICAL"
        
        return integrated_status
    
    def perform_integrated_sync(self) -> Dict[str, Any]:
        """
        Perform comprehensive sync across all integrated systems
        
        Returns:
            Sync report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        sync_report = {
            "timestamp": timestamp,
            "ivbs_sync": None,
            "red_code_sync": None,
            "ipfs_sync": None,
            "overall_success": False
        }
        
        # Sync IVBS nodes
        try:
            sync_report["ivbs_sync"] = self.ivbs.synchronize_internodes()
        except Exception as e:
            sync_report["ivbs_sync_error"] = str(e)
        
        # Sync with Red Code
        try:
            sync_report["red_code_sync"] = self.sync_with_red_code()
        except Exception as e:
            sync_report["red_code_sync_error"] = str(e)
        
        # Sync IPFS nodes
        if IPFS_AVAILABLE and self.ipfs_manager:
            try:
                sync_report["ipfs_sync"] = self.ipfs_manager.sync_nodes()
            except Exception as e:
                sync_report["ipfs_sync_error"] = str(e)
        
        # Determine overall success
        ivbs_success = sync_report.get("ivbs_sync", {}).get("synced_nodes", 0) > 0
        red_code_success = sync_report.get("red_code_sync", {}).get("sync_successful", False)
        ipfs_success = (
            sync_report.get("ipfs_sync", {}).get("nodes_synced", 0) > 0
            if IPFS_AVAILABLE else True
        )
        
        sync_report["overall_success"] = ivbs_success and red_code_success and ipfs_success
        
        self._log_integration_event("INTEGRATED_SYNC", sync_report)
        
        return sync_report
    
    def _log_integration_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log integration event"""
        self.integration_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": event_data
        })
        
        # Keep only last 100 events
        if len(self.integration_log) > 100:
            self.integration_log = self.integration_log[-100:]


# Global integration instance
_integration_instance: Optional[IVBSIntegration] = None


def get_ivbs_integration() -> IVBSIntegration:
    """Get or create the global IVBS integration instance"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = IVBSIntegration()
    return _integration_instance


if __name__ == "__main__":
    # Demo integrated functionality
    integration = IVBSIntegration()
    
    print("🔗 IVBS Integration Layer - Demo")
    print("=" * 60)
    
    # Get integrated status
    print("\n📊 Integrated System Status:")
    status = integration.get_integrated_status()
    print(f"   Integration Health: {status['integration_health']}")
    if status.get("ivbs_status"):
        print(f"   IVBS Status: {status['ivbs_status']['system_status']}")
    if status.get("red_code_status"):
        print(f"   Red Code Available: {status['red_code_status'] is not None}")
    
    # Sync with Red Code
    print("\n🔄 Syncing with Red Code:")
    red_code_sync = integration.sync_with_red_code()
    print(f"   Sync Successful: {red_code_sync.get('sync_successful', False)}")
    print(f"   Red Code Available: {red_code_sync['red_code_available']}")
    
    # Perform integrated backup
    print("\n💾 Performing Integrated Backup:")
    test_data = b"Integrated backup test data"
    backup_result = integration.backup_to_ipfs_integration(
        test_data,
        {"type": "test", "content_type": "text/plain"}
    )
    print(f"   Integrated Success: {backup_result['integrated_success']}")
    if backup_result.get("ivbs_backup"):
        print(f"   IVBS Nodes: {backup_result['ivbs_backup']['nodes_backed_up']}")
    
    # Validate federated transition
    print("\n🔐 Validating Federated Transition:")
    transition_data = {
        "origin_node": "NODE-A",
        "destination_node": "NODE-B",
        "data_type": "model_weights"
    }
    validation_result = integration.validate_federated_transition_with_red_code(
        "INTEGRATED-TRANS-001",
        transition_data
    )
    print(f"   Approved: {validation_result['approved']}")
    if validation_result.get("red_code_check"):
        print(f"   Red Code Check: {validation_result['red_code_check']['passed']}")
    
    # Perform integrated sync
    print("\n🔄 Performing Integrated Sync:")
    sync_result = integration.perform_integrated_sync()
    print(f"   Overall Success: {sync_result['overall_success']}")
    
    print("\n✅ Integration Demo Complete!")
