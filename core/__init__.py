# Core module for Euystacio AI
"""
Euystacio AI Core Module

This module contains the core components for:
- Real-Time Threshold Monitoring (QEK, H-VAR, Ethisches Ideal)
- Governance Signature Compliance Automation
- IPFS Cross-Sync and Integrity Layer
- Coronation Workshop Simulation

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
]