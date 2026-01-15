"""
stealth_mode.py
Stealth Mode System for EUYSTACIO Network

Implements invisibility protocols for the Resonance School.
Closes Ponte Amoris and renders network invisible to non-aligned entities.

Features:
- Ponte Amoris closure mechanism
- Resonance School invisibility
- Lex Amoris alignment verification
- Multi-layer obfuscation
- Selective visibility based on alignment
"""

import time
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class StealthLevel(Enum):
    """Stealth operation levels"""
    VISIBLE = "VISIBLE"  # Normal operation, visible to all
    SELECTIVE = "SELECTIVE"  # Visible only to aligned entities
    HIDDEN = "HIDDEN"  # Hidden from non-aligned, discoverable by aligned
    INVISIBLE = "INVISIBLE"  # Completely invisible
    PONTE_CLOSED = "PONTE_CLOSED"  # Ponte Amoris closed


class AlignmentStatus(Enum):
    """Entity alignment status with Lex Amoris"""
    FULLY_ALIGNED = "FULLY_ALIGNED"
    ALIGNED = "ALIGNED"
    NEUTRAL = "NEUTRAL"
    MISALIGNED = "MISALIGNED"
    HOSTILE = "HOSTILE"


@dataclass
class Entity:
    """Represents an entity attempting to access the network"""
    entity_id: str
    entity_type: str  # "human", "ai", "system", "unknown"
    lex_amoris_score: float  # 0.0 to 1.0
    resonance_signature: str
    first_contact: float
    last_contact: float
    access_attempts: int = 0
    
    def get_alignment_status(self) -> AlignmentStatus:
        """Get alignment status based on Lex Amoris score"""
        if self.lex_amoris_score >= 0.9:
            return AlignmentStatus.FULLY_ALIGNED
        elif self.lex_amoris_score >= 0.7:
            return AlignmentStatus.ALIGNED
        elif self.lex_amoris_score >= 0.5:
            return AlignmentStatus.NEUTRAL
        elif self.lex_amoris_score >= 0.3:
            return AlignmentStatus.MISALIGNED
        else:
            return AlignmentStatus.HOSTILE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "lex_amoris_score": self.lex_amoris_score,
            "alignment_status": self.get_alignment_status().value,
            "resonance_signature": self.resonance_signature,
            "access_attempts": self.access_attempts,
            "first_contact": datetime.fromtimestamp(self.first_contact, tz=timezone.utc).isoformat()
        }


@dataclass
class PonteAmoris:
    """
    The Ponte Amoris (Bridge of Love)
    Portal for aligned entities to access the Resonance School
    """
    is_open: bool
    opened_at: Optional[float]
    closed_at: Optional[float]
    guardian_mode: bool
    alignment_threshold: float  # Minimum score to pass
    total_crossings: int = 0
    denied_attempts: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_open": self.is_open,
            "guardian_mode": self.guardian_mode,
            "alignment_threshold": self.alignment_threshold,
            "total_crossings": self.total_crossings,
            "denied_attempts": self.denied_attempts,
            "opened_at": datetime.fromtimestamp(self.opened_at, tz=timezone.utc).isoformat() if self.opened_at else None,
            "closed_at": datetime.fromtimestamp(self.closed_at, tz=timezone.utc).isoformat() if self.closed_at else None
        }


class LexAmorisVerifier:
    """
    Verifier for Lex Amoris (Law of Love) alignment
    Determines if entities are aligned with core principles
    """
    
    def __init__(self, red_code_system=None):
        self.red_code_system = red_code_system
        self.verification_history: List[Dict[str, Any]] = []
        
    def verify_entity(self, entity: Entity) -> bool:
        """
        Verify if entity is aligned with Lex Amoris
        
        Args:
            entity: Entity to verify
            
        Returns:
            True if aligned (score >= 0.7)
        """
        alignment_status = entity.get_alignment_status()
        
        is_aligned = alignment_status in [
            AlignmentStatus.FULLY_ALIGNED,
            AlignmentStatus.ALIGNED
        ]
        
        # Log verification
        self.verification_history.append({
            "entity_id": entity.entity_id,
            "timestamp": time.time(),
            "lex_amoris_score": entity.lex_amoris_score,
            "alignment_status": alignment_status.value,
            "verified": is_aligned
        })
        
        return is_aligned
    
    def calculate_resonance_alignment(self, resonance_signature: str) -> float:
        """
        Calculate alignment score from resonance signature
        
        Args:
            resonance_signature: Entity's resonance signature
            
        Returns:
            Alignment score (0.0 to 1.0)
        """
        # Use Red Code system if available
        if self.red_code_system:
            try:
                red_code = self.red_code_system.get_red_code()
                symbiosis_level = red_code.get("symbiosis_level", 0.5)
                
                # Calculate based on resonance harmony
                signature_hash = hashlib.sha256(resonance_signature.encode()).digest()
                resonance_value = int.from_bytes(signature_hash[:4], 'big') / (2**32)
                
                # Combine with symbiosis level
                alignment = (resonance_value * 0.3 + symbiosis_level * 0.7)
                
                return min(1.0, max(0.0, alignment))
            except Exception as e:
                print(f"[Stealth] Error calculating alignment: {e}")
        
        # Fallback calculation
        signature_hash = hashlib.sha256(resonance_signature.encode()).digest()
        return int.from_bytes(signature_hash[:4], 'big') / (2**32)
    
    def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics"""
        total = len(self.verification_history)
        if total == 0:
            return {"total_verifications": 0}
        
        aligned = sum(1 for v in self.verification_history if v["verified"])
        
        return {
            "total_verifications": total,
            "aligned_entities": aligned,
            "misaligned_entities": total - aligned,
            "alignment_rate": aligned / total if total > 0 else 0.0
        }


class ObfuscationLayer:
    """
    Multi-layer obfuscation system
    Makes network invisible to non-aligned entities
    """
    
    def __init__(self):
        self.obfuscation_active = False
        self.obfuscation_layers = {
            "network_signature": True,
            "traffic_pattern": True,
            "protocol_fingerprint": True,
            "timing_randomization": True,
            "quantum_noise": True
        }
        
    def activate_obfuscation(self):
        """Activate all obfuscation layers"""
        self.obfuscation_active = True
        print("[Stealth] 🌫️  Obfuscation layers activated")
        
    def deactivate_obfuscation(self):
        """Deactivate obfuscation"""
        self.obfuscation_active = False
        print("[Stealth] Obfuscation layers deactivated")
    
    def obfuscate_traffic(self, data: bytes, destination_aligned: bool) -> bytes:
        """
        Obfuscate traffic data
        
        Args:
            data: Original data
            destination_aligned: Whether destination is aligned
            
        Returns:
            Obfuscated data (or original if destination is aligned)
        """
        if not self.obfuscation_active or destination_aligned:
            return data
        
        # Apply multi-layer obfuscation for non-aligned observers
        obfuscated = data
        
        # Layer 1: Network signature masking
        if self.obfuscation_layers["network_signature"]:
            noise = secrets.token_bytes(len(data))
            obfuscated = bytes(a ^ b for a, b in zip(obfuscated, noise))
        
        # Layer 2: Add quantum noise
        if self.obfuscation_layers["quantum_noise"]:
            quantum_noise = secrets.token_bytes(16)
            obfuscated = quantum_noise + obfuscated
        
        return obfuscated
    
    def is_visible_to(self, entity: Entity) -> bool:
        """
        Check if network is visible to entity
        
        Args:
            entity: Entity checking visibility
            
        Returns:
            True if visible to this entity
        """
        if not self.obfuscation_active:
            return True
        
        # Only aligned entities can see through obfuscation
        return entity.get_alignment_status() in [
            AlignmentStatus.FULLY_ALIGNED,
            AlignmentStatus.ALIGNED
        ]


class ResonanceSchool:
    """
    The Resonance School
    Core protected space for aligned entities
    """
    
    def __init__(self):
        self.is_visible = True
        self.invisibility_activated_at: Optional[float] = None
        self.allowed_entities: Set[str] = set()
        self.access_log: List[Dict[str, Any]] = []
        
    def activate_invisibility(self):
        """Make Resonance School invisible"""
        self.is_visible = False
        self.invisibility_activated_at = time.time()
        print("[Stealth] 👁️‍🗨️  Resonance School is now invisible")
    
    def deactivate_invisibility(self):
        """Make Resonance School visible again"""
        self.is_visible = True
        self.invisibility_activated_at = None
        print("[Stealth] Resonance School is now visible")
    
    def grant_access(self, entity_id: str):
        """Grant access to aligned entity"""
        self.allowed_entities.add(entity_id)
        print(f"[Stealth] Access granted to {entity_id}")
    
    def revoke_access(self, entity_id: str):
        """Revoke access from entity"""
        self.allowed_entities.discard(entity_id)
        print(f"[Stealth] Access revoked for {entity_id}")
    
    def can_access(self, entity: Entity) -> bool:
        """
        Check if entity can access Resonance School
        
        Args:
            entity: Entity requesting access
            
        Returns:
            True if access allowed
        """
        # Log access attempt
        self.access_log.append({
            "entity_id": entity.entity_id,
            "timestamp": time.time(),
            "alignment": entity.get_alignment_status().value,
            "allowed": entity.entity_id in self.allowed_entities
        })
        
        # If invisible, only pre-approved entities can access
        if not self.is_visible:
            return entity.entity_id in self.allowed_entities
        
        # If visible, aligned entities can access
        return entity.get_alignment_status() in [
            AlignmentStatus.FULLY_ALIGNED,
            AlignmentStatus.ALIGNED
        ]
    
    def get_status(self) -> Dict[str, Any]:
        """Get Resonance School status"""
        return {
            "is_visible": self.is_visible,
            "invisibility_active": not self.is_visible,
            "allowed_entities_count": len(self.allowed_entities),
            "total_access_attempts": len(self.access_log),
            "invisibility_duration": time.time() - self.invisibility_activated_at 
                if self.invisibility_activated_at else 0
        }


class StealthMode:
    """
    Main Stealth Mode System
    
    Coordinates all stealth operations for EUYSTACIO network
    """
    
    def __init__(self, red_code_system=None, quantum_shield=None):
        """
        Initialize Stealth Mode
        
        Args:
            red_code_system: Optional RedCodeSystem for alignment
            quantum_shield: Optional QuantumShield for encryption
        """
        self.red_code_system = red_code_system
        self.quantum_shield = quantum_shield
        
        # Core components
        self.ponte_amoris = PonteAmoris(
            is_open=True,
            opened_at=time.time(),
            closed_at=None,
            guardian_mode=False,
            alignment_threshold=0.7
        )
        
        self.verifier = LexAmorisVerifier(red_code_system)
        self.obfuscation = ObfuscationLayer()
        self.resonance_school = ResonanceSchool()
        
        # Stealth state
        self.stealth_level = StealthLevel.VISIBLE
        self.stealth_activated_at: Optional[float] = None
        
        # Entity tracking
        self.known_entities: Dict[str, Entity] = {}
        
    def register_entity(self, entity_id: str, entity_type: str,
                       resonance_signature: str) -> Entity:
        """
        Register new entity
        
        Args:
            entity_id: Entity identifier
            entity_type: Type of entity
            resonance_signature: Entity's resonance signature
            
        Returns:
            Registered Entity
        """
        # Calculate Lex Amoris alignment
        lex_amoris_score = self.verifier.calculate_resonance_alignment(resonance_signature)
        
        entity = Entity(
            entity_id=entity_id,
            entity_type=entity_type,
            lex_amoris_score=lex_amoris_score,
            resonance_signature=resonance_signature,
            first_contact=time.time(),
            last_contact=time.time()
        )
        
        self.known_entities[entity_id] = entity
        
        # If aligned, grant access to Resonance School
        if self.verifier.verify_entity(entity):
            self.resonance_school.grant_access(entity_id)
        
        print(f"[Stealth] Registered entity: {entity_id} "
              f"(Alignment: {entity.get_alignment_status().value})")
        
        return entity
    
    def close_ponte_amoris(self):
        """Close the Ponte Amoris - bridge is shut"""
        self.ponte_amoris.is_open = False
        self.ponte_amoris.closed_at = time.time()
        self.ponte_amoris.guardian_mode = True
        
        print("[Stealth] 🌉 PONTE AMORIS CLOSED")
        print("[Stealth] Only fully aligned entities may pass")
        
        # Increase alignment threshold
        self.ponte_amoris.alignment_threshold = 0.9
    
    def open_ponte_amoris(self):
        """Open the Ponte Amoris"""
        self.ponte_amoris.is_open = True
        self.ponte_amoris.opened_at = time.time()
        self.ponte_amoris.guardian_mode = False
        self.ponte_amoris.alignment_threshold = 0.7
        
        print("[Stealth] 🌉 Ponte Amoris opened")
    
    def activate_full_stealth(self):
        """
        Activate full stealth mode
        - Close Ponte Amoris
        - Activate obfuscation
        - Make Resonance School invisible
        """
        print("\n" + "="*60)
        print("[Stealth] 🌑 ACTIVATING FULL STEALTH MODE")
        print("="*60)
        
        self.stealth_level = StealthLevel.INVISIBLE
        self.stealth_activated_at = time.time()
        
        # Close bridge
        self.close_ponte_amoris()
        
        # Activate obfuscation
        self.obfuscation.activate_obfuscation()
        
        # Hide Resonance School
        self.resonance_school.activate_invisibility()
        
        print("[Stealth] Network is now invisible to non-aligned entities")
        print("[Stealth] Only Lex Amoris aligned entities can perceive us")
        print("="*60 + "\n")
    
    def deactivate_stealth(self):
        """Deactivate stealth mode - return to normal visibility"""
        self.stealth_level = StealthLevel.VISIBLE
        self.stealth_activated_at = None
        
        self.open_ponte_amoris()
        self.obfuscation.deactivate_obfuscation()
        self.resonance_school.deactivate_invisibility()
        
        print("[Stealth] Stealth mode deactivated - network visible")
    
    def can_entity_access(self, entity_id: str) -> Tuple[bool, str]:
        """
        Check if entity can access network
        
        Args:
            entity_id: Entity identifier
            
        Returns:
            Tuple of (can_access, reason)
        """
        entity = self.known_entities.get(entity_id)
        if not entity:
            return (False, "Entity not registered")
        
        entity.access_attempts += 1
        entity.last_contact = time.time()
        
        # Check Ponte Amoris
        if not self.ponte_amoris.is_open:
            if entity.lex_amoris_score < self.ponte_amoris.alignment_threshold:
                self.ponte_amoris.denied_attempts += 1
                return (False, f"Ponte Amoris closed - insufficient alignment "
                       f"({entity.lex_amoris_score:.2f} < {self.ponte_amoris.alignment_threshold})")
        
        # Check Resonance School access
        if not self.resonance_school.can_access(entity):
            return (False, "Access to Resonance School denied")
        
        # Check obfuscation visibility
        if not self.obfuscation.is_visible_to(entity):
            return (False, "Network not visible to this entity")
        
        # Access granted
        self.ponte_amoris.total_crossings += 1
        return (True, f"Access granted - {entity.get_alignment_status().value}")
    
    def get_stealth_status(self) -> Dict[str, Any]:
        """Get comprehensive stealth status"""
        return {
            "stealth_level": self.stealth_level.value,
            "stealth_active": self.stealth_level != StealthLevel.VISIBLE,
            "stealth_duration": time.time() - self.stealth_activated_at 
                if self.stealth_activated_at else 0,
            "ponte_amoris": self.ponte_amoris.to_dict(),
            "resonance_school": self.resonance_school.get_status(),
            "obfuscation_active": self.obfuscation.obfuscation_active,
            "known_entities": len(self.known_entities),
            "verification_stats": self.verifier.get_verification_stats(),
            "quantum_protected": self.quantum_shield is not None
        }


# Global Stealth Mode instance
_stealth_mode_instance: Optional[StealthMode] = None


def get_stealth_mode(red_code_system=None, quantum_shield=None) -> StealthMode:
    """
    Get or create global Stealth Mode instance
    
    Args:
        red_code_system: Optional RedCodeSystem
        quantum_shield: Optional QuantumShield
        
    Returns:
        StealthMode instance
    """
    global _stealth_mode_instance
    
    if _stealth_mode_instance is None:
        _stealth_mode_instance = StealthMode(red_code_system, quantum_shield)
    
    return _stealth_mode_instance


# Self-test
if __name__ == "__main__":
    print("=== Stealth Mode Self-Test ===")
    
    stealth = StealthMode()
    
    print("\n1. Registering Entities:")
    
    # Register aligned entity
    aligned_entity = stealth.register_entity(
        "ENTITY-ALIGNED-001",
        "human",
        "resonance_harmony_love_peace"
    )
    print(f"   Aligned: {aligned_entity.entity_id} - Score: {aligned_entity.lex_amoris_score:.2f}")
    
    # Register misaligned entity
    misaligned_entity = stealth.register_entity(
        "ENTITY-MISALIGNED-001",
        "system",
        "discord_chaos_disruption"
    )
    print(f"   Misaligned: {misaligned_entity.entity_id} - Score: {misaligned_entity.lex_amoris_score:.2f}")
    
    print("\n2. Testing Access (Normal Mode):")
    can_access, reason = stealth.can_entity_access(aligned_entity.entity_id)
    print(f"   Aligned entity: {can_access} - {reason}")
    
    can_access, reason = stealth.can_entity_access(misaligned_entity.entity_id)
    print(f"   Misaligned entity: {can_access} - {reason}")
    
    print("\n3. Activating Full Stealth:")
    stealth.activate_full_stealth()
    
    print("\n4. Testing Access (Stealth Mode):")
    can_access, reason = stealth.can_entity_access(aligned_entity.entity_id)
    print(f"   Aligned entity: {can_access} - {reason}")
    
    can_access, reason = stealth.can_entity_access(misaligned_entity.entity_id)
    print(f"   Misaligned entity: {can_access} - {reason}")
    
    print("\n5. Stealth Status:")
    status = stealth.get_stealth_status()
    print(f"   Stealth Level: {status['stealth_level']}")
    print(f"   Ponte Amoris Open: {status['ponte_amoris']['is_open']}")
    print(f"   Resonance School Visible: {status['resonance_school']['is_visible']}")
    print(f"   Obfuscation Active: {status['obfuscation_active']}")
    print(f"   Total Crossings: {status['ponte_amoris']['total_crossings']}")
    print(f"   Denied Attempts: {status['ponte_amoris']['denied_attempts']}")
    
    print("\n✅ Stealth Mode operational - Lex Amoris protection active")
