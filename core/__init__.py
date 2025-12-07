# Core module for Euystacio AI
"""
Euystacio AI Core Module

This module contains the core components for:
- Real-Time Threshold Monitoring (QEK, H-VAR, Ethisches Ideal)
- Governance Signature Compliance Automation
- IPFS Cross-Sync and Integrity Layer
- Coronation Workshop Simulation
- IGHS (Incorruptible Global Health System) Components:
  - Custos Sentimento (AIC) - Ethical AI Governance
  - Ethics Gap Calculator - H-VAR and Ethics Gap measurement
  - Quantum Solutions - AI decision optimization
  - Peacobonds - Immutable aid distribution
  - AETERNA GOVERNATIA - Eternal guardianship framework

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

# Import IGHS components
from core.custos_sentimento import (
    CustosSentimento,
    EthicalPrincipleType,
    ValidationStatus,
    get_custos_sentimento
)
from core.ethics_gap_calculator import (
    EthicsGapCalculator,
    EthicsGapSeverity,
    VolatilityLevel,
    get_ethics_gap_calculator
)
from core.quantum_solutions import (
    QuantumSolutions,
    ImpactLevel,
    DecisionSpeed,
    InterventionType,
    get_quantum_solutions
)
from core.peacobonds import (
    PeacobandsSystem,
    PeacobondStatus,
    ResourceType,
    SecurityLevel,
    get_peacobonds_system
)
from core.aeterna_governatia import (
    AeternaGovernati,
    GovernanceAction,
    TransparencyLevel,
    CorruptionRisk,
    get_aeterna_governatia
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
    # IGHS - Custos Sentimento
    'CustosSentimento',
    'EthicalPrincipleType',
    'ValidationStatus',
    'get_custos_sentimento',
    # IGHS - Ethics Gap Calculator
    'EthicsGapCalculator',
    'EthicsGapSeverity',
    'VolatilityLevel',
    'get_ethics_gap_calculator',
    # IGHS - Quantum Solutions
    'QuantumSolutions',
    'ImpactLevel',
    'DecisionSpeed',
    'InterventionType',
    'get_quantum_solutions',
    # IGHS - Peacobonds
    'PeacobandsSystem',
    'PeacobondStatus',
    'ResourceType',
    'SecurityLevel',
    'get_peacobonds_system',
    # IGHS - AETERNA GOVERNATIA
    'AeternaGovernati',
    'GovernanceAction',
    'TransparencyLevel',
    'CorruptionRisk',
    'get_aeterna_governatia',
]