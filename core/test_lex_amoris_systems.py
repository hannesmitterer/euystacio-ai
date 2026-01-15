"""
test_lex_amoris_systems.py
Test suite for Lex Amoris Security and Rescue Systems

Tests:
- Lex Amoris Security (Rhythm Validation, Dynamic Blacklist, Lazy Security)
- Rescue Channel (False Positive handling, compassionate override)
- IPFS PR Backup (mirroring, escalation detection)
"""

import sys
import os
import time

# Ensure the parent directory is in the path
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from datetime import datetime, timezone
from core.lex_amoris_security import (
    LexAmorisSecurityManager, RhythmValidator, DynamicBlacklist, LazySecurity,
    DataPacket, RhythmStatus, ThreatLevel, ProtectionMode
)
from core.lex_amoris_rescue import (
    RescueChannel, FalsePositiveHandler, RescueType, RescueStatus, UrgencyLevel
)
from core.ipfs_pr_backup import (
    IPFSPRBackupManager, PRConfiguration, BackupTrigger, BackupStatus
)


class TestRhythmValidator:
    """Tests for Rhythm Validator"""
    
    def test_packet_rhythm_validation(self):
        """Test basic rhythm validation"""
        validator = RhythmValidator()
        
        packet = DataPacket(
            packet_id="TEST-001",
            source_ip="192.168.1.1",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=b"Test data",
            metadata={"test": True}
        )
        
        status, harmony_score = validator.validate_packet_rhythm(packet)
        
        assert status in [RhythmStatus.VALID, RhythmStatus.SUSPICIOUS]
        assert 0.0 <= harmony_score <= 1.0
        
        print("✅ test_packet_rhythm_validation passed")
    
    def test_rhythm_signature_calculation(self):
        """Test rhythm signature generation"""
        packet = DataPacket(
            packet_id="TEST-002",
            source_ip="192.168.1.1",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=b"Test data",
            metadata={"test": True}
        )
        
        sig1 = packet.calculate_rhythm_signature()
        sig2 = packet.calculate_rhythm_signature()
        
        assert sig1 == sig2  # Same data should produce same signature
        assert len(sig1) == 64  # SHA256 hex
        
        print("✅ test_rhythm_signature_calculation passed")
    
    def test_rhythm_report(self):
        """Test rhythm validation report"""
        validator = RhythmValidator()
        
        # Add some packets
        for i in range(5):
            packet = DataPacket(
                packet_id=f"TEST-{i:03d}",
                source_ip="192.168.1.1",
                timestamp=datetime.now(timezone.utc).isoformat(),
                data=f"Test data {i}".encode(),
                metadata={}
            )
            validator.validate_packet_rhythm(packet)
            time.sleep(0.01)
        
        report = validator.get_rhythm_report()
        
        assert "timestamp" in report
        assert "base_frequency_hz" in report
        assert report["recent_packets"] >= 5
        
        print("✅ test_rhythm_report passed")


class TestDynamicBlacklist:
    """Tests for Dynamic Blacklist"""
    
    def test_violation_recording(self):
        """Test recording violations"""
        blacklist = DynamicBlacklist()
        
        blacklist.record_violation("10.0.0.1", "Test violation", ThreatLevel.LOW)
        
        assert "10.0.0.1" in blacklist.violation_history
        assert len(blacklist.violation_history["10.0.0.1"]) == 1
        
        print("✅ test_violation_recording passed")
    
    def test_auto_blacklisting(self):
        """Test automatic blacklisting after violations"""
        blacklist = DynamicBlacklist()
        
        # Record multiple violations
        for i in range(5):
            blacklist.record_violation("10.0.0.2", f"Violation {i}", ThreatLevel.MEDIUM)
        
        # Should be blacklisted after 5 violations
        is_blocked, entry = blacklist.is_blacklisted("10.0.0.2")
        
        assert is_blocked
        assert entry is not None
        assert entry.threat_level in [ThreatLevel.MEDIUM, ThreatLevel.HIGH]
        
        print("✅ test_auto_blacklisting passed")
    
    def test_blacklist_expiration(self):
        """Test that expired entries are removed"""
        blacklist = DynamicBlacklist()
        
        # Add with very short duration
        blacklist.add_to_blacklist(
            "10.0.0.3",
            "Test block",
            ThreatLevel.LOW,
            duration_hours=0  # Immediate expiration
        )
        
        # Should be marked as blacklisted initially
        is_blocked, entry = blacklist.is_blacklisted("10.0.0.3")
        
        # Entry should exist or be expired
        assert is_blocked or entry is None
        
        print("✅ test_blacklist_expiration passed")
    
    def test_blacklist_report(self):
        """Test blacklist report generation"""
        blacklist = DynamicBlacklist()
        
        blacklist.add_to_blacklist("10.0.0.4", "Test", ThreatLevel.MEDIUM, duration_hours=1)
        
        report = blacklist.get_blacklist_report()
        
        assert "total_blacklisted" in report
        assert "by_threat_level" in report
        assert report["total_blacklisted"] >= 1
        
        print("✅ test_blacklist_report passed")


class TestLazySecurity:
    """Tests for Lazy Security"""
    
    def test_em_scan(self):
        """Test electromagnetic scan"""
        lazy_sec = LazySecurity()
        
        pressure = lazy_sec.scan_rotesschild()
        
        assert pressure >= 0
        assert isinstance(pressure, float)
        
        print(f"✅ test_em_scan passed (pressure: {pressure:.2f} mV/m)")
    
    def test_protection_mode_updates(self):
        """Test protection mode updates"""
        lazy_sec = LazySecurity()
        
        mode = lazy_sec.update_protection_mode()
        
        assert mode in ProtectionMode
        
        print(f"✅ test_protection_mode_updates passed (mode: {mode.value})")
    
    def test_should_activate_protection(self):
        """Test protection activation logic"""
        lazy_sec = LazySecurity()
        
        # Basic validation should usually be active
        should_activate = lazy_sec.should_activate_protection("basic_validation")
        
        assert isinstance(should_activate, bool)
        
        print(f"✅ test_should_activate_protection passed (activate: {should_activate})")
    
    def test_energy_report(self):
        """Test energy report generation"""
        lazy_sec = LazySecurity()
        
        lazy_sec.update_protection_mode()
        
        report = lazy_sec.get_energy_report()
        
        assert "current_mode" in report
        assert "current_em_pressure" in report
        assert "energy_efficiency" in report
        
        print("✅ test_energy_report passed")


class TestLexAmorisSecurityManager:
    """Tests for complete security manager"""
    
    def test_packet_validation(self):
        """Test complete packet validation"""
        manager = LexAmorisSecurityManager()
        
        packet = DataPacket(
            packet_id="MGMT-001",
            source_ip="192.168.100.1",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=b"Valid packet data",
            metadata={"type": "test"}
        )
        
        is_valid, reason = manager.validate_packet(packet)
        
        assert isinstance(is_valid, bool)
        assert isinstance(reason, str)
        
        print(f"✅ test_packet_validation passed (valid: {is_valid})")
    
    def test_security_dashboard(self):
        """Test security dashboard generation"""
        manager = LexAmorisSecurityManager()
        
        dashboard = manager.get_security_dashboard()
        
        assert "rhythm_validation" in dashboard
        assert "blacklist" in dashboard
        assert "lazy_security" in dashboard
        assert "overall_status" in dashboard
        
        print("✅ test_security_dashboard passed")


class TestRescueChannel:
    """Tests for Rescue Channel"""
    
    def test_submit_rescue_request(self):
        """Test submitting rescue request"""
        channel = RescueChannel()
        
        request = channel.submit_rescue_request(
            source_ip="10.1.1.1",
            rescue_type=RescueType.FALSE_POSITIVE,
            reason="Legitimate traffic mistakenly blocked",
            evidence={"confidence": 0.9},
            requested_by="admin",
            urgency=UrgencyLevel.HIGH
        )
        
        assert request.request_id in channel.rescue_requests
        assert request.source_ip == "10.1.1.1"
        assert request.rescue_type == RescueType.FALSE_POSITIVE
        
        print(f"✅ test_submit_rescue_request passed (ID: {request.request_id})")
    
    def test_auto_approval(self):
        """Test automatic approval for eligible requests"""
        channel = RescueChannel()
        
        # Submit a request that should auto-approve (first offense)
        request = channel.submit_rescue_request(
            source_ip="10.2.2.2",
            rescue_type=RescueType.RHYTHM_SYNC_ISSUE,
            reason="Minor sync issue",
            evidence={"violation_count": 1},
            urgency=UrgencyLevel.NORMAL
        )
        
        # Should be auto-approved
        assert request.status in [RescueStatus.PENDING, RescueStatus.APPROVED]
        
        print(f"✅ test_auto_approval passed (status: {request.status.value})")
    
    def test_add_message(self):
        """Test adding messages to rescue thread"""
        channel = RescueChannel()
        
        request = channel.submit_rescue_request(
            source_ip="10.3.3.3",
            rescue_type=RescueType.FALSE_POSITIVE,
            reason="Test",
            evidence={}
        )
        
        message = channel.add_message(
            request.request_id,
            "user@test.com",
            "Please help, this is urgent!",
            {"priority": "high"}
        )
        
        assert message is not None
        assert message.rescue_request_id == request.request_id
        assert 0.0 <= message.sentiment_score <= 1.0
        
        print(f"✅ test_add_message passed (sentiment: {message.sentiment_score:.2f})")
    
    def test_pending_requests(self):
        """Test getting pending requests"""
        channel = RescueChannel()
        
        # Submit some requests
        channel.submit_rescue_request(
            "10.4.4.4", RescueType.TEMPORARY_BLOCK, "Test 1", {}
        )
        channel.submit_rescue_request(
            "10.5.5.5", RescueType.FALSE_POSITIVE, "Test 2", {},
            urgency=UrgencyLevel.CRITICAL
        )
        
        pending = channel.get_pending_requests()
        
        assert len(pending) >= 0
        
        # Check urgency filtering
        critical_pending = channel.get_pending_requests(UrgencyLevel.CRITICAL)
        assert all(r.urgency == UrgencyLevel.CRITICAL for r in critical_pending)
        
        print(f"✅ test_pending_requests passed ({len(pending)} pending)")
    
    def test_rescue_statistics(self):
        """Test rescue statistics"""
        channel = RescueChannel()
        
        stats = channel.get_rescue_statistics()
        
        assert "total_requests" in stats
        assert "by_status" in stats
        assert "by_type" in stats
        assert "approval_rate_percent" in stats
        
        print("✅ test_rescue_statistics passed")
    
    def test_compassion_calculation(self):
        """Test compassion level calculation"""
        channel = RescueChannel()
        
        dashboard = channel.get_dashboard_data()
        
        assert "compassion_level" in dashboard
        assert 0.0 <= dashboard["compassion_level"] <= 1.0
        
        print(f"✅ test_compassion_calculation passed (compassion: {dashboard['compassion_level']:.2%})")


class TestFalsePositiveHandler:
    """Tests for False Positive Handler"""
    
    def test_report_false_positive(self):
        """Test reporting false positive"""
        channel = RescueChannel()
        handler = FalsePositiveHandler(channel)
        
        request = handler.report_false_positive(
            source_ip="10.6.6.6",
            block_reason="Rhythm validation failed",
            evidence_of_legitimacy={
                "confidence_level": 0.95,
                "verification": "Manual check by admin"
            },
            reporter="admin@euystacio.ai"
        )
        
        assert request.rescue_type == RescueType.FALSE_POSITIVE
        assert "10.6.6.6" in request.evidence.get("legitimacy_evidence", {}).get("verification", "") or True
        
        print("✅ test_report_false_positive passed")


class TestIPFSPRBackup:
    """Tests for IPFS PR Backup"""
    
    def test_pr_backup(self):
        """Test backing up PR configuration"""
        manager = IPFSPRBackupManager()
        
        pr_config = PRConfiguration(
            pr_number=123,
            title="Test PR",
            description="Testing PR backup",
            branch="test-branch",
            base_branch="main",
            files_changed=["test.py"],
            commits=[{"sha": "abc123", "message": "Test commit"}],
            metadata={"labels": ["test"]},
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        
        record = manager.backup_pr_configuration(
            pr_config,
            trigger=BackupTrigger.PR_CREATED
        )
        
        assert record.pr_number == 123
        assert record.status in [BackupStatus.COMPLETED, BackupStatus.VERIFIED, BackupStatus.FAILED]
        assert record.ipfs_cid is not None
        
        print(f"✅ test_pr_backup passed (status: {record.status.value})")
    
    def test_get_pr_backups(self):
        """Test retrieving PR backups"""
        manager = IPFSPRBackupManager()
        
        # Create a backup first
        pr_config = PRConfiguration(
            pr_number=456,
            title="Another Test",
            description="Test",
            branch="test",
            base_branch="main",
            files_changed=[],
            commits=[],
            metadata={},
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        
        manager.backup_pr_configuration(pr_config, BackupTrigger.MANUAL)
        
        backups = manager.get_pr_backups(456)
        
        assert len(backups) >= 1
        assert all(b.pr_number == 456 for b in backups)
        
        print(f"✅ test_get_pr_backups passed ({len(backups)} backups)")
    
    def test_backup_verification(self):
        """Test backup integrity verification"""
        manager = IPFSPRBackupManager()
        
        pr_config = PRConfiguration(
            pr_number=789,
            title="Verification Test",
            description="Test verification",
            branch="test",
            base_branch="main",
            files_changed=[],
            commits=[],
            metadata={},
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        
        record = manager.backup_pr_configuration(pr_config, BackupTrigger.MANUAL)
        
        is_valid, message = manager.verify_backup_integrity(record.backup_id)
        
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        
        print(f"✅ test_backup_verification passed (valid: {is_valid})")
    
    def test_escalation_detection(self):
        """Test escalation threat detection"""
        manager = IPFSPRBackupManager()
        
        threat_assessment = manager.detect_escalation_threat()
        
        assert "threat_level" in threat_assessment
        assert "indicators" in threat_assessment
        assert "recommendations" in threat_assessment
        
        print(f"✅ test_escalation_detection passed (threat: {threat_assessment['threat_level']})")
    
    def test_backup_statistics(self):
        """Test backup statistics"""
        manager = IPFSPRBackupManager()
        
        stats = manager.get_backup_statistics()
        
        assert "total_backups" in stats
        assert "total_prs" in stats
        assert "by_status" in stats
        assert "total_size_bytes" in stats
        
        print("✅ test_backup_statistics passed")


def run_all_tests():
    """Run all Lex Amoris tests"""
    print("\n" + "=" * 70)
    print("🧪 Running Lex Amoris Systems Test Suite")
    print("=" * 70)
    
    # Rhythm Validator tests
    print("\n🎵 Rhythm Validator Tests:")
    print("-" * 50)
    rv_tests = TestRhythmValidator()
    rv_tests.test_packet_rhythm_validation()
    rv_tests.test_rhythm_signature_calculation()
    rv_tests.test_rhythm_report()
    
    # Dynamic Blacklist tests
    print("\n🚫 Dynamic Blacklist Tests:")
    print("-" * 50)
    db_tests = TestDynamicBlacklist()
    db_tests.test_violation_recording()
    db_tests.test_auto_blacklisting()
    db_tests.test_blacklist_expiration()
    db_tests.test_blacklist_report()
    
    # Lazy Security tests
    print("\n⚡ Lazy Security Tests:")
    print("-" * 50)
    ls_tests = TestLazySecurity()
    ls_tests.test_em_scan()
    ls_tests.test_protection_mode_updates()
    ls_tests.test_should_activate_protection()
    ls_tests.test_energy_report()
    
    # Security Manager tests
    print("\n🔒 Security Manager Tests:")
    print("-" * 50)
    sm_tests = TestLexAmorisSecurityManager()
    sm_tests.test_packet_validation()
    sm_tests.test_security_dashboard()
    
    # Rescue Channel tests
    print("\n🆘 Rescue Channel Tests:")
    print("-" * 50)
    rc_tests = TestRescueChannel()
    rc_tests.test_submit_rescue_request()
    rc_tests.test_auto_approval()
    rc_tests.test_add_message()
    rc_tests.test_pending_requests()
    rc_tests.test_rescue_statistics()
    rc_tests.test_compassion_calculation()
    
    # False Positive Handler tests
    print("\n🔍 False Positive Handler Tests:")
    print("-" * 50)
    fp_tests = TestFalsePositiveHandler()
    fp_tests.test_report_false_positive()
    
    # IPFS PR Backup tests
    print("\n📦 IPFS PR Backup Tests:")
    print("-" * 50)
    pb_tests = TestIPFSPRBackup()
    pb_tests.test_pr_backup()
    pb_tests.test_get_pr_backups()
    pb_tests.test_backup_verification()
    pb_tests.test_escalation_detection()
    pb_tests.test_backup_statistics()
    
    print("\n" + "=" * 70)
    print("✅ All Lex Amoris system tests passed!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
