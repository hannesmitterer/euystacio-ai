"""
peace_bonds.py
Peace Bonds Management Module for Protocollo Meta Salvage

This module provides:
- Definition and enforcement of operational constraints (Peace Bonds)
- Dynamic restriction management for external providers
- Policy-based constraint enforcement
- Integration with decision engines (OPA, Gatekeeper)

Peace Bonds are preventive constraints imposed on CaaS providers during
ethical risk periods to preserve systemic integrity.
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class BondStatus(Enum):
    """Status of a Peace Bond"""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    LIFTED = "LIFTED"
    VIOLATED = "VIOLATED"


class ConstraintType(Enum):
    """Types of operational constraints"""
    THROUGHPUT_LIMIT = "THROUGHPUT_LIMIT"
    LATENCY_CEILING = "LATENCY_CEILING"
    COST_CEILING = "COST_CEILING"
    DATA_VOLUME_LIMIT = "DATA_VOLUME_LIMIT"
    OPERATIONAL_SCOPE = "OPERATIONAL_SCOPE"
    METADATA_TRANSPARENCY = "METADATA_TRANSPARENCY"
    AUDIT_REQUIREMENT = "AUDIT_REQUIREMENT"


@dataclass
class Constraint:
    """Represents an operational constraint"""
    constraint_type: ConstraintType
    parameter: str
    limit_value: Any
    unit: str
    description: str
    enforcement_method: str  # "hard", "soft", "audit"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "constraint_type": self.constraint_type.value,
            "parameter": self.parameter,
            "limit_value": self.limit_value,
            "unit": self.unit,
            "description": self.description,
            "enforcement_method": self.enforcement_method
        }


@dataclass
class PeaceBond:
    """
    Represents a Peace Bond imposed on a provider
    
    A Peace Bond is a set of operational constraints designed to mitigate
    ethical risks while preserving the provider's utility to the system.
    """
    bond_id: str
    provider_id: str
    status: BondStatus
    constraints: List[Constraint]
    reason: str
    imposed_at: str
    expires_at: Optional[str]
    imposed_by: str  # System component that imposed the bond
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bond_id": self.bond_id,
            "provider_id": self.provider_id,
            "status": self.status.value,
            "constraints": [c.to_dict() for c in self.constraints],
            "reason": self.reason,
            "imposed_at": self.imposed_at,
            "expires_at": self.expires_at,
            "imposed_by": self.imposed_by,
            "metadata": self.metadata
        }


@dataclass
class ViolationEvent:
    """Represents a Peace Bond violation"""
    violation_id: str
    bond_id: str
    provider_id: str
    timestamp: str
    constraint_violated: str
    actual_value: Any
    limit_value: Any
    severity: str  # "minor", "major", "critical"
    action_taken: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "bond_id": self.bond_id,
            "provider_id": self.provider_id,
            "timestamp": self.timestamp,
            "constraint_violated": self.constraint_violated,
            "actual_value": self.actual_value,
            "limit_value": self.limit_value,
            "severity": self.severity,
            "action_taken": self.action_taken
        }


class PeaceBondsManager:
    """
    Peace Bonds Management System
    
    Manages the lifecycle of Peace Bonds, from imposition through monitoring
    to lifting or escalation.
    """
    
    def __init__(self, log_dir: str = "logs/peace_bonds"):
        """
        Initialize the Peace Bonds Manager
        
        Args:
            log_dir: Directory for storing bond records and logs
        """
        self.log_dir = log_dir
        self.active_bonds: Dict[str, PeaceBond] = {}
        self.bond_history: List[PeaceBond] = []
        self.violations: List[ViolationEvent] = []
    
    def impose_bond(
        self,
        provider_id: str,
        constraints: List[Constraint],
        reason: str,
        imposed_by: str = "RiskMonitor",
        duration_hours: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PeaceBond:
        """
        Impose a Peace Bond on a provider
        
        Args:
            provider_id: Provider identifier
            constraints: List of constraints to impose
            reason: Reason for imposing the bond
            imposed_by: Component imposing the bond
            duration_hours: Optional duration in hours (None = indefinite)
            metadata: Additional metadata
            
        Returns:
            PeaceBond object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        bond_id = hashlib.sha256(
            f"{timestamp}:{provider_id}".encode()
        ).hexdigest()[:16]
        
        expires_at = None
        if duration_hours:
            expires_at = (
                datetime.now(timezone.utc) + timedelta(hours=duration_hours)
            ).isoformat()
        
        bond = PeaceBond(
            bond_id=bond_id,
            provider_id=provider_id,
            status=BondStatus.ACTIVE,
            constraints=constraints,
            reason=reason,
            imposed_at=timestamp,
            expires_at=expires_at,
            imposed_by=imposed_by,
            metadata=metadata or {}
        )
        
        self.active_bonds[bond_id] = bond
        self.bond_history.append(bond)
        
        return bond
    
    def create_throughput_constraint(
        self,
        max_throughput_ops_sec: float,
        description: Optional[str] = None
    ) -> Constraint:
        """
        Create a throughput limitation constraint
        
        Args:
            max_throughput_ops_sec: Maximum operations per second
            description: Optional custom description
            
        Returns:
            Constraint object
        """
        return Constraint(
            constraint_type=ConstraintType.THROUGHPUT_LIMIT,
            parameter="throughput",
            limit_value=max_throughput_ops_sec,
            unit="ops/sec",
            description=description or f"Maximum throughput limited to {max_throughput_ops_sec} ops/sec",
            enforcement_method="hard"
        )
    
    def create_latency_constraint(
        self,
        max_latency_ms: float,
        description: Optional[str] = None
    ) -> Constraint:
        """
        Create a latency ceiling constraint
        
        Args:
            max_latency_ms: Maximum latency in milliseconds
            description: Optional custom description
            
        Returns:
            Constraint object
        """
        return Constraint(
            constraint_type=ConstraintType.LATENCY_CEILING,
            parameter="latency",
            limit_value=max_latency_ms,
            unit="ms",
            description=description or f"Latency must not exceed {max_latency_ms}ms",
            enforcement_method="hard"
        )
    
    def create_metadata_transparency_constraint(
        self,
        required_fields: List[str],
        description: Optional[str] = None
    ) -> Constraint:
        """
        Create a metadata transparency constraint
        
        Args:
            required_fields: List of metadata fields that must be shared
            description: Optional custom description
            
        Returns:
            Constraint object
        """
        return Constraint(
            constraint_type=ConstraintType.METADATA_TRANSPARENCY,
            parameter="metadata_fields",
            limit_value=required_fields,
            unit="fields",
            description=description or f"Must share metadata fields: {', '.join(required_fields)}",
            enforcement_method="audit"
        )
    
    def create_audit_requirement_constraint(
        self,
        audit_frequency_hours: int,
        description: Optional[str] = None
    ) -> Constraint:
        """
        Create an audit requirement constraint
        
        Args:
            audit_frequency_hours: Frequency of required audits in hours
            description: Optional custom description
            
        Returns:
            Constraint object
        """
        return Constraint(
            constraint_type=ConstraintType.AUDIT_REQUIREMENT,
            parameter="audit_frequency",
            limit_value=audit_frequency_hours,
            unit="hours",
            description=description or f"Must submit to audit every {audit_frequency_hours} hours",
            enforcement_method="audit"
        )
    
    def check_constraint_compliance(
        self,
        bond_id: str,
        actual_values: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Check if a provider is compliant with bond constraints
        
        Args:
            bond_id: Bond identifier
            actual_values: Dictionary of actual measured values
            
        Returns:
            Tuple of (is_compliant, list_of_violations)
        """
        if bond_id not in self.active_bonds:
            return True, []
        
        bond = self.active_bonds[bond_id]
        violations = []
        
        for constraint in bond.constraints:
            parameter = constraint.parameter
            
            if parameter not in actual_values:
                continue
            
            actual_value = actual_values[parameter]
            limit_value = constraint.limit_value
            
            # Check based on constraint type
            if constraint.constraint_type == ConstraintType.THROUGHPUT_LIMIT:
                if actual_value > limit_value:
                    violations.append(
                        f"Throughput exceeded: {actual_value} > {limit_value} {constraint.unit}"
                    )
            
            elif constraint.constraint_type == ConstraintType.LATENCY_CEILING:
                if actual_value > limit_value:
                    violations.append(
                        f"Latency exceeded: {actual_value} > {limit_value} {constraint.unit}"
                    )
            
            elif constraint.constraint_type == ConstraintType.COST_CEILING:
                if actual_value > limit_value:
                    violations.append(
                        f"Cost exceeded: {actual_value} > {limit_value} {constraint.unit}"
                    )
        
        return len(violations) == 0, violations
    
    def record_violation(
        self,
        bond_id: str,
        constraint_violated: str,
        actual_value: Any,
        limit_value: Any,
        severity: str = "major"
    ) -> ViolationEvent:
        """
        Record a Peace Bond violation
        
        Args:
            bond_id: Bond identifier
            constraint_violated: Description of violated constraint
            actual_value: Actual measured value
            limit_value: Limit that was exceeded
            severity: Violation severity
            
        Returns:
            ViolationEvent object
        """
        if bond_id not in self.active_bonds:
            raise ValueError(f"Bond {bond_id} not found")
        
        bond = self.active_bonds[bond_id]
        timestamp = datetime.now(timezone.utc).isoformat()
        violation_id = hashlib.sha256(
            f"{timestamp}:{bond_id}:{constraint_violated}".encode()
        ).hexdigest()[:16]
        
        # Determine action based on severity
        action_taken = "warning_issued"
        if severity == "critical":
            bond.status = BondStatus.VIOLATED
            action_taken = "bond_suspended"
        
        violation = ViolationEvent(
            violation_id=violation_id,
            bond_id=bond_id,
            provider_id=bond.provider_id,
            timestamp=timestamp,
            constraint_violated=constraint_violated,
            actual_value=actual_value,
            limit_value=limit_value,
            severity=severity,
            action_taken=action_taken
        )
        
        self.violations.append(violation)
        
        return violation
    
    def lift_bond(self, bond_id: str, reason: str) -> bool:
        """
        Lift (remove) a Peace Bond
        
        Args:
            bond_id: Bond identifier
            reason: Reason for lifting the bond
            
        Returns:
            True if lifted successfully
        """
        if bond_id not in self.active_bonds:
            return False
        
        bond = self.active_bonds[bond_id]
        bond.status = BondStatus.LIFTED
        bond.metadata["lifted_at"] = datetime.now(timezone.utc).isoformat()
        bond.metadata["lift_reason"] = reason
        
        del self.active_bonds[bond_id]
        
        return True
    
    def suspend_bond(self, bond_id: str, reason: str) -> bool:
        """
        Temporarily suspend a Peace Bond
        
        Args:
            bond_id: Bond identifier
            reason: Reason for suspension
            
        Returns:
            True if suspended successfully
        """
        if bond_id not in self.active_bonds:
            return False
        
        bond = self.active_bonds[bond_id]
        bond.status = BondStatus.SUSPENDED
        bond.metadata["suspended_at"] = datetime.now(timezone.utc).isoformat()
        bond.metadata["suspension_reason"] = reason
        
        return True
    
    def reactivate_bond(self, bond_id: str) -> bool:
        """
        Reactivate a suspended Peace Bond
        
        Args:
            bond_id: Bond identifier
            
        Returns:
            True if reactivated successfully
        """
        if bond_id not in self.active_bonds:
            return False
        
        bond = self.active_bonds[bond_id]
        if bond.status != BondStatus.SUSPENDED:
            return False
        
        bond.status = BondStatus.ACTIVE
        bond.metadata["reactivated_at"] = datetime.now(timezone.utc).isoformat()
        
        return True
    
    def get_active_bonds_for_provider(self, provider_id: str) -> List[PeaceBond]:
        """
        Get all active bonds for a provider
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            List of PeaceBond objects
        """
        return [
            bond for bond in self.active_bonds.values()
            if bond.provider_id == provider_id and bond.status == BondStatus.ACTIVE
        ]
    
    def get_bond_summary(self, bond_id: str) -> Dict[str, Any]:
        """
        Get comprehensive summary of a Peace Bond
        
        Args:
            bond_id: Bond identifier
            
        Returns:
            Summary dictionary
        """
        if bond_id not in self.active_bonds:
            # Check history
            for bond in self.bond_history:
                if bond.bond_id == bond_id:
                    return self._bond_summary_dict(bond)
            return {"error": "Bond not found"}
        
        bond = self.active_bonds[bond_id]
        return self._bond_summary_dict(bond)
    
    def _bond_summary_dict(self, bond: PeaceBond) -> Dict[str, Any]:
        """Create summary dictionary for a bond"""
        bond_violations = [
            v for v in self.violations if v.bond_id == bond.bond_id
        ]
        
        return {
            **bond.to_dict(),
            "violations": [v.to_dict() for v in bond_violations],
            "violation_count": len(bond_violations),
            "is_expired": self._is_bond_expired(bond)
        }
    
    def _is_bond_expired(self, bond: PeaceBond) -> bool:
        """Check if a bond has expired"""
        if not bond.expires_at:
            return False
        
        expires = datetime.fromisoformat(bond.expires_at.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) > expires
    
    def cleanup_expired_bonds(self) -> int:
        """
        Remove expired bonds from active bonds
        
        Returns:
            Number of bonds cleaned up
        """
        expired_bonds = [
            bond_id for bond_id, bond in self.active_bonds.items()
            if self._is_bond_expired(bond)
        ]
        
        for bond_id in expired_bonds:
            self.lift_bond(bond_id, "Bond expired")
        
        return len(expired_bonds)
    
    def get_all_active_bonds(self) -> List[Dict[str, Any]]:
        """
        Get all active Peace Bonds
        
        Returns:
            List of bond summaries
        """
        return [
            self.get_bond_summary(bond_id)
            for bond_id in self.active_bonds.keys()
        ]


# Singleton instance
_peace_bonds_manager_instance: Optional[PeaceBondsManager] = None


def get_peace_bonds_manager(log_dir: str = "logs/peace_bonds") -> PeaceBondsManager:
    """
    Get or create the singleton PeaceBondsManager instance
    
    Args:
        log_dir: Directory for bond logs
        
    Returns:
        PeaceBondsManager instance
    """
    global _peace_bonds_manager_instance
    if _peace_bonds_manager_instance is None:
        _peace_bonds_manager_instance = PeaceBondsManager(log_dir=log_dir)
    return _peace_bonds_manager_instance
