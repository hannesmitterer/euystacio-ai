# Core module for Euystacio AI
"""
Euystacio AI Core Module

This module contains the core components for:
- Real-Time Threshold Monitoring (QEK, H-VAR, Ethisches Ideal)
- Governance Signature Compliance Automation
- IPFS Cross-Sync and Integrity Layer
- Coronation Workshop Simulation
- Protocollo Meta Salvage (Ethical Preservation)

Prepared for Coronation Day (January 2026) and testing phases.
"""

from core.red_code import RedCodeSystem, red_code_system
from core.reflector import reflect_and_suggest

# Import new operational components
from core.threshold_monitor import (
    ThresholdMonitor,
    MetricType,
    AlertLevel,
    get_threshold_monitor
)
from core.governance_compliance import (
    GovernanceComplianceManager,
    SignatureStatus,
    QuorumStatus,
    get_governance_manager
)
from core.ipfs_integrity import (
    IPFSIntegrityManager,
    SyncStatus,
    IntegrityStatus,
    get_ipfs_manager
)
from core.coronation_simulator import (
    CoronationSimulator,
    SimulationMode,
    LoadLevel,
    get_coronation_simulator
)

# Import Protocollo Meta Salvage components
from core.risk_monitor import (
    RiskMonitor,
    RiskLevel,
    RiskType,
    get_risk_monitor
)
from core.peace_bonds import (
    PeaceBondsManager,
    BondStatus,
    ConstraintType,
    get_peace_bonds_manager
)
from core.decision_engine import (
    DecisionEngine,
    DecisionType,
    get_decision_engine
)
from core.audit_pipeline import (
    AuditPipeline,
    AuditStatus,
    ComplianceLevel,
    get_audit_pipeline
)
from core.meta_salvage_protocol import (
    MetaSalvageProtocol,
    ProtocolStatus,
    get_meta_salvage_protocol
)

__all__ = [
    # Existing components
    'RedCodeSystem',
    'red_code_system',
    'reflect_and_suggest',
    # Threshold Monitoring
    'ThresholdMonitor',
    'MetricType',
    'AlertLevel',
    'get_threshold_monitor',
    # Governance Compliance
    'GovernanceComplianceManager',
    'SignatureStatus',
    'QuorumStatus',
    'get_governance_manager',
    # IPFS Integrity
    'IPFSIntegrityManager',
    'SyncStatus',
    'IntegrityStatus',
    'get_ipfs_manager',
    # Coronation Simulator
    'CoronationSimulator',
    'SimulationMode',
    'LoadLevel',
    'get_coronation_simulator',
    # Protocollo Meta Salvage
    'RiskMonitor',
    'RiskLevel',
    'RiskType',
    'get_risk_monitor',
    'PeaceBondsManager',
    'BondStatus',
    'ConstraintType',
    'get_peace_bonds_manager',
    'DecisionEngine',
    'DecisionType',
    'get_decision_engine',
    'AuditPipeline',
    'AuditStatus',
    'ComplianceLevel',
    'get_audit_pipeline',
    'MetaSalvageProtocol',
    'ProtocolStatus',
    'get_meta_salvage_protocol',
]