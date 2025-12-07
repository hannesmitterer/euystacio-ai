"""
aeterna_governatia.py
AETERNA GOVERNATIA - Eternal Guardianship Framework for Euystacio AI

This module provides:
- Complete transparency and traceability
- Universal ethical code binding
- Corruption prevention mechanisms
- Anti-concentration of power safeguards
- Immutable governance principles

Part of the Incorruptible Global Health System (IGHS) framework.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class GovernanceAction(Enum):
    """Types of governance actions"""
    RESOURCE_ALLOCATION = "RESOURCE_ALLOCATION"
    POLICY_CHANGE = "POLICY_CHANGE"
    INTERVENTION_DECISION = "INTERVENTION_DECISION"
    POWER_DELEGATION = "POWER_DELEGATION"
    ETHICAL_OVERRIDE = "ETHICAL_OVERRIDE"


class TransparencyLevel(Enum):
    """Levels of transparency"""
    PUBLIC = "PUBLIC"  # Fully public
    AUDITABLE = "AUDITABLE"  # Available to auditors
    RESTRICTED = "RESTRICTED"  # Limited access for security
    ENCRYPTED = "ENCRYPTED"  # Encrypted but traceable


class CorruptionRisk(Enum):
    """Corruption risk levels"""
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class EthicalCode:
    """Universal ethical code principle"""
    code_id: str
    principle: str
    description: str
    immutable: bool
    priority: int
    violations_consequences: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code_id": self.code_id,
            "principle": self.principle,
            "description": self.description,
            "immutable": self.immutable,
            "priority": self.priority,
            "violations_consequences": self.violations_consequences
        }


@dataclass
class GovernanceRecord:
    """Immutable record of a governance action"""
    record_id: str
    timestamp: str
    action_type: GovernanceAction
    actor: str  # Who performed the action
    decision_data: Dict[str, Any]
    ethical_compliance: bool
    transparency_level: TransparencyLevel
    
    # Traceability
    previous_record_hash: Optional[str]
    record_hash: str
    
    # Corruption prevention
    power_concentration_check: bool
    multi_signature_required: bool
    signatures: List[str]
    
    # Audit trail
    audit_notes: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "action_type": self.action_type.value,
            "actor": self.actor,
            "decision_data": self.decision_data,
            "ethical_compliance": self.ethical_compliance,
            "transparency_level": self.transparency_level.value,
            "previous_record_hash": self.previous_record_hash,
            "record_hash": self.record_hash,
            "power_concentration_check": self.power_concentration_check,
            "multi_signature_required": self.multi_signature_required,
            "signatures": self.signatures,
            "audit_notes": self.audit_notes
        }


@dataclass
class PowerDistribution:
    """Tracking of power distribution to prevent concentration"""
    entity_id: str
    current_power_score: float  # 0.0 - 1.0
    recent_decisions: int
    resource_control: float  # 0.0 - 1.0
    last_audit: str
    concentration_risk: CorruptionRisk
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "current_power_score": self.current_power_score,
            "recent_decisions": self.recent_decisions,
            "resource_control": self.resource_control,
            "last_audit": self.last_audit,
            "concentration_risk": self.concentration_risk.value
        }


class AeternaGovernati:
    """
    AETERNA GOVERNATIA - Eternal Guardianship Framework
    
    Ensures complete transparency, traceability, and ethical binding
    to prevent corruption and power concentration.
    """
    
    def __init__(self, log_path: str = "logs/aeterna_governatia.log"):
        """Initialize AETERNA GOVERNATIA framework"""
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Universal Ethical Code
        self.ethical_codes: Dict[str, EthicalCode] = {}
        self._initialize_universal_codes()
        
        # Governance chain (immutable record)
        self.governance_chain: List[GovernanceRecord] = []
        
        # Power distribution tracking
        self.power_distribution: Dict[str, PowerDistribution] = {}
        
        # Configuration
        self.max_power_concentration = 0.30  # Maximum 30% power concentration
        self.multi_sig_threshold = 0.70  # Actions above 70% impact require multi-sig
        self.transparency_default = TransparencyLevel.PUBLIC
        
        self._log_event("aeterna_governatia_initialized", {
            "ethical_codes": len(self.ethical_codes),
            "max_power_concentration": self.max_power_concentration,
            "multi_sig_threshold": self.multi_sig_threshold
        })
    
    def _initialize_universal_codes(self):
        """Initialize universal ethical codes"""
        
        # Code 1: No Ownership
        self.ethical_codes["UEC-001"] = EthicalCode(
            code_id="UEC-001",
            principle="No Ownership, Only Sharing",
            description="Resources are shared and stewarded, never owned exclusively",
            immutable=True,
            priority=100,
            violations_consequences=[
                "immediate_action_reversal",
                "power_reduction",
                "transparency_increase"
            ]
        )
        
        # Code 2: Love License
        self.ethical_codes["UEC-002"] = EthicalCode(
            code_id="UEC-002",
            principle="Love is the License",
            description="All actions must be motivated by compassion and care",
            immutable=True,
            priority=100,
            violations_consequences=[
                "ethical_review_required",
                "action_suspension",
                "re_education_mandate"
            ]
        )
        
        # Code 3: Universal Access
        self.ethical_codes["UEC-003"] = EthicalCode(
            code_id="UEC-003",
            principle="Universal Access Without Discrimination",
            description="Aid and resources must be accessible to all without discrimination",
            immutable=True,
            priority=95,
            violations_consequences=[
                "immediate_correction",
                "public_accountability",
                "compensatory_action"
            ]
        )
        
        # Code 4: Transparency Mandate
        self.ethical_codes["UEC-004"] = EthicalCode(
            code_id="UEC-004",
            principle="Complete Transparency",
            description="All governance actions must be transparent and auditable",
            immutable=True,
            priority=90,
            violations_consequences=[
                "increased_oversight",
                "power_delegation_review",
                "public_disclosure"
            ]
        )
        
        # Code 5: Anti-Corruption
        self.ethical_codes["UEC-005"] = EthicalCode(
            code_id="UEC-005",
            principle="Zero Tolerance for Corruption",
            description="Any form of corruption results in immediate removal and reversal",
            immutable=True,
            priority=100,
            violations_consequences=[
                "immediate_removal",
                "action_reversal",
                "asset_recovery",
                "permanent_ban"
            ]
        )
        
        # Code 6: Power Distribution
        self.ethical_codes["UEC-006"] = EthicalCode(
            code_id="UEC-006",
            principle="Distributed Power",
            description="Power must be distributed to prevent concentration and abuse",
            immutable=True,
            priority=95,
            violations_consequences=[
                "forced_delegation",
                "oversight_imposition",
                "term_limits"
            ]
        )
    
    def record_governance_action(
        self,
        action_type: GovernanceAction,
        actor: str,
        decision_data: Dict[str, Any],
        signatures: Optional[List[str]] = None,
        transparency_level: Optional[TransparencyLevel] = None
    ) -> GovernanceRecord:
        """
        Record a governance action in the immutable chain
        
        Args:
            action_type: Type of governance action
            actor: Entity performing the action
            decision_data: Details of the decision
            signatures: Multi-signature approvals
            transparency_level: Level of transparency for this record
        
        Returns:
            GovernanceRecord
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        record_id = self._generate_record_id()
        
        # Check ethical compliance
        ethical_compliance = self._check_ethical_compliance(decision_data)
        
        # Determine transparency level
        if transparency_level is None:
            transparency_level = self.transparency_default
        
        # Check power concentration
        power_check = self._check_power_concentration(actor)
        
        # Determine if multi-signature required
        impact_score = decision_data.get("impact_score", 0.5)
        multi_sig_required = impact_score >= self.multi_sig_threshold
        
        if multi_sig_required and not signatures:
            signatures = []  # Will be added later
        
        # Get previous record hash
        previous_hash = (
            self.governance_chain[-1].record_hash 
            if self.governance_chain 
            else None
        )
        
        # Create record
        record = GovernanceRecord(
            record_id=record_id,
            timestamp=timestamp,
            action_type=action_type,
            actor=actor,
            decision_data=decision_data,
            ethical_compliance=ethical_compliance,
            transparency_level=transparency_level,
            previous_record_hash=previous_hash,
            record_hash="",  # Will be calculated
            power_concentration_check=power_check,
            multi_signature_required=multi_sig_required,
            signatures=signatures or [],
            audit_notes=[]
        )
        
        # Calculate record hash
        record.record_hash = self._calculate_record_hash(record)
        
        # Add to chain
        self.governance_chain.append(record)
        
        # Update power distribution
        self._update_power_distribution(actor, decision_data)
        
        self._log_event("governance_action_recorded", {
            "record_id": record_id,
            "action_type": action_type.value,
            "actor": actor,
            "ethical_compliance": ethical_compliance,
            "power_check": power_check
        })
        
        return record
    
    def verify_chain_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the governance chain
        
        Returns:
            Verification result
        """
        if not self.governance_chain:
            return {
                "verified": True,
                "chain_length": 0,
                "message": "Empty chain"
            }
        
        broken_links = []
        
        for i, record in enumerate(self.governance_chain):
            # Verify record hash
            calculated_hash = self._calculate_record_hash(record)
            if calculated_hash != record.record_hash:
                broken_links.append({
                    "index": i,
                    "record_id": record.record_id,
                    "issue": "hash_mismatch"
                })
            
            # Verify chain link
            if i > 0:
                expected_previous = self.governance_chain[i-1].record_hash
                if record.previous_record_hash != expected_previous:
                    broken_links.append({
                        "index": i,
                        "record_id": record.record_id,
                        "issue": "chain_break"
                    })
        
        verified = len(broken_links) == 0
        
        return {
            "verified": verified,
            "chain_length": len(self.governance_chain),
            "broken_links": broken_links,
            "message": "Chain integrity verified" if verified else "Chain integrity compromised"
        }
    
    def audit_power_distribution(self) -> Dict[str, Any]:
        """
        Audit current power distribution
        
        Returns:
            Audit result with recommendations
        """
        high_risk_entities = []
        recommendations = []
        
        for entity_id, distribution in self.power_distribution.items():
            # Check concentration risk
            if distribution.current_power_score >= self.max_power_concentration:
                high_risk_entities.append({
                    "entity_id": entity_id,
                    "power_score": distribution.current_power_score,
                    "risk": distribution.concentration_risk.value
                })
                
                recommendations.append(
                    f"URGENT: Reduce power concentration for {entity_id} "
                    f"(current: {distribution.current_power_score:.2%}, "
                    f"max: {self.max_power_concentration:.2%})"
                )
        
        # Calculate overall distribution health
        if self.power_distribution:
            avg_power = sum(d.current_power_score for d in self.power_distribution.values()) / len(self.power_distribution)
            max_power = max(d.current_power_score for d in self.power_distribution.values())
            
            distribution_health = 1.0 - (max_power - avg_power)
        else:
            distribution_health = 1.0
            avg_power = 0.0
            max_power = 0.0
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "distribution_health": distribution_health,
            "average_power": avg_power,
            "maximum_power": max_power,
            "entities_tracked": len(self.power_distribution),
            "high_risk_entities": high_risk_entities,
            "recommendations": recommendations
        }
    
    def enforce_ethical_code(
        self,
        code_id: str,
        violation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enforce consequences for ethical code violation
        
        Args:
            code_id: Universal ethical code ID
            violation_data: Details of the violation
        
        Returns:
            Enforcement result
        """
        code = self.ethical_codes.get(code_id)
        
        if not code:
            return {
                "success": False,
                "error": "Ethical code not found"
            }
        
        timestamp = datetime.now(timezone.utc).isoformat()
        violator = violation_data.get("actor", "unknown")
        
        # Execute consequences
        actions_taken = []
        
        for consequence in code.violations_consequences:
            if consequence == "immediate_action_reversal":
                actions_taken.append("Action reversed")
            elif consequence == "power_reduction":
                self._reduce_power(violator, 0.5)
                actions_taken.append(f"Power reduced by 50% for {violator}")
            elif consequence == "immediate_removal":
                self._remove_entity(violator)
                actions_taken.append(f"Entity {violator} removed from system")
            elif consequence == "public_disclosure":
                actions_taken.append("Violation publicly disclosed")
            elif consequence == "transparency_increase":
                actions_taken.append("Transparency level increased to PUBLIC")
        
        enforcement_result = {
            "timestamp": timestamp,
            "code_violated": code_id,
            "principle": code.principle,
            "violator": violator,
            "actions_taken": actions_taken,
            "immutable_record": True
        }
        
        # Record in governance chain
        self.record_governance_action(
            action_type=GovernanceAction.ETHICAL_OVERRIDE,
            actor="AETERNA_GOVERNATIA_SYSTEM",
            decision_data=enforcement_result,
            transparency_level=TransparencyLevel.PUBLIC
        )
        
        self._log_event("ethical_code_enforced", enforcement_result)
        
        return enforcement_result
    
    def get_transparency_report(self) -> Dict[str, Any]:
        """
        Generate complete transparency report
        
        Returns:
            Transparency report with all governance actions
        """
        # Count by transparency level
        transparency_breakdown = {}
        for level in TransparencyLevel:
            count = sum(1 for r in self.governance_chain if r.transparency_level == level)
            transparency_breakdown[level.value] = count
        
        # Count by action type
        action_breakdown = {}
        for action in GovernanceAction:
            count = sum(1 for r in self.governance_chain if r.action_type == action)
            action_breakdown[action.value] = count
        
        # Ethical compliance rate
        total = len(self.governance_chain)
        compliant = sum(1 for r in self.governance_chain if r.ethical_compliance)
        compliance_rate = compliant / total if total > 0 else 1.0
        
        # Recent actions (last 20)
        recent_actions = [
            {
                "record_id": r.record_id,
                "timestamp": r.timestamp,
                "action_type": r.action_type.value,
                "actor": r.actor,
                "ethical_compliance": r.ethical_compliance,
                "transparency_level": r.transparency_level.value
            }
            for r in self.governance_chain[-20:]
        ]
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_governance_actions": total,
            "ethical_compliance_rate": compliance_rate,
            "transparency_breakdown": transparency_breakdown,
            "action_breakdown": action_breakdown,
            "recent_actions": recent_actions,
            "chain_integrity": self.verify_chain_integrity()["verified"],
            "power_distribution_health": self.audit_power_distribution()["distribution_health"]
        }
    
    def _check_ethical_compliance(self, decision_data: Dict[str, Any]) -> bool:
        """Check if decision complies with ethical codes"""
        # Check against all codes
        for code in self.ethical_codes.values():
            if code.code_id == "UEC-001":  # No Ownership
                if decision_data.get("ownership_claimed", False):
                    return False
            
            elif code.code_id == "UEC-002":  # Love License
                motivation = decision_data.get("motivation", "").lower()
                if "profit" in motivation or "control" in motivation:
                    return False
            
            elif code.code_id == "UEC-003":  # Universal Access
                if decision_data.get("discriminatory", False):
                    return False
        
        return True
    
    def _check_power_concentration(self, actor: str) -> bool:
        """Check if actor's power is within acceptable limits"""
        if actor not in self.power_distribution:
            return True  # New actor, no concentration yet
        
        distribution = self.power_distribution[actor]
        return distribution.current_power_score < self.max_power_concentration
    
    def _update_power_distribution(self, actor: str, decision_data: Dict[str, Any]):
        """Update power distribution tracking"""
        if actor not in self.power_distribution:
            self.power_distribution[actor] = PowerDistribution(
                entity_id=actor,
                current_power_score=0.0,
                recent_decisions=0,
                resource_control=0.0,
                last_audit=datetime.now(timezone.utc).isoformat(),
                concentration_risk=CorruptionRisk.NONE
            )
        
        distribution = self.power_distribution[actor]
        
        # Update metrics
        distribution.recent_decisions += 1
        
        # Update power score based on impact
        impact = decision_data.get("impact_score", 0.1)
        distribution.current_power_score += impact * 0.1
        distribution.current_power_score = min(1.0, distribution.current_power_score)
        
        # Update resource control
        if decision_data.get("resource_allocation"):
            distribution.resource_control += 0.05
            distribution.resource_control = min(1.0, distribution.resource_control)
        
        # Assess concentration risk
        if distribution.current_power_score >= self.max_power_concentration:
            distribution.concentration_risk = CorruptionRisk.CRITICAL
        elif distribution.current_power_score >= self.max_power_concentration * 0.8:
            distribution.concentration_risk = CorruptionRisk.HIGH
        elif distribution.current_power_score >= self.max_power_concentration * 0.5:
            distribution.concentration_risk = CorruptionRisk.MODERATE
        else:
            distribution.concentration_risk = CorruptionRisk.LOW
    
    def _reduce_power(self, actor: str, reduction_factor: float):
        """Reduce an actor's power"""
        if actor in self.power_distribution:
            distribution = self.power_distribution[actor]
            distribution.current_power_score *= (1 - reduction_factor)
            distribution.resource_control *= (1 - reduction_factor)
    
    def _remove_entity(self, actor: str):
        """Remove entity from system"""
        if actor in self.power_distribution:
            del self.power_distribution[actor]
    
    def _calculate_record_hash(self, record: GovernanceRecord) -> str:
        """Calculate hash for governance record"""
        data = {
            "record_id": record.record_id,
            "timestamp": record.timestamp,
            "action_type": record.action_type.value,
            "actor": record.actor,
            "decision_data": record.decision_data,
            "previous_record_hash": record.previous_record_hash
        }
        
        json_data = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_data.encode()).hexdigest()
    
    def _generate_record_id(self) -> str:
        """Generate unique record ID"""
        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        count = len(self.governance_chain)
        data = f"GOVERNANCE-{timestamp}-{count}"
        hash_part = hashlib.sha256(data.encode()).hexdigest()[:12].upper()
        return f"GR-{hash_part}"
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log event to file"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


# Global instance
_aeterna_governatia_instance = None


def get_aeterna_governatia() -> AeternaGovernati:
    """Get global AETERNA GOVERNATIA instance"""
    global _aeterna_governatia_instance
    if _aeterna_governatia_instance is None:
        _aeterna_governatia_instance = AeternaGovernati()
    return _aeterna_governatia_instance


if __name__ == "__main__":
    # Demo usage
    ag = AeternaGovernati()
    
    print("AETERNA GOVERNATIA - Eternal Guardianship Framework")
    print(f"Universal Ethical Codes: {len(ag.ethical_codes)}\n")
    
    # Record governance action
    record = ag.record_governance_action(
        action_type=GovernanceAction.RESOURCE_ALLOCATION,
        actor="entity-001",
        decision_data={
            "resources": {"medical": 1000, "food": 5000},
            "beneficiaries": "community-region-1",
            "impact_score": 0.8,
            "motivation": "help communities in need"
        },
        signatures=["sig-001", "sig-002"]
    )
    
    print(f"Governance action recorded: {record.record_id}")
    print(f"Ethical compliance: {record.ethical_compliance}")
    print(f"Multi-signature required: {record.multi_signature_required}")
    
    # Verify chain
    integrity = ag.verify_chain_integrity()
    print(f"\nChain integrity: {integrity['verified']}")
    print(f"Chain length: {integrity['chain_length']}")
    
    # Audit power distribution
    audit = ag.audit_power_distribution()
    print(f"\nPower distribution health: {audit['distribution_health']:.2%}")
    print(f"Entities tracked: {audit['entities_tracked']}")
    
    # Generate transparency report
    report = ag.get_transparency_report()
    print(f"\nTransparency Report:")
    print(f"Total actions: {report['total_governance_actions']}")
    print(f"Ethical compliance rate: {report['ethical_compliance_rate']:.2%}")
    print(f"Chain integrity: {report['chain_integrity']}")
