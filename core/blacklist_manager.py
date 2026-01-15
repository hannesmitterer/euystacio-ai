"""
blacklist_manager.py
Permanent Blacklist Management System for EUYSTACIO Framework

Implements:
- Permanent blacklist for suspicious nodes and entities
- Integration with red_code system for persistence
- Threat detection and blocking mechanisms
- Audit logging for security events
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set

# Import fractal systems
try:
    from fractal_logger import get_fractal_logger
    from core.red_code import red_code_system
except ImportError:
    # Fallback for basic functionality
    get_fractal_logger = lambda: None
    red_code_system = None


class ThreatLevel:
    """Threat level classifications for blacklisted entities"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BlockReason:
    """Standard reasons for blocking entities"""
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    ATTACK_ATTEMPT = "attack_attempt"
    DATA_THEFT = "data_theft"
    POLICY_VIOLATION = "policy_violation"
    SECURITY_THREAT = "security_threat"
    ECOSYSTEM_TESTING = "ecosystem_testing"


class BlacklistManager:
    """
    Manages permanent blacklist for EUYSTACIO framework.
    Blocks communication from suspicious nodes and entities.
    """
    
    def __init__(self):
        self.red_code = red_code_system
        self.logger = get_fractal_logger()
        self.blacklist_data = {
            "entities": {},
            "ip_addresses": {},
            "api_keys": {},
            "metadata": {
                "created": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_blocked": 0,
                "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
            }
        }
        self._load_blacklist()
    
    def _load_blacklist(self):
        """Load blacklist from red_code system"""
        if self.red_code:
            red_code_data = self.red_code.get_red_code()
            if "security_blacklist" in red_code_data:
                self.blacklist_data = red_code_data["security_blacklist"]
            else:
                # Initialize blacklist in red_code
                self._save_blacklist()
    
    def _save_blacklist(self):
        """Save blacklist to red_code system"""
        self.blacklist_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        if self.red_code:
            red_code_data = self.red_code.get_red_code()
            red_code_data["security_blacklist"] = self.blacklist_data
            self.red_code._save_red_code()
    
    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        reason: str,
        threat_level: str = ThreatLevel.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add an entity to the blacklist
        
        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of entity (node, user, service, etc.)
            reason: Reason for blacklisting
            threat_level: Threat level classification
            metadata: Additional metadata about the threat
        
        Returns:
            Dictionary with operation result
        """
        if entity_id in self.blacklist_data["entities"]:
            return {
                "success": False,
                "message": f"Entity {entity_id} is already blacklisted",
                "entity_id": entity_id
            }
        
        entry = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "reason": reason,
            "threat_level": threat_level,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "block_count": 0,
            "last_attempt": None
        }
        
        self.blacklist_data["entities"][entity_id] = entry
        self.blacklist_data["metadata"]["total_blocked"] = len(self.blacklist_data["entities"])
        self._save_blacklist()
        
        # Log the event
        if self.logger:
            self.logger.log_event("entity_blacklisted", {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "reason": reason,
                "threat_level": threat_level
            })
        
        return {
            "success": True,
            "message": f"Entity {entity_id} added to blacklist",
            "entity_id": entity_id,
            "threat_level": threat_level
        }
    
    def add_ip_address(
        self,
        ip_address: str,
        reason: str,
        threat_level: str = ThreatLevel.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add an IP address to the blacklist
        
        Args:
            ip_address: IP address to block
            reason: Reason for blacklisting
            threat_level: Threat level classification
            metadata: Additional metadata
        
        Returns:
            Dictionary with operation result
        """
        if ip_address in self.blacklist_data["ip_addresses"]:
            return {
                "success": False,
                "message": f"IP address {ip_address} is already blacklisted",
                "ip_address": ip_address
            }
        
        entry = {
            "ip_address": ip_address,
            "reason": reason,
            "threat_level": threat_level,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "block_count": 0,
            "last_attempt": None
        }
        
        self.blacklist_data["ip_addresses"][ip_address] = entry
        self._save_blacklist()
        
        # Log the event
        if self.logger:
            self.logger.log_event("ip_blacklisted", {
                "ip_address": ip_address,
                "reason": reason,
                "threat_level": threat_level
            })
        
        return {
            "success": True,
            "message": f"IP address {ip_address} added to blacklist",
            "ip_address": ip_address,
            "threat_level": threat_level
        }
    
    def add_api_key(
        self,
        api_key_hash: str,
        reason: str,
        threat_level: str = ThreatLevel.HIGH,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add an API key hash to the blacklist
        
        Args:
            api_key_hash: SHA-256 hash of the API key
            reason: Reason for blacklisting
            threat_level: Threat level classification
            metadata: Additional metadata
        
        Returns:
            Dictionary with operation result
        """
        if api_key_hash in self.blacklist_data["api_keys"]:
            return {
                "success": False,
                "message": "API key is already blacklisted",
                "api_key_hash": api_key_hash[:16] + "..."
            }
        
        entry = {
            "api_key_hash": api_key_hash,
            "reason": reason,
            "threat_level": threat_level,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "block_count": 0,
            "last_attempt": None
        }
        
        self.blacklist_data["api_keys"][api_key_hash] = entry
        self._save_blacklist()
        
        # Log the event
        if self.logger:
            self.logger.log_event("api_key_blacklisted", {
                "api_key_hash": api_key_hash[:16] + "...",
                "reason": reason,
                "threat_level": threat_level
            })
        
        return {
            "success": True,
            "message": "API key added to blacklist",
            "api_key_hash": api_key_hash[:16] + "...",
            "threat_level": threat_level
        }
    
    def is_entity_blocked(self, entity_id: str) -> bool:
        """
        Check if an entity is blacklisted
        
        Args:
            entity_id: Entity identifier to check
        
        Returns:
            True if blocked, False otherwise
        """
        is_blocked = entity_id in self.blacklist_data["entities"]
        
        if is_blocked:
            # Update block count and last attempt
            self.blacklist_data["entities"][entity_id]["block_count"] += 1
            self.blacklist_data["entities"][entity_id]["last_attempt"] = datetime.now(timezone.utc).isoformat()
            self._save_blacklist()
            
            # Log the blocked attempt
            if self.logger:
                self.logger.log_event("blocked_entity_attempt", {
                    "entity_id": entity_id,
                    "block_count": self.blacklist_data["entities"][entity_id]["block_count"]
                })
        
        return is_blocked
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """
        Check if an IP address is blacklisted
        
        Args:
            ip_address: IP address to check
        
        Returns:
            True if blocked, False otherwise
        """
        is_blocked = ip_address in self.blacklist_data["ip_addresses"]
        
        if is_blocked:
            # Update block count and last attempt
            self.blacklist_data["ip_addresses"][ip_address]["block_count"] += 1
            self.blacklist_data["ip_addresses"][ip_address]["last_attempt"] = datetime.now(timezone.utc).isoformat()
            self._save_blacklist()
            
            # Log the blocked attempt
            if self.logger:
                self.logger.log_event("blocked_ip_attempt", {
                    "ip_address": ip_address,
                    "block_count": self.blacklist_data["ip_addresses"][ip_address]["block_count"]
                })
        
        return is_blocked
    
    def is_api_key_blocked(self, api_key: str) -> bool:
        """
        Check if an API key is blacklisted
        
        Args:
            api_key: API key to check (will be hashed)
        
        Returns:
            True if blocked, False otherwise
        """
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        is_blocked = api_key_hash in self.blacklist_data["api_keys"]
        
        if is_blocked:
            # Update block count and last attempt
            self.blacklist_data["api_keys"][api_key_hash]["block_count"] += 1
            self.blacklist_data["api_keys"][api_key_hash]["last_attempt"] = datetime.now(timezone.utc).isoformat()
            self._save_blacklist()
            
            # Log the blocked attempt
            if self.logger:
                self.logger.log_event("blocked_api_key_attempt", {
                    "api_key_hash": api_key_hash[:16] + "...",
                    "block_count": self.blacklist_data["api_keys"][api_key_hash]["block_count"]
                })
        
        return is_blocked
    
    def remove_entity(self, entity_id: str) -> Dict[str, Any]:
        """
        Remove an entity from the blacklist
        
        Args:
            entity_id: Entity identifier to remove
        
        Returns:
            Dictionary with operation result
        """
        if entity_id not in self.blacklist_data["entities"]:
            return {
                "success": False,
                "message": f"Entity {entity_id} is not in the blacklist",
                "entity_id": entity_id
            }
        
        del self.blacklist_data["entities"][entity_id]
        self.blacklist_data["metadata"]["total_blocked"] = len(self.blacklist_data["entities"])
        self._save_blacklist()
        
        # Log the event
        if self.logger:
            self.logger.log_event("entity_removed_from_blacklist", {
                "entity_id": entity_id
            })
        
        return {
            "success": True,
            "message": f"Entity {entity_id} removed from blacklist",
            "entity_id": entity_id
        }
    
    def remove_ip_address(self, ip_address: str) -> Dict[str, Any]:
        """
        Remove an IP address from the blacklist
        
        Args:
            ip_address: IP address to remove
        
        Returns:
            Dictionary with operation result
        """
        if ip_address not in self.blacklist_data["ip_addresses"]:
            return {
                "success": False,
                "message": f"IP address {ip_address} is not in the blacklist",
                "ip_address": ip_address
            }
        
        del self.blacklist_data["ip_addresses"][ip_address]
        self._save_blacklist()
        
        # Log the event
        if self.logger:
            self.logger.log_event("ip_removed_from_blacklist", {
                "ip_address": ip_address
            })
        
        return {
            "success": True,
            "message": f"IP address {ip_address} removed from blacklist",
            "ip_address": ip_address
        }
    
    def get_blacklist_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the blacklist
        
        Returns:
            Dictionary with blacklist statistics
        """
        total_blocks = sum(
            entity["block_count"] for entity in self.blacklist_data["entities"].values()
        ) + sum(
            ip["block_count"] for ip in self.blacklist_data["ip_addresses"].values()
        ) + sum(
            key["block_count"] for key in self.blacklist_data["api_keys"].values()
        )
        
        threat_distribution = {
            ThreatLevel.LOW: 0,
            ThreatLevel.MEDIUM: 0,
            ThreatLevel.HIGH: 0,
            ThreatLevel.CRITICAL: 0
        }
        
        for entity in self.blacklist_data["entities"].values():
            threat_level = entity.get("threat_level", ThreatLevel.MEDIUM)
            threat_distribution[threat_level] = threat_distribution.get(threat_level, 0) + 1
        
        for ip in self.blacklist_data["ip_addresses"].values():
            threat_level = ip.get("threat_level", ThreatLevel.MEDIUM)
            threat_distribution[threat_level] = threat_distribution.get(threat_level, 0) + 1
        
        for key in self.blacklist_data["api_keys"].values():
            threat_level = key.get("threat_level", ThreatLevel.HIGH)
            threat_distribution[threat_level] = threat_distribution.get(threat_level, 0) + 1
        
        return {
            "total_entities_blocked": len(self.blacklist_data["entities"]),
            "total_ips_blocked": len(self.blacklist_data["ip_addresses"]),
            "total_api_keys_blocked": len(self.blacklist_data["api_keys"]),
            "total_block_attempts": total_blocks,
            "threat_distribution": threat_distribution,
            "last_updated": self.blacklist_data["metadata"]["last_updated"],
            "created": self.blacklist_data["metadata"]["created"]
        }
    
    def get_blacklisted_entities(self) -> List[Dict[str, Any]]:
        """
        Get list of all blacklisted entities
        
        Returns:
            List of blacklisted entities
        """
        return list(self.blacklist_data["entities"].values())
    
    def get_blacklisted_ips(self) -> List[Dict[str, Any]]:
        """
        Get list of all blacklisted IP addresses
        
        Returns:
            List of blacklisted IP addresses
        """
        return list(self.blacklist_data["ip_addresses"].values())
    
    def verify_blacklist_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the blacklist data
        
        Returns:
            Dictionary with integrity verification results
        """
        integrity_hash = hashlib.sha256(
            json.dumps(self.blacklist_data, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            "verified": True,
            "integrity_hash": integrity_hash,
            "total_entries": (
                len(self.blacklist_data["entities"]) +
                len(self.blacklist_data["ip_addresses"]) +
                len(self.blacklist_data["api_keys"])
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global blacklist manager instance
_blacklist_manager = None

def get_blacklist_manager() -> BlacklistManager:
    """Get the global blacklist manager instance"""
    global _blacklist_manager
    if _blacklist_manager is None:
        _blacklist_manager = BlacklistManager()
    return _blacklist_manager
