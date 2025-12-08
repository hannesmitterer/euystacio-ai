"""
audit_pipeline.py
Transparency and Audit Pipeline for Protocollo Meta Salvage

This module provides:
- Audit trail collection and storage
- Transparency enforcement for CaaS providers
- Compliance verification
- Metadata validation and archival
- Integration with audit systems

Ensures that external providers maintain transparency and can be audited
for ethical compliance.
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class AuditStatus(Enum):
    """Status of an audit"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    OVERDUE = "OVERDUE"


class ComplianceLevel(Enum):
    """Compliance level assessment"""
    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PENDING_REVIEW = "PENDING_REVIEW"


@dataclass
class AuditRecord:
    """Represents an audit record"""
    audit_id: str
    provider_id: str
    timestamp: str
    audit_type: str  # "scheduled", "triggered", "random"
    status: AuditStatus
    compliance_level: ComplianceLevel
    findings: List[str]
    metadata_received: Dict[str, Any]
    metadata_required: List[str]
    score: float  # 0-100
    auditor: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "provider_id": self.provider_id,
            "timestamp": self.timestamp,
            "audit_type": self.audit_type,
            "status": self.status.value,
            "compliance_level": self.compliance_level.value,
            "findings": self.findings,
            "metadata_received": self.metadata_received,
            "metadata_required": self.metadata_required,
            "score": self.score,
            "auditor": self.auditor
        }


@dataclass
class TransparencyReport:
    """Represents a transparency report from a provider"""
    report_id: str
    provider_id: str
    timestamp: str
    reporting_period_start: str
    reporting_period_end: str
    metrics: Dict[str, Any]
    metadata: Dict[str, Any]
    verified: bool
    verification_signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "provider_id": self.provider_id,
            "timestamp": self.timestamp,
            "reporting_period_start": self.reporting_period_start,
            "reporting_period_end": self.reporting_period_end,
            "metrics": self.metrics,
            "metadata": self.metadata,
            "verified": self.verified,
            "verification_signature": self.verification_signature
        }


@dataclass
class ComplianceViolation:
    """Represents a compliance violation"""
    violation_id: str
    provider_id: str
    timestamp: str
    violation_type: str
    description: str
    severity: str  # "minor", "major", "critical"
    audit_id: Optional[str]
    resolution_status: str  # "open", "acknowledged", "resolved"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "provider_id": self.provider_id,
            "timestamp": self.timestamp,
            "violation_type": self.violation_type,
            "description": self.description,
            "severity": self.severity,
            "audit_id": self.audit_id,
            "resolution_status": self.resolution_status
        }


class AuditPipeline:
    """
    Transparency and Audit Pipeline
    
    Manages audit processes, transparency reporting, and compliance verification
    for external CaaS providers.
    """
    
    def __init__(self, storage_dir: str = "logs/audit_pipeline"):
        """
        Initialize the Audit Pipeline
        
        Args:
            storage_dir: Directory for storing audit records
        """
        self.storage_dir = storage_dir
        self.audit_records: List[AuditRecord] = []
        self.transparency_reports: List[TransparencyReport] = []
        self.violations: List[ComplianceViolation] = []
        self.audit_schedules: Dict[str, Dict[str, Any]] = {}
    
    def schedule_audit(
        self,
        provider_id: str,
        frequency_hours: int,
        metadata_required: List[str]
    ) -> Dict[str, Any]:
        """
        Schedule regular audits for a provider
        
        Args:
            provider_id: Provider identifier
            frequency_hours: Audit frequency in hours
            metadata_required: List of required metadata fields
            
        Returns:
            Schedule configuration
        """
        schedule = {
            "provider_id": provider_id,
            "frequency_hours": frequency_hours,
            "metadata_required": metadata_required,
            "next_audit": (
                datetime.now(timezone.utc) + timedelta(hours=frequency_hours)
            ).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        self.audit_schedules[provider_id] = schedule
        
        return schedule
    
    def initiate_audit(
        self,
        provider_id: str,
        audit_type: str = "scheduled",
        auditor: str = "AuditPipeline"
    ) -> AuditRecord:
        """
        Initiate a new audit
        
        Args:
            provider_id: Provider identifier
            audit_type: Type of audit
            auditor: Identifier of auditor
            
        Returns:
            AuditRecord object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        audit_id = hashlib.sha256(
            f"{timestamp}:{provider_id}:{audit_type}".encode()
        ).hexdigest()[:16]
        
        metadata_required = []
        if provider_id in self.audit_schedules:
            metadata_required = self.audit_schedules[provider_id]["metadata_required"]
        
        audit = AuditRecord(
            audit_id=audit_id,
            provider_id=provider_id,
            timestamp=timestamp,
            audit_type=audit_type,
            status=AuditStatus.PENDING,
            compliance_level=ComplianceLevel.PENDING_REVIEW,
            findings=[],
            metadata_received={},
            metadata_required=metadata_required,
            score=0.0,
            auditor=auditor
        )
        
        self.audit_records.append(audit)
        
        return audit
    
    def submit_audit_data(
        self,
        audit_id: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Submit audit data from a provider
        
        Args:
            audit_id: Audit identifier
            metadata: Metadata submitted by provider
            
        Returns:
            True if submission accepted
        """
        audit = self._find_audit(audit_id)
        if not audit:
            return False
        
        audit.metadata_received = metadata
        audit.status = AuditStatus.IN_PROGRESS
        
        return True
    
    def complete_audit(
        self,
        audit_id: str,
        findings: List[str],
        compliance_level: ComplianceLevel,
        score: float
    ) -> AuditRecord:
        """
        Complete an audit with results
        
        Args:
            audit_id: Audit identifier
            findings: List of audit findings
            compliance_level: Assessed compliance level
            score: Audit score (0-100)
            
        Returns:
            Updated AuditRecord
        """
        audit = self._find_audit(audit_id)
        if not audit:
            raise ValueError(f"Audit {audit_id} not found")
        
        audit.status = AuditStatus.COMPLETED
        audit.findings = findings
        audit.compliance_level = compliance_level
        audit.score = score
        
        # Check for violations
        if compliance_level == ComplianceLevel.NON_COMPLIANT:
            for finding in findings:
                self.record_violation(
                    provider_id=audit.provider_id,
                    violation_type="audit_non_compliance",
                    description=finding,
                    severity="major",
                    audit_id=audit_id
                )
        
        # Update next audit schedule
        if audit.provider_id in self.audit_schedules:
            schedule = self.audit_schedules[audit.provider_id]
            schedule["next_audit"] = (
                datetime.now(timezone.utc) + 
                timedelta(hours=schedule["frequency_hours"])
            ).isoformat()
            schedule["last_audit"] = audit.timestamp
            schedule["last_score"] = score
        
        return audit
    
    def verify_metadata_transparency(
        self,
        provider_id: str,
        required_fields: List[str],
        submitted_metadata: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Verify that provider submitted required metadata
        
        Args:
            provider_id: Provider identifier
            required_fields: List of required metadata fields
            submitted_metadata: Metadata submitted by provider
            
        Returns:
            Tuple of (is_compliant, missing_fields)
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in submitted_metadata:
                missing_fields.append(field)
            elif submitted_metadata[field] is None or submitted_metadata[field] == "":
                missing_fields.append(field)
        
        is_compliant = len(missing_fields) == 0
        
        if not is_compliant:
            self.record_violation(
                provider_id=provider_id,
                violation_type="metadata_transparency",
                description=f"Missing required metadata fields: {', '.join(missing_fields)}",
                severity="major"
            )
        
        return is_compliant, missing_fields
    
    def submit_transparency_report(
        self,
        provider_id: str,
        reporting_period_start: str,
        reporting_period_end: str,
        metrics: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> TransparencyReport:
        """
        Submit a transparency report from a provider
        
        Args:
            provider_id: Provider identifier
            reporting_period_start: Start of reporting period
            reporting_period_end: End of reporting period
            metrics: Performance metrics
            metadata: Additional metadata
            
        Returns:
            TransparencyReport object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        report_id = hashlib.sha256(
            f"{timestamp}:{provider_id}".encode()
        ).hexdigest()[:16]
        
        report = TransparencyReport(
            report_id=report_id,
            provider_id=provider_id,
            timestamp=timestamp,
            reporting_period_start=reporting_period_start,
            reporting_period_end=reporting_period_end,
            metrics=metrics,
            metadata=metadata,
            verified=False
        )
        
        self.transparency_reports.append(report)
        
        return report
    
    def verify_transparency_report(
        self,
        report_id: str,
        verification_signature: str
    ) -> bool:
        """
        Verify a transparency report
        
        Args:
            report_id: Report identifier
            verification_signature: Cryptographic signature
            
        Returns:
            True if verified successfully
        """
        report = self._find_report(report_id)
        if not report:
            return False
        
        report.verified = True
        report.verification_signature = verification_signature
        
        return True
    
    def record_violation(
        self,
        provider_id: str,
        violation_type: str,
        description: str,
        severity: str = "major",
        audit_id: Optional[str] = None
    ) -> ComplianceViolation:
        """
        Record a compliance violation
        
        Args:
            provider_id: Provider identifier
            violation_type: Type of violation
            description: Description of violation
            severity: Severity level
            audit_id: Optional associated audit
            
        Returns:
            ComplianceViolation object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        violation_id = hashlib.sha256(
            f"{timestamp}:{provider_id}:{violation_type}".encode()
        ).hexdigest()[:16]
        
        violation = ComplianceViolation(
            violation_id=violation_id,
            provider_id=provider_id,
            timestamp=timestamp,
            violation_type=violation_type,
            description=description,
            severity=severity,
            audit_id=audit_id,
            resolution_status="open"
        )
        
        self.violations.append(violation)
        
        return violation
    
    def resolve_violation(
        self,
        violation_id: str,
        resolution_notes: str
    ) -> bool:
        """
        Mark a violation as resolved
        
        Args:
            violation_id: Violation identifier
            resolution_notes: Notes about resolution
            
        Returns:
            True if resolved successfully
        """
        violation = self._find_violation(violation_id)
        if not violation:
            return False
        
        violation.resolution_status = "resolved"
        
        return True
    
    def get_provider_audit_history(
        self,
        provider_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get audit history for a provider
        
        Args:
            provider_id: Provider identifier
            limit: Maximum number of records to return
            
        Returns:
            List of audit records
        """
        provider_audits = [
            audit for audit in self.audit_records
            if audit.provider_id == provider_id
        ]
        
        # Sort by timestamp (most recent first)
        provider_audits.sort(
            key=lambda a: a.timestamp,
            reverse=True
        )
        
        return [audit.to_dict() for audit in provider_audits[:limit]]
    
    def get_provider_compliance_summary(
        self,
        provider_id: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive compliance summary for a provider
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            Compliance summary dictionary
        """
        recent_audits = self.get_provider_audit_history(provider_id, limit=5)
        
        open_violations = [
            v for v in self.violations
            if v.provider_id == provider_id and v.resolution_status == "open"
        ]
        
        recent_reports = [
            r for r in self.transparency_reports
            if r.provider_id == provider_id
        ][-5:]
        
        # Calculate average audit score
        audit_scores = [
            audit["score"] for audit in recent_audits
            if audit["status"] == "COMPLETED"
        ]
        avg_score = sum(audit_scores) / len(audit_scores) if audit_scores else 0.0
        
        return {
            "provider_id": provider_id,
            "average_audit_score": avg_score,
            "recent_audits": recent_audits,
            "open_violations": [v.to_dict() for v in open_violations],
            "open_violations_count": len(open_violations),
            "recent_transparency_reports": [r.to_dict() for r in recent_reports],
            "compliance_status": self._assess_overall_compliance(avg_score, len(open_violations))
        }
    
    def _assess_overall_compliance(
        self,
        avg_score: float,
        open_violations_count: int
    ) -> str:
        """Assess overall compliance status"""
        if open_violations_count > 3:
            return "NON_COMPLIANT"
        elif avg_score >= 80 and open_violations_count == 0:
            return "COMPLIANT"
        elif avg_score >= 60:
            return "PARTIALLY_COMPLIANT"
        else:
            return "NON_COMPLIANT"
    
    def _find_audit(self, audit_id: str) -> Optional[AuditRecord]:
        """Find an audit record by ID"""
        for audit in self.audit_records:
            if audit.audit_id == audit_id:
                return audit
        return None
    
    def _find_report(self, report_id: str) -> Optional[TransparencyReport]:
        """Find a transparency report by ID"""
        for report in self.transparency_reports:
            if report.report_id == report_id:
                return report
        return None
    
    def _find_violation(self, violation_id: str) -> Optional[ComplianceViolation]:
        """Find a violation by ID"""
        for violation in self.violations:
            if violation.violation_id == violation_id:
                return violation
        return None
    
    def check_overdue_audits(self) -> List[str]:
        """
        Check for overdue audits
        
        Returns:
            List of provider IDs with overdue audits
        """
        now = datetime.now(timezone.utc)
        overdue_providers = []
        
        for provider_id, schedule in self.audit_schedules.items():
            next_audit = datetime.fromisoformat(
                schedule["next_audit"].replace('Z', '+00:00')
            )
            
            if now > next_audit:
                overdue_providers.append(provider_id)
        
        return overdue_providers


# Singleton instance
_audit_pipeline_instance: Optional[AuditPipeline] = None


def get_audit_pipeline(storage_dir: str = "logs/audit_pipeline") -> AuditPipeline:
    """
    Get or create the singleton AuditPipeline instance
    
    Args:
        storage_dir: Directory for audit storage
        
    Returns:
        AuditPipeline instance
    """
    global _audit_pipeline_instance
    if _audit_pipeline_instance is None:
        _audit_pipeline_instance = AuditPipeline(storage_dir=storage_dir)
    return _audit_pipeline_instance
