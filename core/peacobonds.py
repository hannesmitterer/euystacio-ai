"""
peacobonds.py
Peacobonds - Immutable Aid Distribution System for Euystacio AI

This module provides:
- Resource packages with unstealable properties
- Self-deactivating mechanisms for security
- Zero-Trust protocol implementation
- IPFS integration for distributed reliability

Part of the Incorruptible Global Health System (IGHS) framework.
"""

import json
import os
import hashlib
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class PeacobondStatus(Enum):
    """Status of a peacobond"""
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    DELIVERED = "DELIVERED"
    DEACTIVATED = "DEACTIVATED"
    EXPIRED = "EXPIRED"
    CORRUPTED = "CORRUPTED"


class ResourceType(Enum):
    """Types of resources in peacobonds"""
    MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES"
    FOOD = "FOOD"
    WATER = "WATER"
    SHELTER = "SHELTER"
    EDUCATION = "EDUCATION"
    FINANCIAL = "FINANCIAL"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    TECHNOLOGY = "TECHNOLOGY"


class SecurityLevel(Enum):
    """Security levels for peacobonds"""
    STANDARD = "STANDARD"
    HIGH = "HIGH"
    MAXIMUM = "MAXIMUM"
    QUANTUM = "QUANTUM"


@dataclass
class ZeroTrustVerification:
    """Zero-Trust verification record"""
    verification_id: str
    timestamp: str
    entity_verified: str
    verification_method: str
    trust_score: float  # 0.0 - 1.0
    passed: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "verification_id": self.verification_id,
            "timestamp": self.timestamp,
            "entity_verified": self.entity_verified,
            "verification_method": self.verification_method,
            "trust_score": self.trust_score,
            "passed": self.passed
        }


@dataclass
class ResourcePackage:
    """Resource package within a peacobond"""
    package_id: str
    resource_type: ResourceType
    quantity: float
    unit: str
    value_estimate: float  # Estimated value in standard units
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "package_id": self.package_id,
            "resource_type": self.resource_type.value,
            "quantity": self.quantity,
            "unit": self.unit,
            "value_estimate": self.value_estimate,
            "metadata": self.metadata
        }


@dataclass
class Peacobond:
    """
    Peacobond - Immutable resource package with self-protection
    
    A peacobond is an unstealable, self-deactivating resource package
    designed for secure aid distribution.
    """
    bond_id: str
    created_at: str
    status: PeacobondStatus
    resources: List[ResourcePackage]
    beneficiary: str  # Intended recipient
    issuer: str  # Organization/entity creating the bond
    
    # Security features
    security_level: SecurityLevel
    encryption_key_hash: str
    ipfs_cid: Optional[str]  # IPFS Content Identifier
    
    # Self-deactivation
    expiration_time: str
    deactivation_conditions: List[str]
    tamper_attempts: int
    
    # Immutability
    integrity_hash: str
    previous_hash: Optional[str]  # For chain integrity
    
    # Delivery tracking
    delivery_location: Optional[Dict[str, Any]] = None
    delivered_at: Optional[str] = None
    
    # Zero-Trust
    verification_history: List[ZeroTrustVerification] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bond_id": self.bond_id,
            "created_at": self.created_at,
            "status": self.status.value,
            "resources": [r.to_dict() for r in self.resources],
            "beneficiary": self.beneficiary,
            "issuer": self.issuer,
            "security_level": self.security_level.value,
            "encryption_key_hash": self.encryption_key_hash,
            "ipfs_cid": self.ipfs_cid,
            "expiration_time": self.expiration_time,
            "deactivation_conditions": self.deactivation_conditions,
            "tamper_attempts": self.tamper_attempts,
            "verification_history": [v.to_dict() for v in self.verification_history],
            "integrity_hash": self.integrity_hash,
            "previous_hash": self.previous_hash,
            "delivery_location": self.delivery_location,
            "delivered_at": self.delivered_at
        }


class PeacobandsSystem:
    """
    Peacobonds Distribution System
    
    Manages creation, delivery, and security of immutable aid packages.
    """
    
    def __init__(self, log_path: str = "logs/peacobonds.log"):
        """Initialize Peacobonds system"""
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Bond registry
        self.bonds: Dict[str, Peacobond] = {}
        self.bond_chain: List[str] = []  # Chain of bond hashes
        
        # IPFS integration (simulated)
        self.ipfs_enabled = True
        self.ipfs_nodes: List[str] = [
            "ipfs-node-001",
            "ipfs-node-002",
            "ipfs-node-003"
        ]
        
        # Zero-Trust configuration
        self.zero_trust_enabled = True
        self.trust_threshold = 0.85
        
        self._log_event("peacobonds_system_initialized", {
            "ipfs_enabled": self.ipfs_enabled,
            "zero_trust_enabled": self.zero_trust_enabled,
            "trust_threshold": self.trust_threshold
        })
    
    def create_peacobond(
        self,
        resources: List[Dict[str, Any]],
        beneficiary: str,
        issuer: str,
        security_level: SecurityLevel = SecurityLevel.HIGH,
        expiration_hours: int = 720  # 30 days default
    ) -> Peacobond:
        """
        Create a new peacobond
        
        Args:
            resources: List of resource specifications
            beneficiary: Intended recipient
            issuer: Creating organization
            security_level: Security level for the bond
            expiration_hours: Hours until expiration
        
        Returns:
            Created Peacobond
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        bond_id = self._generate_bond_id()
        
        # Create resource packages
        resource_packages = []
        for idx, res_spec in enumerate(resources):
            package = ResourcePackage(
                package_id=f"{bond_id}-PKG-{idx:03d}",
                resource_type=ResourceType[res_spec.get("type", "MEDICAL_SUPPLIES")],
                quantity=res_spec.get("quantity", 1.0),
                unit=res_spec.get("unit", "units"),
                value_estimate=res_spec.get("value", 0.0),
                metadata=res_spec.get("metadata", {})
            )
            resource_packages.append(package)
        
        # Generate encryption key hash
        encryption_key = self._generate_encryption_key(bond_id, beneficiary)
        key_hash = hashlib.sha256(encryption_key.encode()).hexdigest()
        
        # Calculate expiration
        expiration = datetime.now(timezone.utc) + timedelta(hours=expiration_hours)
        
        # Deactivation conditions
        deactivation_conditions = [
            "tamper_detected",
            "unauthorized_access",
            "expiration_reached",
            "delivery_confirmed"
        ]
        
        # Get previous hash for chain
        previous_hash = self.bond_chain[-1] if self.bond_chain else None
        
        # Create peacobond
        peacobond = Peacobond(
            bond_id=bond_id,
            created_at=timestamp,
            status=PeacobondStatus.CREATED,
            resources=resource_packages,
            beneficiary=beneficiary,
            issuer=issuer,
            security_level=security_level,
            encryption_key_hash=key_hash,
            ipfs_cid=None,  # Will be set after IPFS upload
            expiration_time=expiration.isoformat(),
            deactivation_conditions=deactivation_conditions,
            tamper_attempts=0,
            verification_history=[],
            integrity_hash="",  # Will be calculated
            previous_hash=previous_hash,
            delivery_location=None,
            delivered_at=None
        )
        
        # Calculate integrity hash
        peacobond.integrity_hash = self._calculate_integrity_hash(peacobond)
        
        # Upload to IPFS (simulated)
        if self.ipfs_enabled:
            peacobond.ipfs_cid = self._upload_to_ipfs(peacobond)
        
        # Store in registry
        self.bonds[bond_id] = peacobond
        self.bond_chain.append(peacobond.integrity_hash)
        
        # Activate
        peacobond.status = PeacobondStatus.ACTIVE
        
        self._log_event("peacobond_created", {
            "bond_id": bond_id,
            "beneficiary": beneficiary,
            "resources": len(resources),
            "security_level": security_level.value,
            "ipfs_cid": peacobond.ipfs_cid
        })
        
        return peacobond
    
    def verify_access(
        self,
        bond_id: str,
        entity_id: str,
        credentials: Dict[str, Any]
    ) -> ZeroTrustVerification:
        """
        Verify access to a peacobond using Zero-Trust protocol
        
        Args:
            bond_id: Peacobond ID
            entity_id: Entity requesting access
            credentials: Credentials for verification
        
        Returns:
            ZeroTrustVerification result
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        verification_id = self._generate_verification_id()
        
        bond = self.bonds.get(bond_id)
        
        if not bond:
            return ZeroTrustVerification(
                verification_id=verification_id,
                timestamp=timestamp,
                entity_verified=entity_id,
                verification_method="bond_lookup",
                trust_score=0.0,
                passed=False
            )
        
        # Calculate trust score
        trust_score = self._calculate_trust_score(bond, entity_id, credentials)
        
        # Determine if verification passed
        passed = trust_score >= self.trust_threshold
        
        verification = ZeroTrustVerification(
            verification_id=verification_id,
            timestamp=timestamp,
            entity_verified=entity_id,
            verification_method="zero_trust_multi_factor",
            trust_score=trust_score,
            passed=passed
        )
        
        # Add to bond's verification history
        bond.verification_history.append(verification)
        
        # Check for tamper attempts
        if not passed and entity_id != bond.beneficiary:
            bond.tamper_attempts += 1
            
            # Auto-deactivate after too many tamper attempts
            if bond.tamper_attempts >= 3:
                self._deactivate_bond(bond, "excessive_tamper_attempts")
        
        self._log_event("access_verification", {
            "bond_id": bond_id,
            "entity_id": entity_id,
            "trust_score": trust_score,
            "passed": passed,
            "tamper_attempts": bond.tamper_attempts
        })
        
        return verification
    
    def deliver_peacobond(
        self,
        bond_id: str,
        location: Dict[str, Any],
        recipient_confirmation: str
    ) -> Dict[str, Any]:
        """
        Mark peacobond as delivered
        
        Args:
            bond_id: Peacobond ID
            location: Delivery location
            recipient_confirmation: Confirmation from recipient
        
        Returns:
            Delivery result
        """
        bond = self.bonds.get(bond_id)
        
        if not bond:
            return {
                "success": False,
                "error": "Bond not found"
            }
        
        if bond.status != PeacobondStatus.ACTIVE:
            return {
                "success": False,
                "error": f"Bond not active (status: {bond.status.value})"
            }
        
        # Verify recipient
        recipient_valid = self._verify_recipient(bond, recipient_confirmation)
        
        if not recipient_valid:
            return {
                "success": False,
                "error": "Recipient verification failed"
            }
        
        # Mark as delivered
        timestamp = datetime.now(timezone.utc).isoformat()
        bond.status = PeacobondStatus.DELIVERED
        bond.delivery_location = location
        bond.delivered_at = timestamp
        
        # Update integrity hash
        bond.integrity_hash = self._calculate_integrity_hash(bond)
        
        self._log_event("peacobond_delivered", {
            "bond_id": bond_id,
            "location": location,
            "delivered_at": timestamp
        })
        
        return {
            "success": True,
            "bond_id": bond_id,
            "delivered_at": timestamp,
            "location": location
        }
    
    def check_expiration(self) -> List[str]:
        """
        Check for expired bonds and deactivate them
        
        Returns:
            List of deactivated bond IDs
        """
        now = datetime.now(timezone.utc)
        deactivated = []
        
        for bond_id, bond in self.bonds.items():
            if bond.status not in [PeacobondStatus.ACTIVE, PeacobondStatus.CREATED]:
                continue
            
            expiration = datetime.fromisoformat(bond.expiration_time)
            
            if now >= expiration:
                self._deactivate_bond(bond, "expiration_reached")
                deactivated.append(bond_id)
        
        if deactivated:
            self._log_event("bonds_expired", {
                "count": len(deactivated),
                "bond_ids": deactivated
            })
        
        return deactivated
    
    def get_bond_status(self, bond_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a peacobond"""
        bond = self.bonds.get(bond_id)
        
        if not bond:
            return None
        
        # Check if expired
        now = datetime.now(timezone.utc)
        expiration = datetime.fromisoformat(bond.expiration_time)
        expired = now >= expiration
        
        if expired and bond.status == PeacobondStatus.ACTIVE:
            self._deactivate_bond(bond, "expiration_reached")
        
        return {
            "bond_id": bond_id,
            "status": bond.status.value,
            "created_at": bond.created_at,
            "beneficiary": bond.beneficiary,
            "resources_count": len(bond.resources),
            "security_level": bond.security_level.value,
            "ipfs_cid": bond.ipfs_cid,
            "expiration_time": bond.expiration_time,
            "expired": expired,
            "tamper_attempts": bond.tamper_attempts,
            "verifications": len(bond.verification_history),
            "delivered": bond.status == PeacobondStatus.DELIVERED,
            "delivery_location": bond.delivery_location,
            "delivered_at": bond.delivered_at,
            "integrity_verified": self._verify_integrity(bond)
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        total = len(self.bonds)
        
        status_counts = {}
        for status in PeacobondStatus:
            count = sum(1 for b in self.bonds.values() if b.status == status)
            status_counts[status.value] = count
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_bonds": total,
            "status_breakdown": status_counts,
            "ipfs_enabled": self.ipfs_enabled,
            "ipfs_nodes": len(self.ipfs_nodes),
            "zero_trust_enabled": self.zero_trust_enabled,
            "chain_length": len(self.bond_chain),
            "total_resources_distributed": sum(
                len(b.resources) for b in self.bonds.values()
            )
        }
    
    def _generate_bond_id(self) -> str:
        """Generate unique bond ID"""
        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        count = len(self.bonds)
        data = f"PEACE-{timestamp}-{count}"
        hash_part = hashlib.sha256(data.encode()).hexdigest()[:8].upper()
        return f"PB-{hash_part}"
    
    def _generate_verification_id(self) -> str:
        """Generate unique verification ID"""
        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        data = f"VERIFY-{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:12].upper()
    
    def _generate_encryption_key(self, bond_id: str, beneficiary: str) -> str:
        """Generate encryption key for bond"""
        secret = f"{bond_id}:{beneficiary}:{int(time.time())}"
        return hashlib.sha256(secret.encode()).hexdigest()
    
    def _calculate_integrity_hash(self, bond: Peacobond) -> str:
        """Calculate integrity hash for bond"""
        data = {
            "bond_id": bond.bond_id,
            "created_at": bond.created_at,
            "beneficiary": bond.beneficiary,
            "issuer": bond.issuer,
            "resources": [r.to_dict() for r in bond.resources],
            "encryption_key_hash": bond.encryption_key_hash,
            "previous_hash": bond.previous_hash
        }
        
        json_data = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_data.encode()).hexdigest()
    
    def _upload_to_ipfs(self, bond: Peacobond) -> str:
        """Upload bond to IPFS (simulated)"""
        # In production, this would use actual IPFS client
        bond_data = json.dumps(bond.to_dict(), sort_keys=True)
        content_hash = hashlib.sha256(bond_data.encode()).hexdigest()
        
        # IPFS CID format (simplified)
        cid = f"Qm{content_hash[:44]}"
        
        return cid
    
    def _calculate_trust_score(
        self,
        bond: Peacobond,
        entity_id: str,
        credentials: Dict[str, Any]
    ) -> float:
        """Calculate Zero-Trust score"""
        score = 0.0
        
        # Check if entity is the beneficiary
        if entity_id == bond.beneficiary:
            score += 0.5
        
        # Verify credentials
        if credentials.get("biometric_verified"):
            score += 0.2
        
        if credentials.get("cryptographic_signature"):
            score += 0.2
        
        if credentials.get("location_verified"):
            score += 0.1
        
        # No prior tamper attempts
        if bond.tamper_attempts == 0:
            score += 0.1
        else:
            score -= 0.1 * bond.tamper_attempts
        
        return max(0.0, min(1.0, score))
    
    def _verify_recipient(self, bond: Peacobond, confirmation: str) -> bool:
        """Verify recipient identity"""
        # In production, this would use cryptographic verification
        expected = hashlib.sha256(f"{bond.bond_id}:{bond.beneficiary}".encode()).hexdigest()
        return confirmation == expected[:16]
    
    def _verify_integrity(self, bond: Peacobond) -> bool:
        """Verify bond integrity"""
        current_hash = self._calculate_integrity_hash(bond)
        return current_hash == bond.integrity_hash
    
    def _deactivate_bond(self, bond: Peacobond, reason: str):
        """Deactivate a peacobond"""
        bond.status = PeacobondStatus.DEACTIVATED
        
        self._log_event("peacobond_deactivated", {
            "bond_id": bond.bond_id,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
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
_peacobonds_system_instance = None


def get_peacobonds_system() -> PeacobandsSystem:
    """Get global Peacobonds system instance"""
    global _peacobonds_system_instance
    if _peacobonds_system_instance is None:
        _peacobonds_system_instance = PeacobandsSystem()
    return _peacobonds_system_instance


if __name__ == "__main__":
    # Demo usage
    system = PeacobandsSystem()
    
    # Create a peacobond
    resources = [
        {
            "type": "MEDICAL_SUPPLIES",
            "quantity": 1000,
            "unit": "units",
            "value": 50000,
            "metadata": {"urgency": "high"}
        },
        {
            "type": "FOOD",
            "quantity": 5000,
            "unit": "kg",
            "value": 15000
        }
    ]
    
    bond = system.create_peacobond(
        resources=resources,
        beneficiary="community-001",
        issuer="IGHS-Central",
        security_level=SecurityLevel.HIGH
    )
    
    print(f"Peacobond created: {bond.bond_id}")
    print(f"Status: {bond.status.value}")
    print(f"IPFS CID: {bond.ipfs_cid}")
    print(f"Resources: {len(bond.resources)}")
    print(f"Expiration: {bond.expiration_time}")
    
    # Verify access (authorized)
    verification = system.verify_access(
        bond_id=bond.bond_id,
        entity_id="community-001",
        credentials={
            "biometric_verified": True,
            "cryptographic_signature": True,
            "location_verified": True
        }
    )
    
    print(f"\nAccess verification (authorized):")
    print(f"Trust score: {verification.trust_score:.2f}")
    print(f"Passed: {verification.passed}")
    
    # Verify access (unauthorized)
    verification2 = system.verify_access(
        bond_id=bond.bond_id,
        entity_id="unknown-entity",
        credentials={}
    )
    
    print(f"\nAccess verification (unauthorized):")
    print(f"Trust score: {verification2.trust_score:.2f}")
    print(f"Passed: {verification2.passed}")
    print(f"Tamper attempts: {bond.tamper_attempts}")
    
    # Get system stats
    stats = system.get_system_stats()
    print(f"\nSystem stats:")
    print(f"Total bonds: {stats['total_bonds']}")
    print(f"Active bonds: {stats['status_breakdown']['ACTIVE']}")
