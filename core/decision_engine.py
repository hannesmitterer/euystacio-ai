"""
decision_engine.py
Autonomous Decision Engine for Protocollo Meta Salvage

This module provides:
- Policy-based decision making for Peace Bond enforcement
- Integration with Open Policy Agent (OPA) concepts
- Automated constraint determination based on risk assessment
- Decision transparency and audit trail

The decision engine evaluates risk events and determines appropriate
Peace Bond constraints autonomously.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.risk_monitor import RiskEvent, RiskLevel, RiskType
from core.peace_bonds import Constraint, ConstraintType


class DecisionType(Enum):
    """Types of decisions"""
    IMPOSE_BOND = "IMPOSE_BOND"
    ESCALATE_BOND = "ESCALATE_BOND"
    LIFT_BOND = "LIFT_BOND"
    MONITOR_ONLY = "MONITOR_ONLY"
    SUSPEND_PROVIDER = "SUSPEND_PROVIDER"


@dataclass
class PolicyRule:
    """Represents a policy rule for decision making"""
    rule_id: str
    condition: str  # Description of when rule applies
    risk_types: List[RiskType]
    min_risk_level: RiskLevel
    decision: DecisionType
    constraints_template: List[Dict[str, Any]]
    priority: int  # Higher priority rules are evaluated first
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "condition": self.condition,
            "risk_types": [rt.value for rt in self.risk_types],
            "min_risk_level": self.min_risk_level.value,
            "decision": self.decision.value,
            "constraints_template": self.constraints_template,
            "priority": self.priority
        }


@dataclass
class Decision:
    """Represents a decision made by the engine"""
    decision_id: str
    timestamp: str
    decision_type: DecisionType
    provider_id: str
    risk_event_id: str
    reasoning: str
    constraints: List[Constraint]
    confidence_score: float
    applied_rule: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "decision_type": self.decision_type.value,
            "provider_id": self.provider_id,
            "risk_event_id": self.risk_event_id,
            "reasoning": self.reasoning,
            "constraints": [c.to_dict() for c in self.constraints],
            "confidence_score": self.confidence_score,
            "applied_rule": self.applied_rule,
            "metadata": self.metadata
        }


class DecisionEngine:
    """
    Autonomous Decision Engine
    
    Evaluates risk events and makes decisions about Peace Bond enforcement
    based on policy rules.
    """
    
    def __init__(self):
        """Initialize the Decision Engine"""
        self.policy_rules: List[PolicyRule] = []
        self.decisions: List[Decision] = []
        self._load_default_policies()
    
    def _load_default_policies(self) -> None:
        """Load default policy rules"""
        
        # Rule 1: Critical Symbiosis Decline
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_001",
            condition="Symbiosis Score drops below 0.75 or shows rapid decline",
            risk_types=[RiskType.SYMBIOSIS_DECLINE],
            min_risk_level=RiskLevel.HIGH,
            decision=DecisionType.IMPOSE_BOND,
            constraints_template=[
                {
                    "type": "THROUGHPUT_LIMIT",
                    "parameter": "throughput",
                    "limit_factor": 0.05,  # 5% of total throughput
                    "unit": "ops/sec"
                },
                {
                    "type": "AUDIT_REQUIREMENT",
                    "parameter": "audit_frequency",
                    "value": 12,  # Every 12 hours
                    "unit": "hours"
                }
            ],
            priority=10
        ))
        
        # Rule 2: Latency Manipulation
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_002",
            condition="Latency increases significantly or exceeds threshold",
            risk_types=[RiskType.LATENCY_MANIPULATION],
            min_risk_level=RiskLevel.MEDIUM,
            decision=DecisionType.IMPOSE_BOND,
            constraints_template=[
                {
                    "type": "LATENCY_CEILING",
                    "parameter": "latency",
                    "value": 100.0,  # 100ms max
                    "unit": "ms"
                },
                {
                    "type": "METADATA_TRANSPARENCY",
                    "parameter": "metadata_fields",
                    "value": ["latency_measurements", "network_topology", "routing_data"],
                    "unit": "fields"
                }
            ],
            priority=8
        ))
        
        # Rule 3: Cost Manipulation
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_003",
            condition="Cost increases significantly above expected rates",
            risk_types=[RiskType.COST_MANIPULATION],
            min_risk_level=RiskLevel.MEDIUM,
            decision=DecisionType.MONITOR_ONLY,
            constraints_template=[],
            priority=5
        ))
        
        # Rule 4: Data Flow Anomaly (High Severity)
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_004",
            condition="Critical availability or data flow issues detected",
            risk_types=[RiskType.DATA_FLOW_ANOMALY],
            min_risk_level=RiskLevel.HIGH,
            decision=DecisionType.IMPOSE_BOND,
            constraints_template=[
                {
                    "type": "THROUGHPUT_LIMIT",
                    "parameter": "throughput",
                    "limit_factor": 0.10,  # 10% throughput during recovery
                    "unit": "ops/sec"
                },
                {
                    "type": "AUDIT_REQUIREMENT",
                    "parameter": "audit_frequency",
                    "value": 6,  # Every 6 hours
                    "unit": "hours"
                }
            ],
            priority=9
        ))
        
        # Rule 5: Lock-in Attempt (Critical)
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_005",
            condition="Provider attempting to create vendor lock-in",
            risk_types=[RiskType.LOCK_IN_ATTEMPT],
            min_risk_level=RiskLevel.CRITICAL,
            decision=DecisionType.SUSPEND_PROVIDER,
            constraints_template=[],
            priority=15
        ))
        
        # Rule 6: Ethical Breach
        self.policy_rules.append(PolicyRule(
            rule_id="RULE_006",
            condition="Direct ethical breach detected",
            risk_types=[RiskType.ETHICAL_BREACH],
            min_risk_level=RiskLevel.HIGH,
            decision=DecisionType.IMPOSE_BOND,
            constraints_template=[
                {
                    "type": "THROUGHPUT_LIMIT",
                    "parameter": "throughput",
                    "limit_factor": 0.01,  # Severely limited to 1%
                    "unit": "ops/sec"
                },
                {
                    "type": "AUDIT_REQUIREMENT",
                    "parameter": "audit_frequency",
                    "value": 4,  # Every 4 hours
                    "unit": "hours"
                },
                {
                    "type": "METADATA_TRANSPARENCY",
                    "parameter": "metadata_fields",
                    "value": ["all_operations", "data_access_logs", "decision_logs"],
                    "unit": "fields"
                }
            ],
            priority=12
        ))
        
        # Sort rules by priority (descending)
        self.policy_rules.sort(key=lambda r: r.priority, reverse=True)
    
    def evaluate_risk_event(
        self,
        risk_event: RiskEvent,
        provider_context: Optional[Dict[str, Any]] = None
    ) -> Decision:
        """
        Evaluate a risk event and make a decision
        
        Args:
            risk_event: The risk event to evaluate
            provider_context: Additional context about the provider
            
        Returns:
            Decision object
        """
        provider_context = provider_context or {}
        
        # Find matching policy rule
        matching_rule = None
        for rule in self.policy_rules:
            if self._rule_matches(rule, risk_event):
                matching_rule = rule
                break
        
        if not matching_rule:
            # Default to monitoring if no rule matches
            matching_rule = PolicyRule(
                rule_id="DEFAULT",
                condition="No specific rule matched",
                risk_types=[],
                min_risk_level=RiskLevel.LOW,
                decision=DecisionType.MONITOR_ONLY,
                constraints_template=[],
                priority=0
            )
        
        # Generate constraints based on rule template
        constraints = self._generate_constraints(
            matching_rule.constraints_template,
            risk_event,
            provider_context
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(risk_event, matching_rule)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(risk_event, matching_rule, constraints)
        
        # Create decision
        timestamp = datetime.now(timezone.utc).isoformat()
        decision_id = f"DEC_{timestamp.replace(':', '').replace('-', '')[:14]}"
        
        decision = Decision(
            decision_id=decision_id,
            timestamp=timestamp,
            decision_type=matching_rule.decision,
            provider_id=risk_event.provider_id,
            risk_event_id=risk_event.event_id,
            reasoning=reasoning,
            constraints=constraints,
            confidence_score=confidence_score,
            applied_rule=matching_rule.rule_id,
            metadata={
                "risk_type": risk_event.risk_type.value,
                "risk_level": risk_event.risk_level.value,
                "provider_context": provider_context
            }
        )
        
        self.decisions.append(decision)
        
        return decision
    
    def _rule_matches(self, rule: PolicyRule, risk_event: RiskEvent) -> bool:
        """
        Check if a policy rule matches a risk event
        
        Args:
            rule: Policy rule to check
            risk_event: Risk event to match against
            
        Returns:
            True if rule matches
        """
        # Check risk type
        if rule.risk_types and risk_event.risk_type not in rule.risk_types:
            return False
        
        # Check risk level (event must be at or above minimum level)
        risk_levels = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        event_level_idx = risk_levels.index(risk_event.risk_level)
        rule_level_idx = risk_levels.index(rule.min_risk_level)
        
        if event_level_idx < rule_level_idx:
            return False
        
        return True
    
    def _generate_constraints(
        self,
        template: List[Dict[str, Any]],
        risk_event: RiskEvent,
        provider_context: Dict[str, Any]
    ) -> List[Constraint]:
        """
        Generate constraints from template
        
        Args:
            template: Constraint template from policy rule
            risk_event: Risk event context
            provider_context: Provider context
            
        Returns:
            List of Constraint objects
        """
        constraints = []
        
        for constraint_def in template:
            constraint_type = ConstraintType[constraint_def["type"]]
            parameter = constraint_def["parameter"]
            unit = constraint_def["unit"]
            
            # Calculate actual limit value
            if "value" in constraint_def:
                limit_value = constraint_def["value"]
            elif "limit_factor" in constraint_def:
                # Apply factor to current metrics
                base_value = provider_context.get(parameter, 10000)
                limit_value = base_value * constraint_def["limit_factor"]
            else:
                limit_value = None
            
            description = f"Constraint imposed due to {risk_event.risk_type.value}"
            
            constraints.append(Constraint(
                constraint_type=constraint_type,
                parameter=parameter,
                limit_value=limit_value,
                unit=unit,
                description=description,
                enforcement_method="hard" if constraint_type in [
                    ConstraintType.THROUGHPUT_LIMIT,
                    ConstraintType.LATENCY_CEILING
                ] else "audit"
            ))
        
        return constraints
    
    def _calculate_confidence(
        self,
        risk_event: RiskEvent,
        rule: PolicyRule
    ) -> float:
        """
        Calculate confidence score for the decision
        
        Args:
            risk_event: Risk event
            rule: Applied policy rule
            
        Returns:
            Confidence score (0-1)
        """
        base_confidence = 0.7
        
        # Adjust based on risk level
        if risk_event.risk_level == RiskLevel.CRITICAL:
            base_confidence += 0.2
        elif risk_event.risk_level == RiskLevel.HIGH:
            base_confidence += 0.15
        elif risk_event.risk_level == RiskLevel.MEDIUM:
            base_confidence += 0.05
        
        # Adjust based on rule priority
        if rule.priority >= 10:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    def _generate_reasoning(
        self,
        risk_event: RiskEvent,
        rule: PolicyRule,
        constraints: List[Constraint]
    ) -> str:
        """
        Generate human-readable reasoning for the decision
        
        Args:
            risk_event: Risk event
            rule: Applied policy rule
            constraints: Generated constraints
            
        Returns:
            Reasoning string
        """
        reasoning_parts = [
            f"Risk Type: {risk_event.risk_type.value}",
            f"Risk Level: {risk_event.risk_level.value}",
            f"Applied Rule: {rule.rule_id} - {rule.condition}",
            f"Decision: {rule.decision.value}"
        ]
        
        if constraints:
            reasoning_parts.append(
                f"Constraints: {len(constraints)} operational constraints imposed"
            )
        
        reasoning_parts.append(f"Rationale: {risk_event.description}")
        
        return " | ".join(reasoning_parts)
    
    def add_policy_rule(self, rule: PolicyRule) -> None:
        """
        Add a new policy rule
        
        Args:
            rule: PolicyRule to add
        """
        self.policy_rules.append(rule)
        self.policy_rules.sort(key=lambda r: r.priority, reverse=True)
    
    def get_policy_rules(self) -> List[Dict[str, Any]]:
        """
        Get all policy rules
        
        Returns:
            List of rule dictionaries
        """
        return [rule.to_dict() for rule in self.policy_rules]
    
    def get_decision_history(
        self,
        provider_id: Optional[str] = None,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Get decision history
        
        Args:
            provider_id: Optional filter by provider
            hours: Look back period in hours
            
        Returns:
            List of decision dictionaries
        """
        from datetime import timedelta
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        filtered_decisions = []
        for decision in self.decisions:
            decision_time = datetime.fromisoformat(decision.timestamp.replace('Z', '+00:00'))
            
            if decision_time < cutoff_time:
                continue
            
            if provider_id and decision.provider_id != provider_id:
                continue
            
            filtered_decisions.append(decision.to_dict())
        
        return filtered_decisions


# Singleton instance
_decision_engine_instance: Optional[DecisionEngine] = None


def get_decision_engine() -> DecisionEngine:
    """
    Get or create the singleton DecisionEngine instance
    
    Returns:
        DecisionEngine instance
    """
    global _decision_engine_instance
    if _decision_engine_instance is None:
        _decision_engine_instance = DecisionEngine()
    return _decision_engine_instance
