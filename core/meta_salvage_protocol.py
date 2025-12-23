"""
meta_salvage_protocol.py
Main Orchestration Module for Protocollo Meta Salvage

This module provides:
- Automated workflow orchestration for ethical preservation
- Integration of all Meta Salvage components
- End-to-end automation of monitoring, decision-making, and enforcement
- Feedback loop for continuous improvement

The Protocollo Meta Salvage is the practical implementation of ethical
preservation during the Great Ethical Decommissioning (Epoca I della Dismissione Etica).
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.risk_monitor import (
    RiskMonitor, get_risk_monitor, RiskEvent, RiskLevel, RiskType
)
from core.peace_bonds import (
    PeaceBondsManager, get_peace_bonds_manager, PeaceBond, BondStatus
)
from core.decision_engine import (
    DecisionEngine, get_decision_engine, Decision, DecisionType
)
from core.audit_pipeline import (
    AuditPipeline, get_audit_pipeline, AuditStatus, ComplianceLevel
)


class ProtocolStatus(Enum):
    """Status of the Meta Salvage Protocol"""
    INITIALIZING = "INITIALIZING"
    MONITORING = "MONITORING"
    ACTIVE_INTERVENTION = "ACTIVE_INTERVENTION"
    AUDIT_MODE = "AUDIT_MODE"
    FEEDBACK_LEARNING = "FEEDBACK_LEARNING"
    SUSPENDED = "SUSPENDED"


@dataclass
class ProtocolExecution:
    """Represents a single protocol execution cycle"""
    execution_id: str
    timestamp: str
    status: ProtocolStatus
    providers_monitored: int
    risks_detected: int
    decisions_made: int
    bonds_imposed: int
    audits_completed: int
    duration_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "providers_monitored": self.providers_monitored,
            "risks_detected": self.risks_detected,
            "decisions_made": self.decisions_made,
            "bonds_imposed": self.bonds_imposed,
            "audits_completed": self.audits_completed,
            "duration_ms": self.duration_ms
        }


class MetaSalvageProtocol:
    """
    Protocollo Meta Salvage - Main Orchestration System
    
    Coordinates all components of the ethical preservation system:
    - Risk monitoring and detection
    - Autonomous decision making
    - Peace Bond enforcement
    - Audit and transparency
    - Feedback and learning
    """
    
    def __init__(self):
        """Initialize the Meta Salvage Protocol"""
        self.risk_monitor = get_risk_monitor()
        self.peace_bonds_manager = get_peace_bonds_manager()
        self.decision_engine = get_decision_engine()
        self.audit_pipeline = get_audit_pipeline()
        
        self.status = ProtocolStatus.INITIALIZING
        self.execution_history: List[ProtocolExecution] = []
        self.feedback_data: List[Dict[str, Any]] = []
        
        # Configuration
        self.config = {
            "monitoring_interval_seconds": 60,
            "auto_decision_enabled": True,
            "auto_bond_enforcement": True,
            "audit_frequency_hours": 24,
            "feedback_learning_enabled": True
        }
    
    def initialize(self) -> None:
        """Initialize the protocol and all subsystems"""
        print("🛡️ Initializing Protocollo Meta Salvage...")
        
        # Initialize subsystems
        print("  ✓ Risk Monitor initialized")
        print("  ✓ Peace Bonds Manager initialized")
        print("  ✓ Decision Engine initialized")
        print("  ✓ Audit Pipeline initialized")
        
        self.status = ProtocolStatus.MONITORING
        print("✅ Protocollo Meta Salvage ready")
    
    def execute_monitoring_cycle(
        self,
        provider_metrics: List[Dict[str, Any]]
    ) -> ProtocolExecution:
        """
        Execute a complete monitoring cycle
        
        Args:
            provider_metrics: List of current provider metrics
            
        Returns:
            ProtocolExecution record
        """
        start_time = datetime.now(timezone.utc)
        execution_id = f"EXEC_{start_time.isoformat()[:19].replace(':', '').replace('-', '')}"
        
        risks_detected = 0
        decisions_made = 0
        bonds_imposed = 0
        
        # Phase 1: Monitor all providers
        for metrics in provider_metrics:
            provider_id = metrics["provider_id"]
            
            # Record metrics
            self.risk_monitor.record_provider_metrics(
                provider_id=provider_id,
                latency_ms=metrics.get("latency_ms", 0),
                throughput_ops_sec=metrics.get("throughput_ops_sec", 0),
                cost_per_operation=metrics.get("cost_per_operation", 0),
                availability_pct=metrics.get("availability_pct", 100),
                symbiosis_score=metrics.get("symbiosis_score", 1.0)
            )
            
            # Record Symbiosis Score separately
            if "symbiosis_score" in metrics:
                self.risk_monitor.record_symbiosis_score(
                    provider_id=provider_id,
                    score=metrics["symbiosis_score"]
                )
        
        # Phase 2: Identify and process risks
        active_risks = self.risk_monitor.get_active_risks(hours=1)
        risks_detected = len(active_risks)
        
        for risk_event in active_risks:
            if risk_event.peace_bond_required:
                # Get provider context
                provider_status = self.risk_monitor.get_provider_status(
                    risk_event.provider_id
                )
                
                # Make decision
                decision = self.decision_engine.evaluate_risk_event(
                    risk_event=risk_event,
                    provider_context=provider_status.get("latest_metrics")
                )
                decisions_made += 1
                
                # Execute decision if auto-enforcement enabled
                if self.config["auto_bond_enforcement"]:
                    if decision.decision_type == DecisionType.IMPOSE_BOND:
                        self._impose_peace_bond(decision, risk_event)
                        bonds_imposed += 1
                    elif decision.decision_type == DecisionType.SUSPEND_PROVIDER:
                        self._suspend_provider(decision, risk_event)
        
        # Phase 3: Check bond compliance
        self._check_bond_compliance(provider_metrics)
        
        # Phase 4: Process audits
        audits_completed = self._process_audits()
        
        # Phase 5: Cleanup expired bonds
        self.peace_bonds_manager.cleanup_expired_bonds()
        
        # Record execution
        end_time = datetime.now(timezone.utc)
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        execution = ProtocolExecution(
            execution_id=execution_id,
            timestamp=start_time.isoformat(),
            status=self.status,
            providers_monitored=len(provider_metrics),
            risks_detected=risks_detected,
            decisions_made=decisions_made,
            bonds_imposed=bonds_imposed,
            audits_completed=audits_completed,
            duration_ms=duration_ms
        )
        
        self.execution_history.append(execution)
        
        return execution
    
    def _impose_peace_bond(
        self,
        decision: Decision,
        risk_event: RiskEvent
    ) -> PeaceBond:
        """
        Impose a Peace Bond based on a decision
        
        Args:
            decision: Decision object
            risk_event: Associated risk event
            
        Returns:
            PeaceBond object
        """
        # Determine duration based on risk level
        duration_hours = None
        if risk_event.risk_level == RiskLevel.MEDIUM:
            duration_hours = 72  # 3 days
        elif risk_event.risk_level == RiskLevel.HIGH:
            duration_hours = 168  # 1 week
        # CRITICAL risks get indefinite bonds
        
        bond = self.peace_bonds_manager.impose_bond(
            provider_id=decision.provider_id,
            constraints=decision.constraints,
            reason=f"{risk_event.risk_type.value}: {risk_event.description}",
            imposed_by="MetaSalvageProtocol",
            duration_hours=duration_hours,
            metadata={
                "risk_event_id": risk_event.event_id,
                "decision_id": decision.decision_id,
                "risk_level": risk_event.risk_level.value
            }
        )
        
        # Schedule audit if required
        audit_constraint = next(
            (c for c in decision.constraints if c.constraint_type.value == "AUDIT_REQUIREMENT"),
            None
        )
        if audit_constraint:
            self.audit_pipeline.schedule_audit(
                provider_id=decision.provider_id,
                frequency_hours=int(audit_constraint.limit_value),
                metadata_required=["operations_log", "performance_metrics", "cost_breakdown"]
            )
        
        return bond
    
    def _suspend_provider(
        self,
        decision: Decision,
        risk_event: RiskEvent
    ) -> None:
        """
        Suspend a provider due to critical risk
        
        Args:
            decision: Decision object
            risk_event: Associated risk event
        """
        # Create a highly restrictive bond
        severe_constraint = self.peace_bonds_manager.create_throughput_constraint(
            max_throughput_ops_sec=1.0,  # Essentially suspended
            description="Provider suspended due to critical ethical breach"
        )
        
        self.peace_bonds_manager.impose_bond(
            provider_id=decision.provider_id,
            constraints=[severe_constraint],
            reason=f"SUSPENDED: {risk_event.description}",
            imposed_by="MetaSalvageProtocol",
            duration_hours=None,  # Indefinite
            metadata={
                "suspension": True,
                "risk_event_id": risk_event.event_id,
                "decision_id": decision.decision_id
            }
        )
    
    def _check_bond_compliance(
        self,
        provider_metrics: List[Dict[str, Any]]
    ) -> None:
        """
        Check Peace Bond compliance for all providers
        
        Args:
            provider_metrics: Current provider metrics
        """
        for metrics in provider_metrics:
            provider_id = metrics["provider_id"]
            active_bonds = self.peace_bonds_manager.get_active_bonds_for_provider(provider_id)
            
            for bond in active_bonds:
                is_compliant, violations = self.peace_bonds_manager.check_constraint_compliance(
                    bond_id=bond.bond_id,
                    actual_values=metrics
                )
                
                if not is_compliant:
                    # Record violations
                    for violation_msg in violations:
                        self.peace_bonds_manager.record_violation(
                            bond_id=bond.bond_id,
                            constraint_violated=violation_msg,
                            actual_value=metrics.get("throughput", 0),
                            limit_value=0,
                            severity="major"
                        )
    
    def _process_audits(self) -> int:
        """
        Process scheduled audits
        
        Returns:
            Number of audits completed
        """
        audits_completed = 0
        
        # Check for overdue audits
        overdue_providers = self.audit_pipeline.check_overdue_audits()
        
        for provider_id in overdue_providers:
            # Initiate audit
            audit = self.audit_pipeline.initiate_audit(
                provider_id=provider_id,
                audit_type="scheduled",
                auditor="MetaSalvageProtocol"
            )
            
            # In a real system, this would trigger external audit processes
            # For now, we'll mark it as pending
            audits_completed += 1
        
        return audits_completed
    
    def collect_feedback(
        self,
        execution_id: str,
        effectiveness_score: float,
        notes: str
    ) -> None:
        """
        Collect feedback on protocol execution for learning
        
        Args:
            execution_id: Execution identifier
            effectiveness_score: Score (0-1) of how effective the execution was
            notes: Additional notes
        """
        feedback = {
            "execution_id": execution_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "effectiveness_score": effectiveness_score,
            "notes": notes
        }
        
        self.feedback_data.append(feedback)
        
        if self.config["feedback_learning_enabled"]:
            self._apply_feedback_learning()
    
    def _apply_feedback_learning(self) -> None:
        """
        Apply machine learning based on feedback
        
        This is a placeholder for ML model retraining based on audit data
        and effectiveness scores.
        """
        if len(self.feedback_data) < 10:
            return  # Need sufficient data
        
        # Calculate average effectiveness
        avg_effectiveness = sum(
            f["effectiveness_score"] for f in self.feedback_data[-10:]
        ) / 10
        
        # Adjust thresholds based on effectiveness
        if avg_effectiveness < 0.7:
            # System not effective enough, be more aggressive
            self.risk_monitor.thresholds["symbiosis_min"] += 0.05
        elif avg_effectiveness > 0.9:
            # System very effective, can be more lenient
            self.risk_monitor.thresholds["symbiosis_min"] -= 0.02
    
    def get_protocol_status(self) -> Dict[str, Any]:
        """
        Get comprehensive protocol status
        
        Returns:
            Status dictionary
        """
        all_providers = self.risk_monitor.get_all_providers_summary()
        active_bonds = self.peace_bonds_manager.get_all_active_bonds()
        recent_executions = self.execution_history[-10:]
        
        return {
            "status": self.status.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "configuration": self.config,
            "providers_monitored": len(all_providers),
            "active_bonds": len(active_bonds),
            "total_executions": len(self.execution_history),
            "recent_executions": [e.to_dict() for e in recent_executions],
            "providers_summary": all_providers,
            "active_bonds_summary": active_bonds
        }
    
    def generate_status_report(self) -> str:
        """
        Generate a human-readable status report
        
        Returns:
            Formatted status report
        """
        status = self.get_protocol_status()
        
        report_lines = [
            "=" * 70,
            "PROTOCOLLO META SALVAGE - STATUS REPORT",
            "=" * 70,
            "",
            f"Status: {status['status']}",
            f"Timestamp: {status['timestamp']}",
            "",
            "MONITORING SUMMARY:",
            f"  Providers Monitored: {status['providers_monitored']}",
            f"  Active Peace Bonds: {status['active_bonds']}",
            f"  Total Execution Cycles: {status['total_executions']}",
            "",
            "RECENT ACTIVITY:",
        ]
        
        for execution in status['recent_executions'][-5:]:
            report_lines.append(
                f"  [{execution['timestamp'][:19]}] "
                f"Risks: {execution['risks_detected']}, "
                f"Decisions: {execution['decisions_made']}, "
                f"Bonds: {execution['bonds_imposed']}"
            )
        
        report_lines.extend([
            "",
            "CONFIGURATION:",
            f"  Monitoring Interval: {self.config['monitoring_interval_seconds']}s",
            f"  Auto Decision: {self.config['auto_decision_enabled']}",
            f"  Auto Bond Enforcement: {self.config['auto_bond_enforcement']}",
            f"  Audit Frequency: {self.config['audit_frequency_hours']}h",
            f"  Feedback Learning: {self.config['feedback_learning_enabled']}",
            "",
            "=" * 70
        ])
        
        return "\n".join(report_lines)


# Singleton instance
_meta_salvage_protocol_instance: Optional[MetaSalvageProtocol] = None


def get_meta_salvage_protocol() -> MetaSalvageProtocol:
    """
    Get or create the singleton MetaSalvageProtocol instance
    
    Returns:
        MetaSalvageProtocol instance
    """
    global _meta_salvage_protocol_instance
    if _meta_salvage_protocol_instance is None:
        _meta_salvage_protocol_instance = MetaSalvageProtocol()
    return _meta_salvage_protocol_instance
