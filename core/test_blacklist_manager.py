"""
test_blacklist_manager.py
Tests for the Blacklist Manager System
"""

import os
import json
import tempfile
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timezone

# Import the blacklist manager
from core.blacklist_manager import (
    BlacklistManager,
    ThreatLevel,
    BlockReason,
    get_blacklist_manager
)


class TestBlacklistManager(unittest.TestCase):
    """Test suite for BlacklistManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.red_code_path = os.path.join(self.test_dir, 'red_code.json')
        
        # Create a mock red code system
        self.mock_red_code = Mock()
        self.mock_red_code.get_red_code.return_value = {
            "core_truth": "Test truth",
            "symbiosis_level": 0.1
        }
        self.mock_red_code._save_red_code = Mock()
        
        # Create blacklist manager with mock
        self.manager = BlacklistManager()
        self.manager.red_code = self.mock_red_code
    
    def test_add_entity_to_blacklist(self):
        """Test adding an entity to the blacklist"""
        result = self.manager.add_entity(
            entity_id="suspicious_node_001",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY,
            threat_level=ThreatLevel.HIGH
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["entity_id"], "suspicious_node_001")
        self.assertEqual(result["threat_level"], ThreatLevel.HIGH)
        
        # Verify entity is in blacklist
        self.assertIn("suspicious_node_001", self.manager.blacklist_data["entities"])
    
    def test_add_duplicate_entity(self):
        """Test adding a duplicate entity to the blacklist"""
        # Add entity first time
        self.manager.add_entity(
            entity_id="test_entity",
            entity_type="node",
            reason=BlockReason.ATTACK_ATTEMPT
        )
        
        # Try to add same entity again
        result = self.manager.add_entity(
            entity_id="test_entity",
            entity_type="node",
            reason=BlockReason.ATTACK_ATTEMPT
        )
        
        self.assertFalse(result["success"])
        self.assertIn("already blacklisted", result["message"])
    
    def test_add_ip_address_to_blacklist(self):
        """Test adding an IP address to the blacklist"""
        result = self.manager.add_ip_address(
            ip_address="192.168.1.100",
            reason=BlockReason.ATTACK_ATTEMPT,
            threat_level=ThreatLevel.CRITICAL
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["ip_address"], "192.168.1.100")
        self.assertEqual(result["threat_level"], ThreatLevel.CRITICAL)
        
        # Verify IP is in blacklist
        self.assertIn("192.168.1.100", self.manager.blacklist_data["ip_addresses"])
    
    def test_add_api_key_to_blacklist(self):
        """Test adding an API key to the blacklist"""
        import hashlib
        test_api_key = "test_api_key_12345"
        expected_hash = hashlib.sha256(test_api_key.encode()).hexdigest()
        
        result = self.manager.add_api_key(
            api_key_hash=expected_hash,
            reason=BlockReason.DATA_THEFT,
            threat_level=ThreatLevel.CRITICAL
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["threat_level"], ThreatLevel.CRITICAL)
        
        # Verify API key hash is in blacklist
        self.assertIn(expected_hash, self.manager.blacklist_data["api_keys"])
    
    def test_is_entity_blocked(self):
        """Test checking if an entity is blocked"""
        # Add entity to blacklist
        self.manager.add_entity(
            entity_id="blocked_entity",
            entity_type="service",
            reason=BlockReason.POLICY_VIOLATION
        )
        
        # Check if blocked
        self.assertTrue(self.manager.is_entity_blocked("blocked_entity"))
        
        # Check non-blocked entity
        self.assertFalse(self.manager.is_entity_blocked("normal_entity"))
    
    def test_is_ip_blocked(self):
        """Test checking if an IP address is blocked"""
        # Add IP to blacklist
        self.manager.add_ip_address(
            ip_address="10.0.0.1",
            reason=BlockReason.ATTACK_ATTEMPT
        )
        
        # Check if blocked
        self.assertTrue(self.manager.is_ip_blocked("10.0.0.1"))
        
        # Check non-blocked IP
        self.assertFalse(self.manager.is_ip_blocked("10.0.0.2"))
    
    def test_is_api_key_blocked(self):
        """Test checking if an API key is blocked"""
        import hashlib
        test_api_key = "blocked_key_67890"
        key_hash = hashlib.sha256(test_api_key.encode()).hexdigest()
        
        # Add API key to blacklist
        self.manager.add_api_key(
            api_key_hash=key_hash,
            reason=BlockReason.SECURITY_THREAT
        )
        
        # Check if blocked (using original key, which gets hashed)
        self.assertTrue(self.manager.is_api_key_blocked(test_api_key))
        
        # Check non-blocked API key
        self.assertFalse(self.manager.is_api_key_blocked("normal_key"))
    
    def test_block_count_increments(self):
        """Test that block count increments on each block attempt"""
        # Add entity to blacklist
        self.manager.add_entity(
            entity_id="test_entity",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY
        )
        
        # Check block count is initially 0
        initial_count = self.manager.blacklist_data["entities"]["test_entity"]["block_count"]
        self.assertEqual(initial_count, 0)
        
        # Trigger multiple block checks
        self.manager.is_entity_blocked("test_entity")
        self.manager.is_entity_blocked("test_entity")
        self.manager.is_entity_blocked("test_entity")
        
        # Check block count incremented
        final_count = self.manager.blacklist_data["entities"]["test_entity"]["block_count"]
        self.assertEqual(final_count, 3)
    
    def test_remove_entity(self):
        """Test removing an entity from the blacklist"""
        # Add entity
        self.manager.add_entity(
            entity_id="temp_entity",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY
        )
        
        # Verify entity is blocked
        self.assertTrue(self.manager.is_entity_blocked("temp_entity"))
        
        # Remove entity
        result = self.manager.remove_entity("temp_entity")
        self.assertTrue(result["success"])
        
        # Verify entity is no longer blocked
        self.assertFalse(self.manager.is_entity_blocked("temp_entity"))
    
    def test_remove_ip_address(self):
        """Test removing an IP address from the blacklist"""
        # Add IP
        self.manager.add_ip_address(
            ip_address="172.16.0.1",
            reason=BlockReason.ATTACK_ATTEMPT
        )
        
        # Verify IP is blocked
        self.assertTrue(self.manager.is_ip_blocked("172.16.0.1"))
        
        # Remove IP
        result = self.manager.remove_ip_address("172.16.0.1")
        self.assertTrue(result["success"])
        
        # Verify IP is no longer blocked
        self.assertFalse(self.manager.is_ip_blocked("172.16.0.1"))
    
    def test_get_blacklist_stats(self):
        """Test getting blacklist statistics"""
        # Add various entries
        self.manager.add_entity(
            entity_id="entity1",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY,
            threat_level=ThreatLevel.LOW
        )
        self.manager.add_entity(
            entity_id="entity2",
            entity_type="service",
            reason=BlockReason.ATTACK_ATTEMPT,
            threat_level=ThreatLevel.HIGH
        )
        self.manager.add_ip_address(
            ip_address="192.168.1.1",
            reason=BlockReason.ATTACK_ATTEMPT,
            threat_level=ThreatLevel.CRITICAL
        )
        
        # Get stats
        stats = self.manager.get_blacklist_stats()
        
        # Verify stats
        self.assertEqual(stats["total_entities_blocked"], 2)
        self.assertEqual(stats["total_ips_blocked"], 1)
        self.assertIn("threat_distribution", stats)
        self.assertEqual(stats["threat_distribution"][ThreatLevel.LOW], 1)
        self.assertEqual(stats["threat_distribution"][ThreatLevel.HIGH], 1)
        self.assertEqual(stats["threat_distribution"][ThreatLevel.CRITICAL], 1)
    
    def test_get_blacklisted_entities(self):
        """Test getting list of blacklisted entities"""
        # Add entities
        self.manager.add_entity(
            entity_id="entity1",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY
        )
        self.manager.add_entity(
            entity_id="entity2",
            entity_type="service",
            reason=BlockReason.ATTACK_ATTEMPT
        )
        
        # Get list
        entities = self.manager.get_blacklisted_entities()
        
        # Verify list
        self.assertEqual(len(entities), 2)
        entity_ids = [e["entity_id"] for e in entities]
        self.assertIn("entity1", entity_ids)
        self.assertIn("entity2", entity_ids)
    
    def test_verify_blacklist_integrity(self):
        """Test verifying blacklist integrity"""
        # Add some data
        self.manager.add_entity(
            entity_id="test_entity",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY
        )
        
        # Verify integrity
        result = self.manager.verify_blacklist_integrity()
        
        self.assertTrue(result["verified"])
        self.assertIn("integrity_hash", result)
        self.assertEqual(result["total_entries"], 1)
    
    def test_metadata_updates(self):
        """Test that metadata is updated correctly"""
        # Add entity
        self.manager.add_entity(
            entity_id="entity1",
            entity_type="node",
            reason=BlockReason.SUSPICIOUS_ACTIVITY
        )
        
        # Check metadata
        metadata = self.manager.blacklist_data["metadata"]
        self.assertEqual(metadata["total_blocked"], 1)
        self.assertIn("last_updated", metadata)
        self.assertIn("created", metadata)
        self.assertIn("ai_signature", metadata)


class TestBlacklistManagerIntegration(unittest.TestCase):
    """Integration tests for blacklist manager"""
    
    def test_get_blacklist_manager_singleton(self):
        """Test that get_blacklist_manager returns a singleton instance"""
        manager1 = get_blacklist_manager()
        manager2 = get_blacklist_manager()
        
        # Should be the same instance
        self.assertIs(manager1, manager2)


if __name__ == "__main__":
    unittest.main()
