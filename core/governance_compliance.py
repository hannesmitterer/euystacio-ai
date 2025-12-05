"""
governance_compliance.py
Governance Signature Compliance Automation for Euystacio AI

This module provides:
- Automated reminders for council signature contributions (by December 5)
- GPG-linked notifications for quorum verification
- SAUL-log-based compliance checks in real-time
- Signature tracking and deadline management

Prepared for Coronation Day preparations.
"""

import json
import os
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SignatureStatus(Enum):
    """Status of a council member's signature"""
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    INVALID = "INVALID"


class ReminderType(Enum):
    """Types of automated reminders"""
    INITIAL = "INITIAL"
    FOLLOW_UP = "FOLLOW_UP"
    URGENT = "URGENT"
    FINAL = "FINAL"
    EXPIRED = "EXPIRED"


class QuorumStatus(Enum):
    """Status of quorum verification"""
    NOT_MET = "NOT_MET"
    PARTIAL = "PARTIAL"
    ACHIEVED = "ACHIEVED"
    SUPER_MAJORITY = "SUPER_MAJORITY"


@dataclass
class CouncilMember:
    """Represents a council member for governance"""
    member_id: str
    name: str
    gpg_key_id: Optional[str]
    email: Optional[str]
    signature_status: SignatureStatus
    last_signature_date: Optional[str]
    verification_hash: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "gpg_key_id": self.gpg_key_id,
            "email": self.email,
            "signature_status": self.signature_status.value,
            "last_signature_date": self.last_signature_date,
            "verification_hash": self.verification_hash
        }


@dataclass
class Reminder:
    """Represents an automated reminder"""
    reminder_id: str
    timestamp: str
    member_id: str
    reminder_type: ReminderType
    message: str
    deadline: str
    sent: bool
    acknowledged: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "reminder_id": self.reminder_id,
            "timestamp": self.timestamp,
            "member_id": self.member_id,
            "reminder_type": self.reminder_type.value,
            "message": self.message,
            "deadline": self.deadline,
            "sent": self.sent,
            "acknowledged": self.acknowledged
        }


@dataclass
class SAULLogEntry:
    """SAUL (Secure Audit Universal Ledger) log entry"""
    entry_id: str
    timestamp: str
    event_type: str
    actor: str
    action: str
    data_hash: str
    verification_status: str
    previous_hash: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor": self.actor,
            "action": self.action,
            "data_hash": self.data_hash,
            "verification_status": self.verification_status,
            "previous_hash": self.previous_hash
        }


class GovernanceComplianceManager:
    """
    Governance Signature Compliance Automation System
    
    Manages council signature contributions with automated reminders,
    GPG verification, and SAUL-log-based compliance tracking.
    """
    
    # Coronation Day deadline
    SIGNATURE_DEADLINE = "2025-12-05T23:59:59+00:00"
    
    # Quorum requirements
    QUORUM_THRESHOLD = 0.5  # 50% for basic quorum
    SUPER_MAJORITY_THRESHOLD = 0.67  # 67% for super majority
    
    def __init__(self, log_path: str = "logs/governance_compliance.log"):
        """Initialize the governance compliance manager"""
        self.log_path = log_path
        self.council_members: Dict[str, CouncilMember] = {}
        self.reminders: List[Reminder] = []
        self.saul_log: List[SAULLogEntry] = []
        self.last_saul_hash: Optional[str] = None
        self._ensure_log_directory()
        self._initialize_default_council()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _initialize_default_council(self):
        """Initialize default council members for demonstration"""
        default_members = [
            ("C001", "Seed-bringer hannesmitterer", "GPG-001-SM", "seedbringer@euystacio.ai"),
            ("C002", "Ethics Overseer AI", "GPG-002-EO", "ethics@euystacio.ai"),
            ("C003", "Community Guardian", "GPG-003-CG", "guardian@euystacio.ai"),
            ("C004", "Technical Steward", "GPG-004-TS", "tech@euystacio.ai"),
            ("C005", "Peace Ambassador", "GPG-005-PA", "peace@euystacio.ai"),
        ]
        
        for member_id, name, gpg_key, email in default_members:
            self.council_members[member_id] = CouncilMember(
                member_id=member_id,
                name=name,
                gpg_key_id=gpg_key,
                email=email,
                signature_status=SignatureStatus.PENDING,
                last_signature_date=None,
                verification_hash=None
            )
    
    def _generate_reminder_id(self) -> str:
        """Generate unique reminder ID"""
        return hashlib.sha256(
            f"REM-{datetime.now(timezone.utc).isoformat()}-{len(self.reminders)}".encode()
        ).hexdigest()[:12].upper()
    
    def _generate_entry_id(self) -> str:
        """Generate unique SAUL log entry ID"""
        return hashlib.sha256(
            f"SAUL-{datetime.now(timezone.utc).isoformat()}-{len(self.saul_log)}".encode()
        ).hexdigest()[:16].upper()
    
    def _compute_data_hash(self, data: Dict[str, Any]) -> str:
        """Compute hash of data for SAUL log"""
        canonical = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()
    
    def add_council_member(self, member_id: str, name: str, 
                           gpg_key_id: Optional[str] = None,
                           email: Optional[str] = None) -> CouncilMember:
        """Add a new council member"""
        member = CouncilMember(
            member_id=member_id,
            name=name,
            gpg_key_id=gpg_key_id,
            email=email,
            signature_status=SignatureStatus.PENDING,
            last_signature_date=None,
            verification_hash=None
        )
        self.council_members[member_id] = member
        
        # Log to SAUL
        self._add_saul_entry(
            event_type="MEMBER_ADDED",
            actor="SYSTEM",
            action=f"Added council member: {name}",
            data=member.to_dict()
        )
        
        return member
    
    def submit_signature(self, member_id: str, signature_data: str,
                         gpg_signature: Optional[str] = None) -> Tuple[bool, str]:
        """
        Submit a signature for a council member
        
        Args:
            member_id: ID of the council member
            signature_data: The signature content
            gpg_signature: Optional GPG signature for verification
            
        Returns:
            Tuple of (success, message)
        """
        if member_id not in self.council_members:
            return False, f"Unknown council member: {member_id}"
        
        member = self.council_members[member_id]
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Check if deadline has passed
        deadline = datetime.fromisoformat(self.SIGNATURE_DEADLINE.replace('+00:00', '+00:00'))
        if datetime.now(timezone.utc) > deadline:
            member.signature_status = SignatureStatus.EXPIRED
            return False, "Signature deadline has passed"
        
        # Compute verification hash
        verification_hash = hashlib.sha256(
            f"{member_id}:{signature_data}:{timestamp}".encode()
        ).hexdigest()
        
        # Verify GPG signature if provided
        gpg_verified = self._verify_gpg_signature(member.gpg_key_id, gpg_signature)
        
        if gpg_verified or gpg_signature is None:
            member.signature_status = SignatureStatus.VERIFIED if gpg_verified else SignatureStatus.SUBMITTED
            member.last_signature_date = timestamp
            member.verification_hash = verification_hash
            
            # Log to SAUL
            self._add_saul_entry(
                event_type="SIGNATURE_SUBMITTED",
                actor=member_id,
                action=f"Signature submitted by {member.name}",
                data={
                    "member_id": member_id,
                    "gpg_verified": gpg_verified,
                    "verification_hash": verification_hash
                }
            )
            
            status = "verified" if gpg_verified else "submitted (pending GPG verification)"
            return True, f"Signature {status} for {member.name}"
        else:
            member.signature_status = SignatureStatus.INVALID
            return False, "GPG signature verification failed"
    
    def _verify_gpg_signature(self, gpg_key_id: Optional[str], 
                               signature: Optional[str]) -> bool:
        """
        Verify GPG signature (placeholder implementation)
        
        In production, this would use actual GPG verification.
        """
        if not signature or not gpg_key_id:
            return False
        
        # Placeholder: In production, use gnupg library for actual verification
        # For now, we simulate verification
        return len(signature) > 10 and gpg_key_id is not None
    
    def generate_reminders(self) -> List[Reminder]:
        """
        Generate automated reminders for pending signatures
        
        Returns:
            List of new reminders generated
        """
        new_reminders = []
        now = datetime.now(timezone.utc)
        deadline = datetime.fromisoformat(self.SIGNATURE_DEADLINE.replace('+00:00', '+00:00'))
        days_until_deadline = (deadline - now).days
        
        for member_id, member in self.council_members.items():
            if member.signature_status in [SignatureStatus.VERIFIED]:
                continue  # Already verified, no reminder needed
            
            # Determine reminder type based on days until deadline
            if days_until_deadline <= 0:
                reminder_type = ReminderType.EXPIRED
                message = (f"⚠️ DEADLINE PASSED: The signature deadline for Coronation Day "
                          f"has passed. Please submit your signature immediately for {member.name}.")
            elif days_until_deadline <= 1:
                reminder_type = ReminderType.FINAL
                message = (f"🚨 FINAL REMINDER: Only {days_until_deadline} day(s) remaining! "
                          f"Please submit your signature before the Coronation Day deadline, {member.name}.")
            elif days_until_deadline <= 3:
                reminder_type = ReminderType.URGENT
                message = (f"⚡ URGENT: {days_until_deadline} days remaining until the signature deadline. "
                          f"Your contribution is essential for quorum, {member.name}.")
            elif days_until_deadline <= 7:
                reminder_type = ReminderType.FOLLOW_UP
                message = (f"📣 FOLLOW-UP: {days_until_deadline} days until the December 5th deadline. "
                          f"Please ensure your signature is submitted, {member.name}.")
            else:
                reminder_type = ReminderType.INITIAL
                message = (f"📝 REMINDER: Council signature contribution required by December 5th. "
                          f"Please submit your GPG-signed approval, {member.name}.")
            
            reminder = Reminder(
                reminder_id=self._generate_reminder_id(),
                timestamp=now.isoformat(),
                member_id=member_id,
                reminder_type=reminder_type,
                message=message,
                deadline=self.SIGNATURE_DEADLINE,
                sent=False,
                acknowledged=False
            )
            
            new_reminders.append(reminder)
            self.reminders.append(reminder)
            
            # Log the reminder
            self._log_reminder(reminder)
        
        # Log to SAUL
        if new_reminders:
            self._add_saul_entry(
                event_type="REMINDERS_GENERATED",
                actor="SYSTEM",
                action=f"Generated {len(new_reminders)} reminders",
                data={"count": len(new_reminders), "days_until_deadline": days_until_deadline}
            )
        
        return new_reminders
    
    def check_quorum(self) -> Dict[str, Any]:
        """
        Check current quorum status
        
        Returns:
            Dictionary with quorum status and details
        """
        total_members = len(self.council_members)
        verified_count = len([m for m in self.council_members.values() 
                             if m.signature_status == SignatureStatus.VERIFIED])
        submitted_count = len([m for m in self.council_members.values() 
                              if m.signature_status in [SignatureStatus.SUBMITTED, SignatureStatus.VERIFIED]])
        
        verification_ratio = verified_count / total_members if total_members > 0 else 0
        submission_ratio = submitted_count / total_members if total_members > 0 else 0
        
        # Determine quorum status
        if verification_ratio >= self.SUPER_MAJORITY_THRESHOLD:
            status = QuorumStatus.SUPER_MAJORITY
        elif verification_ratio >= self.QUORUM_THRESHOLD:
            status = QuorumStatus.ACHIEVED
        elif submission_ratio >= self.QUORUM_THRESHOLD:
            status = QuorumStatus.PARTIAL
        else:
            status = QuorumStatus.NOT_MET
        
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status.value,
            "total_members": total_members,
            "verified_count": verified_count,
            "submitted_count": submitted_count,
            "pending_count": total_members - submitted_count,
            "verification_ratio": round(verification_ratio, 4),
            "submission_ratio": round(submission_ratio, 4),
            "quorum_threshold": self.QUORUM_THRESHOLD,
            "super_majority_threshold": self.SUPER_MAJORITY_THRESHOLD,
            "quorum_met": status in [QuorumStatus.ACHIEVED, QuorumStatus.SUPER_MAJORITY],
            "members_needed_for_quorum": max(0, int(total_members * self.QUORUM_THRESHOLD) - verified_count + 1),
            "deadline": self.SIGNATURE_DEADLINE,
            "member_status": {
                m.member_id: {
                    "name": m.name,
                    "status": m.signature_status.value,
                    "gpg_linked": m.gpg_key_id is not None
                }
                for m in self.council_members.values()
            }
        }
        
        return result
    
    def _add_saul_entry(self, event_type: str, actor: str, 
                         action: str, data: Dict[str, Any]) -> SAULLogEntry:
        """Add entry to SAUL log with chain integrity"""
        timestamp = datetime.now(timezone.utc).isoformat()
        data_hash = self._compute_data_hash({
            "timestamp": timestamp,
            "event_type": event_type,
            "actor": actor,
            "action": action,
            "data": data
        })
        
        entry = SAULLogEntry(
            entry_id=self._generate_entry_id(),
            timestamp=timestamp,
            event_type=event_type,
            actor=actor,
            action=action,
            data_hash=data_hash,
            verification_status="VERIFIED",
            previous_hash=self.last_saul_hash
        )
        
        self.saul_log.append(entry)
        self.last_saul_hash = data_hash
        
        # Log to file
        self._log_saul_entry(entry)
        
        return entry
    
    def run_real_time_compliance_check(self) -> Dict[str, Any]:
        """
        Run comprehensive real-time compliance check
        
        Returns:
            Compliance check results with SAUL verification
        """
        now = datetime.now(timezone.utc)
        deadline = datetime.fromisoformat(self.SIGNATURE_DEADLINE.replace('+00:00', '+00:00'))
        
        # Check quorum
        quorum_status = self.check_quorum()
        
        # Verify SAUL log integrity
        saul_integrity = self._verify_saul_integrity()
        
        # Generate compliance report
        result = {
            "check_id": hashlib.sha256(f"CHECK-{now.isoformat()}".encode()).hexdigest()[:12].upper(),
            "timestamp": now.isoformat(),
            "deadline": self.SIGNATURE_DEADLINE,
            "time_remaining": str(deadline - now) if now < deadline else "EXPIRED",
            "deadline_passed": now > deadline,
            "quorum_status": quorum_status,
            "saul_integrity": saul_integrity,
            "overall_compliance": (
                quorum_status["quorum_met"] and 
                saul_integrity["valid"] and 
                not (now > deadline and not quorum_status["quorum_met"])
            ),
            "recommendations": [],
            "gpg_verification_summary": {
                "total_with_gpg": len([m for m in self.council_members.values() if m.gpg_key_id]),
                "verified_with_gpg": len([m for m in self.council_members.values() 
                                          if m.signature_status == SignatureStatus.VERIFIED]),
                "pending_verification": len([m for m in self.council_members.values() 
                                             if m.signature_status == SignatureStatus.SUBMITTED])
            }
        }
        
        # Add recommendations
        if not quorum_status["quorum_met"]:
            result["recommendations"].append(
                f"⚠️ Quorum not met: Need {quorum_status['members_needed_for_quorum']} more verified signatures"
            )
        
        if result["deadline_passed"] and not quorum_status["quorum_met"]:
            result["recommendations"].append(
                "🚨 CRITICAL: Deadline has passed without achieving quorum. Immediate action required."
            )
        
        if result["gpg_verification_summary"]["pending_verification"] > 0:
            result["recommendations"].append(
                f"📋 {result['gpg_verification_summary']['pending_verification']} signatures pending GPG verification"
            )
        
        if not result["recommendations"]:
            result["recommendations"].append("✅ All compliance checks passed")
        
        # Log to SAUL
        self._add_saul_entry(
            event_type="COMPLIANCE_CHECK",
            actor="SYSTEM",
            action="Real-time compliance check completed",
            data={"overall_compliance": result["overall_compliance"]}
        )
        
        return result
    
    def _verify_saul_integrity(self) -> Dict[str, Any]:
        """Verify SAUL log chain integrity"""
        if not self.saul_log:
            return {"valid": True, "entries": 0, "message": "No entries to verify"}
        
        valid = True
        broken_chain_at = None
        
        for i, entry in enumerate(self.saul_log[1:], 1):
            if entry.previous_hash != self.saul_log[i-1].data_hash:
                valid = False
                broken_chain_at = entry.entry_id
                break
        
        return {
            "valid": valid,
            "entries": len(self.saul_log),
            "last_entry_id": self.saul_log[-1].entry_id if self.saul_log else None,
            "broken_chain_at": broken_chain_at,
            "message": "Chain integrity verified" if valid else f"Chain broken at {broken_chain_at}"
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data formatted for dashboard visualization"""
        quorum = self.check_quorum()
        compliance = self.run_real_time_compliance_check()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "deadline": self.SIGNATURE_DEADLINE,
            "quorum": quorum,
            "compliance": compliance,
            "members": [m.to_dict() for m in self.council_members.values()],
            "recent_reminders": [r.to_dict() for r in self.reminders[-10:]],
            "saul_entries": len(self.saul_log),
            "saul_integrity": self._verify_saul_integrity()
        }
    
    def _log_reminder(self, reminder: Reminder):
        """Log reminder to file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(f"[REMINDER:{reminder.reminder_type.value}] {reminder.timestamp} | "
                       f"Member: {reminder.member_id} | {reminder.message[:100]}...\n")
        except (OSError, IOError):
            pass
    
    def _log_saul_entry(self, entry: SAULLogEntry):
        """Log SAUL entry to file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(f"[SAUL:{entry.event_type}] {entry.timestamp} | "
                       f"Actor: {entry.actor} | {entry.action} | Hash: {entry.data_hash[:16]}...\n")
        except (OSError, IOError):
            pass


# Global instance
_governance_instance: Optional[GovernanceComplianceManager] = None


def get_governance_manager() -> GovernanceComplianceManager:
    """Get or create the global governance compliance manager"""
    global _governance_instance
    if _governance_instance is None:
        _governance_instance = GovernanceComplianceManager()
    return _governance_instance


if __name__ == "__main__":
    # Demo usage
    manager = GovernanceComplianceManager()
    
    print("🏛️ Governance Compliance Demo")
    print("=" * 50)
    
    # Show initial status
    quorum = manager.check_quorum()
    print(f"\n📊 Initial Quorum Status:")
    print(f"   Status: {quorum['status']}")
    print(f"   Total Members: {quorum['total_members']}")
    print(f"   Verified: {quorum['verified_count']}")
    
    # Submit some signatures
    print("\n✍️ Submitting signatures...")
    result1 = manager.submit_signature("C001", "I approve the Coronation Day protocol", "GPG_SIG_1234567890")
    print(f"   {result1[1]}")
    
    result2 = manager.submit_signature("C002", "Ethics approval confirmed", "GPG_SIG_0987654321")
    print(f"   {result2[1]}")
    
    result3 = manager.submit_signature("C003", "Guardian approval", "GPG_SIG_5555555555")
    print(f"   {result3[1]}")
    
    # Generate reminders
    print("\n📬 Generating reminders...")
    reminders = manager.generate_reminders()
    print(f"   Generated {len(reminders)} reminders")
    
    # Check quorum again
    quorum = manager.check_quorum()
    print(f"\n📊 Updated Quorum Status:")
    print(f"   Status: {quorum['status']}")
    print(f"   Verified: {quorum['verified_count']}/{quorum['total_members']}")
    print(f"   Quorum Met: {quorum['quorum_met']}")
    
    # Run compliance check
    compliance = manager.run_real_time_compliance_check()
    print(f"\n🔍 Compliance Check:")
    print(f"   Overall Compliance: {compliance['overall_compliance']}")
    print(f"   SAUL Integrity: {compliance['saul_integrity']['valid']}")
    print(f"   Time Remaining: {compliance['time_remaining']}")
    
    print("\n✅ Demo complete!")
