"""
lex_amoris_rescue.py
Canale di Soccorso (Rescue Channel) for Euystacio AI

Implements:
- Emergency messaging based on Lex Amoris principles
- Unlocking mechanism for False Positive cases
- Integration with Sentimento Pulse Interface
- Compassionate override system

Based on Lex Amoris: Even in security, leave room for compassion and correction.
"""

import json
import os
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RescueType(Enum):
    """Type of rescue operation"""
    FALSE_POSITIVE = "FALSE_POSITIVE"
    TEMPORARY_BLOCK = "TEMPORARY_BLOCK"
    RHYTHM_SYNC_ISSUE = "RHYTHM_SYNC_ISSUE"
    EMERGENCY_OVERRIDE = "EMERGENCY_OVERRIDE"
    COMPASSIONATE_RELEASE = "COMPASSIONATE_RELEASE"


class RescueStatus(Enum):
    """Status of rescue request"""
    PENDING = "PENDING"
    REVIEWING = "REVIEWING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    COMPLETED = "COMPLETED"


class UrgencyLevel(Enum):
    """Urgency level of rescue"""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class RescueRequest:
    """Rescue request for unlocking a blocked source"""
    request_id: str
    source_ip: str
    rescue_type: RescueType
    urgency: UrgencyLevel
    reason: str
    evidence: Dict[str, Any]
    requested_at: str
    requested_by: Optional[str] = None
    status: RescueStatus = RescueStatus.PENDING
    reviewed_at: Optional[str] = None
    resolved_at: Optional[str] = None
    resolution_notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "source_ip": self.source_ip,
            "rescue_type": self.rescue_type.value,
            "urgency": self.urgency.value,
            "reason": self.reason,
            "evidence": self.evidence,
            "requested_at": self.requested_at,
            "requested_by": self.requested_by,
            "status": self.status.value,
            "reviewed_at": self.reviewed_at,
            "resolved_at": self.resolved_at,
            "resolution_notes": self.resolution_notes
        }


@dataclass
class RescueMessage:
    """Message in the rescue channel"""
    message_id: str
    rescue_request_id: str
    sender: str
    content: str
    timestamp: str
    sentiment_score: float  # Lex Amoris: measure compassion level
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "rescue_request_id": self.rescue_request_id,
            "sender": sender,
            "content": self.content,
            "timestamp": self.timestamp,
            "sentiment_score": self.sentiment_score,
            "metadata": self.metadata
        }


class RescueChannel:
    """
    Rescue Channel for handling false positives and emergency overrides
    
    Based on Lex Amoris: Security with compassion.
    Even strict systems need a way to correct mistakes.
    """
    
    def __init__(self, log_path: str = "logs/lex_amoris_rescue.log"):
        self.rescue_requests: Dict[str, RescueRequest] = {}
        self.rescue_messages: Dict[str, List[RescueMessage]] = {}
        self.auto_approval_rules: Dict[str, Any] = {}
        self.log_path = log_path
        self._ensure_log_directory()
        self._initialize_auto_approval_rules()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _initialize_auto_approval_rules(self):
        """Initialize automatic approval rules based on Lex Amoris"""
        self.auto_approval_rules = {
            # Compassionate rules for automatic approval
            "rhythm_sync": {
                "enabled": True,
                "max_violations": 2,
                "time_window_minutes": 10,
                "description": "Auto-approve for minor rhythm synchronization issues"
            },
            "temporary_block": {
                "enabled": True,
                "max_block_duration_hours": 1,
                "description": "Auto-approve for short temporary blocks"
            },
            "first_offense": {
                "enabled": True,
                "description": "Give first-time offenders a second chance"
            }
        }
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        return hashlib.sha256(f"RESCUE-{timestamp}".encode()).hexdigest()[:16].upper()
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        return hashlib.sha256(f"MSG-{timestamp}".encode()).hexdigest()[:12].upper()
    
    def _calculate_sentiment_score(self, content: str) -> float:
        """
        Calculate sentiment/compassion score of message
        
        Based on Lex Amoris: measure the love and understanding in communication.
        In production, this would use sentiment analysis.
        """
        # Simple heuristic based on compassionate keywords
        compassionate_words = [
            'please', 'help', 'understand', 'sorry', 'mistake', 'error',
            'temporary', 'urgent', 'need', 'critical', 'emergency',
            'accidentally', 'unintentionally', 'apologize'
        ]
        
        negative_words = [
            'attack', 'malicious', 'intentional', 'deliberate', 'hostile'
        ]
        
        content_lower = content.lower()
        
        compassion_count = sum(1 for word in compassionate_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        # Score from 0.0 to 1.0
        score = 0.5 + (compassion_count * 0.1) - (negative_count * 0.15)
        return max(0.0, min(1.0, score))
    
    def submit_rescue_request(self, 
                             source_ip: str,
                             rescue_type: RescueType,
                             reason: str,
                             evidence: Optional[Dict[str, Any]] = None,
                             requested_by: Optional[str] = None,
                             urgency: UrgencyLevel = UrgencyLevel.NORMAL) -> RescueRequest:
        """
        Submit a rescue request to unblock a source
        
        Args:
            source_ip: The IP address to rescue
            rescue_type: Type of rescue needed
            reason: Human-readable reason for rescue
            evidence: Supporting evidence for the request
            requested_by: Identifier of requester
            urgency: Urgency level
            
        Returns:
            Created RescueRequest
        """
        request_id = self._generate_request_id()
        timestamp = datetime.now(timezone.utc).isoformat()
        
        request = RescueRequest(
            request_id=request_id,
            source_ip=source_ip,
            rescue_type=rescue_type,
            urgency=urgency,
            reason=reason,
            evidence=evidence or {},
            requested_at=timestamp,
            requested_by=requested_by
        )
        
        self.rescue_requests[request_id] = request
        self.rescue_messages[request_id] = []
        
        # Check for auto-approval
        self._check_auto_approval(request)
        
        self._log_event("RESCUE_REQUEST_SUBMITTED", 
                       f"Request: {request_id}, IP: {source_ip}, Type: {rescue_type.value}")
        
        return request
    
    def _check_auto_approval(self, request: RescueRequest):
        """Check if request qualifies for automatic approval"""
        # Rule 1: Rhythm sync issues (minor, technical)
        if (request.rescue_type == RescueType.RHYTHM_SYNC_ISSUE and 
            self.auto_approval_rules["rhythm_sync"]["enabled"]):
            
            violation_count = request.evidence.get("violation_count", 0)
            if violation_count <= self.auto_approval_rules["rhythm_sync"]["max_violations"]:
                self._auto_approve(request, "Minor rhythm sync issue - auto-approved")
                return
        
        # Rule 2: Temporary blocks (short duration)
        if (request.rescue_type == RescueType.TEMPORARY_BLOCK and
            self.auto_approval_rules["temporary_block"]["enabled"]):
            
            block_duration = request.evidence.get("block_duration_hours", 0)
            if block_duration <= self.auto_approval_rules["temporary_block"]["max_block_duration_hours"]:
                self._auto_approve(request, "Short temporary block - auto-approved")
                return
        
        # Rule 3: First offense (compassionate second chance)
        if self.auto_approval_rules["first_offense"]["enabled"]:
            violation_count = request.evidence.get("violation_count", 0)
            if violation_count == 1:
                self._auto_approve(request, "First offense - compassionate approval")
                return
    
    def _auto_approve(self, request: RescueRequest, reason: str):
        """Automatically approve a rescue request"""
        timestamp = datetime.now(timezone.utc).isoformat()
        request.status = RescueStatus.APPROVED
        request.reviewed_at = timestamp
        request.resolved_at = timestamp
        request.resolution_notes = f"AUTO-APPROVED: {reason}"
        
        self._log_event("RESCUE_AUTO_APPROVED", 
                       f"Request: {request.request_id}, Reason: {reason}")
    
    def add_message(self, request_id: str, sender: str, content: str,
                   metadata: Optional[Dict[str, Any]] = None) -> Optional[RescueMessage]:
        """
        Add a message to a rescue request thread
        
        Args:
            request_id: The rescue request ID
            sender: Message sender identifier
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Created RescueMessage or None if request not found
        """
        if request_id not in self.rescue_requests:
            return None
        
        message_id = self._generate_message_id()
        timestamp = datetime.now(timezone.utc).isoformat()
        sentiment_score = self._calculate_sentiment_score(content)
        
        message = RescueMessage(
            message_id=message_id,
            rescue_request_id=request_id,
            sender=sender,
            content=content,
            timestamp=timestamp,
            sentiment_score=sentiment_score,
            metadata=metadata or {}
        )
        
        self.rescue_messages[request_id].append(message)
        
        self._log_event("RESCUE_MESSAGE", 
                       f"Request: {request_id}, Sender: {sender}, Sentiment: {sentiment_score:.2f}")
        
        return message
    
    def review_request(self, request_id: str, 
                      approve: bool, 
                      notes: str,
                      reviewer: str) -> bool:
        """
        Review and approve/deny a rescue request
        
        Args:
            request_id: Request to review
            approve: True to approve, False to deny
            notes: Review notes
            reviewer: Reviewer identifier
            
        Returns:
            True if successful
        """
        if request_id not in self.rescue_requests:
            return False
        
        request = self.rescue_requests[request_id]
        timestamp = datetime.now(timezone.utc).isoformat()
        
        request.status = RescueStatus.APPROVED if approve else RescueStatus.DENIED
        request.reviewed_at = timestamp
        request.resolved_at = timestamp
        request.resolution_notes = f"Reviewed by {reviewer}: {notes}"
        
        self._log_event("RESCUE_REVIEWED", 
                       f"Request: {request_id}, Approved: {approve}, Reviewer: {reviewer}")
        
        return True
    
    def get_pending_requests(self, urgency_filter: Optional[UrgencyLevel] = None) -> List[RescueRequest]:
        """Get all pending rescue requests"""
        requests = [
            r for r in self.rescue_requests.values()
            if r.status == RescueStatus.PENDING
        ]
        
        if urgency_filter:
            requests = [r for r in requests if r.urgency == urgency_filter]
        
        # Sort by urgency and timestamp
        urgency_order = {
            UrgencyLevel.CRITICAL: 0,
            UrgencyLevel.HIGH: 1,
            UrgencyLevel.NORMAL: 2,
            UrgencyLevel.LOW: 3
        }
        
        requests.sort(key=lambda r: (urgency_order[r.urgency], r.requested_at))
        
        return requests
    
    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a rescue request"""
        if request_id not in self.rescue_requests:
            return None
        
        request = self.rescue_requests[request_id]
        messages = self.rescue_messages.get(request_id, [])
        
        return {
            "request": request.to_dict(),
            "message_count": len(messages),
            "messages": [m.to_dict() for m in messages],
            "average_sentiment": (
                sum(m.sentiment_score for m in messages) / len(messages)
                if messages else 0.0
            )
        }
    
    def get_rescue_statistics(self) -> Dict[str, Any]:
        """Get statistics about rescue channel activity"""
        total_requests = len(self.rescue_requests)
        
        status_counts = {}
        for status in RescueStatus:
            status_counts[status.value] = len([
                r for r in self.rescue_requests.values()
                if r.status == status
            ])
        
        type_counts = {}
        for rescue_type in RescueType:
            type_counts[rescue_type.value] = len([
                r for r in self.rescue_requests.values()
                if r.rescue_type == rescue_type
            ])
        
        # Calculate approval rate
        approved = status_counts.get(RescueStatus.APPROVED.value, 0)
        denied = status_counts.get(RescueStatus.DENIED.value, 0)
        total_reviewed = approved + denied
        approval_rate = (approved / total_reviewed * 100) if total_reviewed > 0 else 0
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_requests": total_requests,
            "by_status": status_counts,
            "by_type": type_counts,
            "approval_rate_percent": round(approval_rate, 2),
            "total_messages": sum(len(msgs) for msgs in self.rescue_messages.values()),
            "auto_approval_rules": self.auto_approval_rules
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get rescue channel dashboard data"""
        pending = self.get_pending_requests()
        stats = self.get_rescue_statistics()
        
        # Get critical/high priority requests
        urgent_requests = [
            r for r in pending
            if r.urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.HIGH]
        ]
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pending_requests": len(pending),
            "urgent_requests": len(urgent_requests),
            "statistics": stats,
            "recent_requests": [
                r.to_dict() for r in list(self.rescue_requests.values())[-10:]
            ],
            "compassion_level": self._calculate_overall_compassion(),
            "system_health": "OPERATIONAL"
        }
    
    def _calculate_overall_compassion(self) -> float:
        """
        Calculate overall compassion level of the rescue system
        
        Based on Lex Amoris: measure how compassionate the system is
        """
        # Factors:
        # 1. Approval rate (higher is more compassionate)
        # 2. Average response time (faster is more compassionate)
        # 3. Auto-approval rules (more rules = more compassionate)
        
        stats = self.get_rescue_statistics()
        approval_rate = stats["approval_rate_percent"] / 100.0
        
        auto_rules_enabled = sum(
            1 for rule in self.auto_approval_rules.values()
            if rule.get("enabled", False)
        )
        auto_rules_score = min(auto_rules_enabled / 5.0, 1.0)  # Max 5 rules
        
        # Weighted average
        compassion_score = (approval_rate * 0.6) + (auto_rules_score * 0.4)
        
        return round(compassion_score, 3)
    
    def _log_event(self, event_type: str, message: str):
        """Log rescue channel event"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


class FalsePositiveHandler:
    """
    Handler for dealing with false positives
    
    Integrates with security system to unlock mistakenly blocked sources.
    """
    
    def __init__(self, rescue_channel: RescueChannel):
        self.rescue_channel = rescue_channel
    
    def report_false_positive(self,
                             source_ip: str,
                             block_reason: str,
                             evidence_of_legitimacy: Dict[str, Any],
                             reporter: str) -> RescueRequest:
        """
        Report a false positive blocking
        
        Args:
            source_ip: The mistakenly blocked IP
            block_reason: Original reason for blocking
            evidence_of_legitimacy: Evidence that source is legitimate
            reporter: Who is reporting the false positive
            
        Returns:
            Created rescue request
        """
        reason = f"False positive: {block_reason}"
        
        evidence = {
            "original_block_reason": block_reason,
            "legitimacy_evidence": evidence_of_legitimacy,
            "reporter": reporter
        }
        
        # Auto-escalate based on evidence strength
        urgency = UrgencyLevel.NORMAL
        if evidence_of_legitimacy.get("confidence_level", 0) > 0.8:
            urgency = UrgencyLevel.HIGH
        
        return self.rescue_channel.submit_rescue_request(
            source_ip=source_ip,
            rescue_type=RescueType.FALSE_POSITIVE,
            reason=reason,
            evidence=evidence,
            requested_by=reporter,
            urgency=urgency
        )
    
    def unlock_source(self, request_id: str) -> Tuple[bool, str]:
        """
        Unlock a source based on approved rescue request
        
        This would integrate with the actual security system.
        
        Returns:
            Tuple of (success, message)
        """
        request = self.rescue_channel.rescue_requests.get(request_id)
        
        if not request:
            return False, "Request not found"
        
        if request.status != RescueStatus.APPROVED:
            return False, f"Request not approved (status: {request.status.value})"
        
        # Here we would actually unlock the source in the security system
        # For now, just mark as completed
        request.status = RescueStatus.COMPLETED
        request.resolved_at = datetime.now(timezone.utc).isoformat()
        
        return True, f"Source {request.source_ip} unlocked successfully"


# Global instance
_rescue_channel: Optional[RescueChannel] = None


def get_rescue_channel() -> RescueChannel:
    """Get or create global rescue channel"""
    global _rescue_channel
    if _rescue_channel is None:
        _rescue_channel = RescueChannel()
    return _rescue_channel


if __name__ == "__main__":
    # Demo
    print("🆘 Lex Amoris Rescue Channel Demo")
    print("=" * 60)
    
    channel = RescueChannel()
    handler = FalsePositiveHandler(channel)
    
    # Submit a false positive report
    print("\n📋 Submitting false positive report...")
    request = handler.report_false_positive(
        source_ip="192.168.1.100",
        block_reason="Suspicious rhythm pattern",
        evidence_of_legitimacy={
            "confidence_level": 0.9,
            "verification": "Manual verification by admin",
            "history": "Long-term trusted source"
        },
        reporter="admin@euystacio.ai"
    )
    print(f"   Request ID: {request.request_id}")
    print(f"   Status: {request.status.value}")
    
    # Add a message to the request
    print("\n💬 Adding message to rescue thread...")
    message = channel.add_message(
        request.request_id,
        "admin@euystacio.ai",
        "This source has been verified as legitimate. Please unblock urgently.",
        {"priority": "high"}
    )
    print(f"   Message ID: {message.message_id}")
    print(f"   Sentiment Score: {message.sentiment_score:.2f}")
    
    # Get dashboard data
    print("\n📊 Rescue Channel Dashboard:")
    dashboard = channel.get_dashboard_data()
    print(f"   Pending Requests: {dashboard['pending_requests']}")
    print(f"   Compassion Level: {dashboard['compassion_level']:.2%}")
    print(f"   System Health: {dashboard['system_health']}")
    
    # Get statistics
    print("\n📈 Statistics:")
    stats = channel.get_rescue_statistics()
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Approval Rate: {stats['approval_rate_percent']:.1f}%")
    print(f"   Auto-approval Rules: {sum(1 for r in stats['auto_approval_rules'].values() if r.get('enabled'))}")
    
    print("\n✅ Rescue Channel Demo Complete!")
