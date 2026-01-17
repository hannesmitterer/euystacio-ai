# Core module for Euystacio AI
"""
Euystacio AI Core Module

This module contains the core components for:
- Real-Time Threshold Monitoring (QEK, H-VAR, Ethisches Ideal)
- Governance Signature Compliance Automation
- IPFS Cross-Sync and Integrity Layer
- Coronation Workshop Simulation
- Quantum-Shield Protection (NTRU lattice-based encryption)
- BBMN - Blockchain-Based Mesh Network (DNS-free)
- TensorFlow Predictive Kernel (Anomaly Detection)
- Stealth Mode (Ponte Amoris & Resonance School Protection)

Prepared for Coronation Day (January 2026) and testing phases.
"""

from core.red_code import RedCodeSystem, red_code_system
from core.reflector import reflect_and_suggest

# Import operational components
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

# Import EUYSTACIO network protection components
from core.quantum_shield import (
    QuantumShield,
    QuantumKey,
    get_quantum_shield
)
from core.bbmn_network import (
    BBMNNetwork,
    MeshNode,
    NodeRole,
    NodeStatus,
    get_bbmn_network
)
from core.tf_kernel_monitor import (
    TFKernelMonitor,
    Anomaly,
    ThreatLevel,
    AnomalyType,
    get_tf_kernel_monitor
)
from core.stealth_mode import (
    StealthMode,
    StealthLevel,
    AlignmentStatus,
    get_stealth_mode
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
    # Quantum Shield Protection
    'QuantumShield',
    'QuantumKey',
    'get_quantum_shield',
    # BBMN Network
    'BBMNNetwork',
    'MeshNode',
    'NodeRole',
    'NodeStatus',
    'get_bbmn_network',
    # TensorFlow Kernel
    'TFKernelMonitor',
    'Anomaly',
    'ThreatLevel',
    'AnomalyType',
    'get_tf_kernel_monitor',
    # Stealth Mode
    'StealthMode',
    'StealthLevel',
    'AlignmentStatus',
    'get_stealth_mode',
]