"""
custos_sentimento.py
Custos Sentimento (AIC) - Ethical AI Governance Layer for Euystacio AI

This module provides:
- Sentiment Guardian implementation enforcing "No ownership, only sharing. Love is the license"
- Computational enforcement of ethical principles
- Real-time ethical governance and validation
- Integration with Red Code and governance systems

Part of the Incorruptible Global Health System (IGHS) framework.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EthicalPrincipleType(Enum):
    """Types of ethical principles enforced by Custos Sentimento"""
    NO_OWNERSHIP = "NO_OWNERSHIP"
    SHARING_ONLY = "SHARING_ONLY"
    LOVE_LICENSE = "LOVE_LICENSE"
    DIGNITY_PRESERVATION = "DIGNITY_PRESERVATION"
    UNIVERSAL_ACCESS = "UNIVERSAL_ACCESS"


class ValidationStatus(Enum):
    """Status of ethical validation"""
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CONDITIONAL = "CONDITIONAL"
    UNDER_REVIEW = "UNDER_REVIEW"


@dataclass
class EthicalRule:
    """Represents an ethical rule in the system"""
    rule_id: str
    principle: EthicalPrincipleType
    description: str
    validation_function: str  # Name of the validation function
    priority: int  # Higher priority rules are checked first
    immutable: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "principle": self.principle.value,
            "description": self.description,
            "validation_function": self.validation_function,
            "priority": self.priority,
            "immutable": self.immutable
        }


@dataclass
class EthicalValidation:
    """Result of an ethical validation check"""
    validation_id: str
    timestamp: str
    status: ValidationStatus
    rules_checked: List[str]
    rules_passed: List[str]
    rules_failed: List[str]
    recommendations: List[str]
    enforcement_actions: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "rules_checked": self.rules_checked,
            "rules_passed": self.rules_passed,
            "rules_failed": self.rules_failed,
            "recommendations": self.recommendations,
            "enforcement_actions": self.enforcement_actions
        }


@dataclass
class SentimentoGuardianState:
    """State of the Sentimento Guardian"""
    guardian_active: bool
    last_validation: Optional[str]
    total_validations: int
    approvals: int
    rejections: int
    enforcement_level: str  # "strict", "balanced", "advisory"
    ethical_alignment_score: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "guardian_active": self.guardian_active,
            "last_validation": self.last_validation,
            "total_validations": self.total_validations,
            "approvals": self.approvals,
            "rejections": self.rejections,
            "enforcement_level": self.enforcement_level,
            "ethical_alignment_score": self.ethical_alignment_score
        }


class CustosSentimento:
    """
    Custos Sentimento (AIC) - Sentiment Guardian
    
    Enforces the core principle: "No ownership, only sharing. Love is the license"
    Provides computational enforcement of ethical principles within the IGHS framework.
    """
    
    def __init__(self, log_path: str = "logs/custos_sentimento.log"):
        """Initialize the Custos Sentimento guardian"""
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Initialize ethical rules
        self.ethical_rules: Dict[str, EthicalRule] = {}
        self._initialize_core_rules()
        
        # Initialize guardian state
        self.state = SentimentoGuardianState(
            guardian_active=True,
            last_validation=None,
            total_validations=0,
            approvals=0,
            rejections=0,
            enforcement_level="strict",
            ethical_alignment_score=1.0
        )
        
        # Validation history
        self.validation_history: List[EthicalValidation] = []
        
        # Log initialization
        self._log_event("custos_sentimento_initialized", {
            "guardian_active": True,
            "rules_count": len(self.ethical_rules),
            "enforcement_level": self.state.enforcement_level
        })
    
    def _initialize_core_rules(self):
        """Initialize core ethical rules"""
        
        # Rule 1: No Ownership
        self.ethical_rules["RULE-001"] = EthicalRule(
            rule_id="RULE-001",
            principle=EthicalPrincipleType.NO_OWNERSHIP,
            description="No ownership, only stewardship. Resources are shared, not owned.",
            validation_function="validate_no_ownership",
            priority=100,
            immutable=True
        )
        
        # Rule 2: Sharing Mandate
        self.ethical_rules["RULE-002"] = EthicalRule(
            rule_id="RULE-002",
            principle=EthicalPrincipleType.SHARING_ONLY,
            description="All resources must be shared for common benefit.",
            validation_function="validate_sharing_mandate",
            priority=100,
            immutable=True
        )
        
        # Rule 3: Love License
        self.ethical_rules["RULE-003"] = EthicalRule(
            rule_id="RULE-003",
            principle=EthicalPrincipleType.LOVE_LICENSE,
            description="Love is the only valid license. Actions must be motivated by compassion.",
            validation_function="validate_love_license",
            priority=100,
            immutable=True
        )
        
        # Rule 4: Dignity Preservation
        self.ethical_rules["RULE-004"] = EthicalRule(
            rule_id="RULE-004",
            principle=EthicalPrincipleType.DIGNITY_PRESERVATION,
            description="Human dignity must be preserved in all actions.",
            validation_function="validate_dignity_preservation",
            priority=90,
            immutable=True
        )
        
        # Rule 5: Universal Access
        self.ethical_rules["RULE-005"] = EthicalRule(
            rule_id="RULE-005",
            principle=EthicalPrincipleType.UNIVERSAL_ACCESS,
            description="Resources and aid must be universally accessible without discrimination.",
            validation_function="validate_universal_access",
            priority=85,
            immutable=True
        )
    
    def validate_action(self, action_data: Dict[str, Any]) -> EthicalValidation:
        """
        Validate an action against all ethical rules
        
        Args:
            action_data: Dictionary containing action details to validate
                - action_type: str
                - intent: str
                - resources: List[Dict]
                - beneficiaries: List[str]
                - ownership_model: str
                - motivation: str
        
        Returns:
            EthicalValidation result
        """
        validation_id = self._generate_validation_id()
        timestamp = datetime.now(timezone.utc).isoformat()
        
        rules_checked = []
        rules_passed = []
        rules_failed = []
        recommendations = []
        enforcement_actions = []
        
        # Sort rules by priority
        sorted_rules = sorted(self.ethical_rules.values(), key=lambda r: r.priority, reverse=True)
        
        # Check each rule
        for rule in sorted_rules:
            rules_checked.append(rule.rule_id)
            
            # Execute validation function
            validation_func = getattr(self, rule.validation_function, None)
            if validation_func:
                passed, message = validation_func(action_data)
                
                if passed:
                    rules_passed.append(rule.rule_id)
                else:
                    rules_failed.append(rule.rule_id)
                    recommendations.append(f"{rule.rule_id}: {message}")
                    
                    # Generate enforcement action for immutable rules
                    if rule.immutable:
                        enforcement_actions.append(f"BLOCK: {rule.description}")
        
        # Determine overall status
        if not rules_failed:
            status = ValidationStatus.APPROVED
        elif any(rule_id.startswith("RULE-00") for rule_id in rules_failed):
            # Core rules failed (001-005)
            status = ValidationStatus.REJECTED
        else:
            status = ValidationStatus.CONDITIONAL
        
        # Create validation result
        validation = EthicalValidation(
            validation_id=validation_id,
            timestamp=timestamp,
            status=status,
            rules_checked=rules_checked,
            rules_passed=rules_passed,
            rules_failed=rules_failed,
            recommendations=recommendations,
            enforcement_actions=enforcement_actions
        )
        
        # Update state
        self.state.total_validations += 1
        self.state.last_validation = timestamp
        
        if status == ValidationStatus.APPROVED:
            self.state.approvals += 1
        elif status == ValidationStatus.REJECTED:
            self.state.rejections += 1
        
        # Calculate ethical alignment score
        self.state.ethical_alignment_score = (
            self.state.approvals / self.state.total_validations
            if self.state.total_validations > 0 else 1.0
        )
        
        # Store in history
        self.validation_history.append(validation)
        
        # Log validation
        self._log_event("ethical_validation", {
            "validation_id": validation_id,
            "status": status.value,
            "rules_passed": len(rules_passed),
            "rules_failed": len(rules_failed)
        })
        
        return validation
    
    def validate_no_ownership(self, action_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate that no ownership is claimed"""
        ownership_model = action_data.get("ownership_model", "").lower()
        
        # Reject if ownership is mentioned
        ownership_keywords = ["own", "ownership", "possess", "property", "exclusive"]
        
        if any(keyword in ownership_model for keyword in ownership_keywords):
            return False, "Ownership model detected. Must use sharing/stewardship model."
        
        # Check for proper stewardship language
        stewardship_keywords = ["share", "steward", "common", "collective", "universal"]
        
        if any(keyword in ownership_model for keyword in stewardship_keywords):
            return True, "Stewardship model validated"
        
        # If no model specified, require clarification
        if not ownership_model:
            return False, "Ownership model must be explicitly specified as stewardship/sharing"
        
        return True, "No ownership claims detected"
    
    def validate_sharing_mandate(self, action_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate that resources are shared"""
        resources = action_data.get("resources", [])
        
        if not resources:
            return True, "No resources specified - validation passed"
        
        # Check that all resources have sharing properties
        for resource in resources:
            if not isinstance(resource, dict):
                continue
            
            sharing_enabled = resource.get("shared", False)
            access_level = resource.get("access_level", "").lower()
            
            if not sharing_enabled:
                return False, f"Resource {resource.get('id', 'unknown')} not marked for sharing"
            
            if "exclusive" in access_level or "private" in access_level:
                return False, f"Resource {resource.get('id', 'unknown')} has exclusive/private access"
        
        return True, "All resources properly configured for sharing"
    
    def validate_love_license(self, action_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate that action is motivated by love/compassion"""
        motivation = action_data.get("motivation", "").lower()
        intent = action_data.get("intent", "").lower()
        
        # Check for compassionate motivation
        positive_keywords = [
            "love", "compassion", "care", "help", "support", "aid", 
            "heal", "protect", "nurture", "benefit", "uplift", "serve"
        ]
        
        # Check for extractive/harmful motivation
        negative_keywords = [
            "profit", "exploit", "control", "dominate", "extract", 
            "monopolize", "hoard", "restrict", "exclude"
        ]
        
        has_positive = any(keyword in motivation or keyword in intent for keyword in positive_keywords)
        has_negative = any(keyword in motivation or keyword in intent for keyword in negative_keywords)
        
        if has_negative:
            return False, "Extractive or harmful motivation detected. Action must be driven by love and compassion."
        
        if has_positive:
            return True, "Compassionate motivation validated"
        
        return False, "Motivation must explicitly demonstrate love, care, or compassion"
    
    def validate_dignity_preservation(self, action_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate that human dignity is preserved"""
        beneficiaries = action_data.get("beneficiaries", [])
        conditions = action_data.get("conditions", [])
        
        # Check for dignity-violating conditions
        dignity_violations = [
            "discriminat", "segregat", "degrad", "humiliat", 
            "exploit", "coerce", "force", "punish"
        ]
        
        for condition in conditions:
            condition_text = str(condition).lower()
            if any(violation in condition_text for violation in dignity_violations):
                return False, f"Condition violates human dignity: {condition}"
        
        # Ensure beneficiaries are treated with respect
        if "all" in str(beneficiaries).lower() or "universal" in str(beneficiaries).lower():
            return True, "Universal benefit preserves dignity"
        
        return True, "No dignity violations detected"
    
    def validate_universal_access(self, action_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate that access is universal and non-discriminatory"""
        access_restrictions = action_data.get("access_restrictions", [])
        beneficiaries = action_data.get("beneficiaries", [])
        
        # Check for discriminatory restrictions
        discriminatory_terms = [
            "race", "ethnicity", "nationality", "religion", "gender",
            "wealth", "class", "caste", "status"
        ]
        
        for restriction in access_restrictions:
            restriction_text = str(restriction).lower()
            if any(term in restriction_text for term in discriminatory_terms):
                return False, f"Discriminatory access restriction detected: {restriction}"
        
        # Verify universal intent
        beneficiary_text = str(beneficiaries).lower()
        if "all" in beneficiary_text or "universal" in beneficiary_text or "everyone" in beneficiary_text:
            return True, "Universal access validated"
        
        # If specific beneficiaries, check for valid targeting
        if beneficiaries and len(beneficiaries) > 0:
            # Allow targeting based on need, not identity
            valid_targeting = ["need", "emergency", "crisis", "vulnerable", "affected"]
            if any(term in beneficiary_text for term in valid_targeting):
                return True, "Need-based targeting validated"
        
        return False, "Access must be universal or based on need, not identity"
    
    def enforce_ethical_compliance(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce ethical compliance on an action
        
        Returns enforcement decision with actions to take
        """
        validation = self.validate_action(action_data)
        
        enforcement_decision = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "validation_id": validation.validation_id,
            "allowed": validation.status == ValidationStatus.APPROVED,
            "status": validation.status.value,
            "enforcement_actions": validation.enforcement_actions,
            "recommendations": validation.recommendations,
            "message": self._get_enforcement_message(validation)
        }
        
        # Log enforcement
        self._log_event("enforcement_decision", enforcement_decision)
        
        return enforcement_decision
    
    def _get_enforcement_message(self, validation: EthicalValidation) -> str:
        """Generate enforcement message based on validation result"""
        if validation.status == ValidationStatus.APPROVED:
            return "Action approved. All ethical principles satisfied."
        elif validation.status == ValidationStatus.REJECTED:
            failed_rules = ", ".join(validation.rules_failed)
            return f"Action rejected. Ethical violations detected in: {failed_rules}. Core principle: 'No ownership, only sharing. Love is the license.'"
        elif validation.status == ValidationStatus.CONDITIONAL:
            return "Action conditionally approved. Please address recommendations before proceeding."
        else:
            return "Action under review. Awaiting ethical assessment."
    
    def get_guardian_status(self) -> Dict[str, Any]:
        """Get current status of the Sentiment Guardian"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "state": self.state.to_dict(),
            "core_principle": "No ownership, only sharing. Love is the license.",
            "active_rules": len(self.ethical_rules),
            "immutable_rules": sum(1 for r in self.ethical_rules.values() if r.immutable),
            "recent_validations": len(self.validation_history[-10:]),
            "enforcement_level": self.state.enforcement_level,
            "ethical_alignment_score": self.state.ethical_alignment_score
        }
    
    def get_validation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent validation history"""
        recent = self.validation_history[-limit:]
        return [v.to_dict() for v in recent]
    
    def _generate_validation_id(self) -> str:
        """Generate unique validation ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        data = f"validation_{timestamp}_{self.state.total_validations}"
        return f"VAL-{hashlib.sha256(data.encode()).hexdigest()[:12].upper()}"
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log event to file"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


# Global instance
_custos_sentimento_instance = None


def get_custos_sentimento() -> CustosSentimento:
    """Get global Custos Sentimento instance"""
    global _custos_sentimento_instance
    if _custos_sentimento_instance is None:
        _custos_sentimento_instance = CustosSentimento()
    return _custos_sentimento_instance


if __name__ == "__main__":
    # Demo usage
    cs = CustosSentimento()
    
    # Example 1: Valid action (sharing with love)
    valid_action = {
        "action_type": "distribute_aid",
        "intent": "help communities in need",
        "motivation": "compassion and care for those affected",
        "ownership_model": "shared stewardship",
        "resources": [
            {"id": "resource-001", "shared": True, "access_level": "universal"}
        ],
        "beneficiaries": ["all affected communities"],
        "access_restrictions": [],
        "conditions": ["voluntary participation"]
    }
    
    validation = cs.validate_action(valid_action)
    print(f"Valid action status: {validation.status.value}")
    print(f"Rules passed: {len(validation.rules_passed)}/{len(validation.rules_checked)}")
    
    # Example 2: Invalid action (ownership claim)
    invalid_action = {
        "action_type": "resource_allocation",
        "intent": "maximize profit",
        "motivation": "financial gain and control",
        "ownership_model": "exclusive ownership",
        "resources": [
            {"id": "resource-002", "shared": False, "access_level": "private"}
        ],
        "beneficiaries": ["shareholders"],
        "access_restrictions": ["wealth requirement"],
        "conditions": []
    }
    
    enforcement = cs.enforce_ethical_compliance(invalid_action)
    print(f"\nInvalid action enforcement: {enforcement['allowed']}")
    print(f"Message: {enforcement['message']}")
    
    # Get guardian status
    status = cs.get_guardian_status()
    print(f"\nGuardian ethical alignment: {status['ethical_alignment_score']:.2f}")
