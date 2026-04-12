#!/usr/bin/env python3
"""
Test suite for security and resilience systems
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from security.forensic_response import ForensicResponseSystem
from security.firmware_update import FirmwareUpdateSystem
from security.ipfs_backup import IPFSBackupSystem
from security.protocol_hardening import ProtocolHardeningConfig


class TestForensicResponse(unittest.TestCase):
    """Test forensic response system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "forensic_config.json")
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_intrusion_detection(self):
        """Test intrusion pattern detection"""
        frs = ForensicResponseSystem(self.config_path)
        
        # Test various intrusion patterns
        test_cases = [
            ("2026-01-20 failed login attempt from 192.168.1.1", True),
            ("2026-01-20 unauthorized access detected", True),
            ("2026-01-20 normal operation", False),
            ("2026-01-20 SQL injection attempt blocked", True),
            ("2026-01-20 user logged in successfully", False)
        ]
        
        for log_line, should_detect in test_cases:
            detection = frs.detect_intrusion(log_line)
            if should_detect:
                self.assertIsNotNone(detection, f"Should detect: {log_line}")
            else:
                self.assertIsNone(detection, f"Should not detect: {log_line}")
    
    def test_severity_calculation(self):
        """Test severity level calculation"""
        frs = ForensicResponseSystem(self.config_path)
        
        self.assertEqual(frs._calculate_severity("sql injection"), "HIGH")
        self.assertEqual(frs._calculate_severity("unauthorized access"), "MEDIUM")
        self.assertEqual(frs._calculate_severity("invalid token"), "LOW")
    
    def test_config_save_load(self):
        """Test configuration save and load"""
        frs = ForensicResponseSystem(self.config_path)
        frs.config["alert_threshold"] = 10
        frs.save_config()
        
        # Load again
        frs2 = ForensicResponseSystem(self.config_path)
        self.assertEqual(frs2.config["alert_threshold"], 10)
    
    def test_get_status(self):
        """Test status retrieval"""
        frs = ForensicResponseSystem(self.config_path)
        status = frs.get_status()
        
        self.assertIn("monitoring_enabled", status)
        self.assertIn("alert_count", status)
        self.assertIn("response_mode", status)


class TestFirmwareUpdate(unittest.TestCase):
    """Test firmware update system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fus = FirmwareUpdateSystem(self.temp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_checksum_calculation(self):
        """Test checksum calculation"""
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        checksum = self.fus.calculate_checksum(test_file)
        self.assertEqual(len(checksum), 64)  # SHA-256 hex length
        
        # Verify same content gives same checksum
        checksum2 = self.fus.calculate_checksum(test_file)
        self.assertEqual(checksum, checksum2)
    
    def test_checksum_verification(self):
        """Test checksum verification"""
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        correct_checksum = self.fus.calculate_checksum(test_file)
        wrong_checksum = "0" * 64
        
        self.assertTrue(self.fus.verify_checksum(test_file, correct_checksum))
        self.assertFalse(self.fus.verify_checksum(test_file, wrong_checksum))
    
    def test_backup_creation(self):
        """Test backup creation"""
        # Create test files
        test_files = []
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"test{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"test content {i}")
            test_files.append(test_file)
        
        backup_id = "test_backup"
        backup_dir = self.fus.create_backup(test_files, backup_id)
        
        self.assertTrue(os.path.exists(backup_dir))
        manifest_path = os.path.join(backup_dir, "backup_manifest.json")
        self.assertTrue(os.path.exists(manifest_path))
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        self.assertEqual(len(manifest["files"]), 3)


class TestIPFSBackup(unittest.TestCase):
    """Test IPFS backup system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ipfs = IPFSBackupSystem(self.temp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_encryption_decryption(self):
        """Test file encryption and decryption"""
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content for encryption")
        
        # Encrypt
        encrypted_path = self.ipfs.encrypt_file(test_file)
        self.assertTrue(os.path.exists(encrypted_path))
        
        # Decrypt
        decrypted_path = os.path.join(self.temp_dir, "decrypted.txt")
        self.ipfs.decrypt_file(encrypted_path, decrypted_path)
        self.assertTrue(os.path.exists(decrypted_path))
        
        # Verify content
        with open(test_file, 'r') as f:
            original = f.read()
        with open(decrypted_path, 'r') as f:
            decrypted = f.read()
        
        self.assertEqual(original, decrypted)
    
    def test_ipfs_hash_generation(self):
        """Test IPFS hash generation"""
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        ipfs_hash = self.ipfs.add_to_ipfs(test_file)
        self.assertIsNotNone(ipfs_hash)
        self.assertTrue(ipfs_hash.startswith("Qm"))
    
    def test_backup_status(self):
        """Test backup status retrieval"""
        status = self.ipfs.get_backup_status()
        
        self.assertIn("ipfs_available", status)
        self.assertIn("gpg_available", status)
        self.assertIn("total_backups", status)


class TestProtocolHardening(unittest.TestCase):
    """Test protocol hardening"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "protocol_config.json")
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_tls_context_creation(self):
        """Test TLS context creation"""
        config = ProtocolHardeningConfig(self.config_path)
        
        context = config.create_tls_context()
        self.assertIsNotNone(context)
    
    def test_connection_validation(self):
        """Test connection validation"""
        config = ProtocolHardeningConfig(self.config_path)
        
        # Valid connections
        self.assertTrue(config.validate_connection("h3", encrypted=True))
        self.assertTrue(config.validate_connection("http/1.1", encrypted=True))
        
        # Invalid connections
        self.assertFalse(config.validate_connection("http", encrypted=False))
        self.assertFalse(config.validate_connection("unknown", encrypted=True))
    
    def test_quic_config(self):
        """Test QUIC configuration"""
        config = ProtocolHardeningConfig(self.config_path)
        quic_config = config.get_quic_config()
        
        self.assertIn("max_datagram_size", quic_config)
        self.assertIn("max_idle_timeout", quic_config)
        self.assertGreater(quic_config["max_datagram_size"], 0)
    
    def test_security_status(self):
        """Test security status"""
        config = ProtocolHardeningConfig(self.config_path)
        status = config.get_security_status()
        
        self.assertEqual(status["tls_version"], "TLS1_3")
        self.assertTrue(status["quic_enabled"])
        self.assertTrue(status["unencrypted_disabled"])


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestForensicResponse))
    suite.addTests(loader.loadTestsFromTestCase(TestFirmwareUpdate))
    suite.addTests(loader.loadTestsFromTestCase(TestIPFSBackup))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolHardening))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
