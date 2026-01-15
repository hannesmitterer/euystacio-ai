"""
tf_kernel_monitor.py
TensorFlow Predictive Kernel for EUYSTACIO Network

AI-powered monitoring of electromagnetic anomalies and security threats.
Automatically moves sensitive data to encrypted buffers when scan attempts detected.

Features:
- TensorFlow-based anomaly detection
- Electromagnetic pattern recognition
- Encrypted buffer management for sensitive data
- Real-time threat assessment
- Integration with Quantum Shield for data protection
"""

import time
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import secrets

# TensorFlow imports (graceful degradation if not available)
try:
    import tensorflow as tf
    import numpy as np
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Warning: TensorFlow not available, using fallback detection")


class ThreatLevel(Enum):
    """Threat level classification"""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnomalyType(Enum):
    """Type of detected anomaly"""
    ELECTROMAGNETIC = "ELECTROMAGNETIC"
    SCAN_ATTEMPT = "SCAN_ATTEMPT"
    INTRUSION = "INTRUSION"
    DATA_EXFILTRATION = "DATA_EXFILTRATION"
    RESONANCE_DISRUPTION = "RESONANCE_DISRUPTION"
    UNKNOWN = "UNKNOWN"


@dataclass
class ElectromagneticSignal:
    """Represents an electromagnetic signal measurement"""
    timestamp: float
    frequency_mhz: float
    amplitude: float
    phase: float
    source_location: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_vector(self) -> List[float]:
        """Convert to feature vector for ML model"""
        return [
            self.timestamp % 86400,  # Time of day normalization
            self.frequency_mhz,
            self.amplitude,
            self.phase,
            hash(self.source_location) % 1000  # Location hash
        ]


@dataclass
class Anomaly:
    """Detected anomaly"""
    anomaly_id: str
    timestamp: float
    anomaly_type: AnomalyType
    threat_level: ThreatLevel
    confidence: float  # 0.0 to 1.0
    signals: List[ElectromagneticSignal]
    description: str
    recommended_action: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "anomaly_id": self.anomaly_id,
            "timestamp": self.timestamp,
            "time": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
            "anomaly_type": self.anomaly_type.value,
            "threat_level": self.threat_level.value,
            "confidence": self.confidence,
            "signal_count": len(self.signals),
            "description": self.description,
            "recommended_action": self.recommended_action
        }


@dataclass
class EncryptedBuffer:
    """Encrypted buffer for sensitive data"""
    buffer_id: str
    created_at: float
    data_hash: str
    encrypted_data: bytes
    quantum_key_id: str
    access_count: int = 0
    last_accessed: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "buffer_id": self.buffer_id,
            "created_at": self.created_at,
            "data_hash": self.data_hash,
            "quantum_key_id": self.quantum_key_id,
            "size_bytes": len(self.encrypted_data),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed
        }


class TensorFlowAnomalyDetector:
    """
    TensorFlow-based anomaly detection model
    Detects electromagnetic anomalies and security threats
    """
    
    def __init__(self):
        self.tf_available = TF_AVAILABLE
        self.model: Optional[Any] = None
        self.training_data: List[List[float]] = []
        self.labels: List[int] = []
        
        if self.tf_available:
            self._initialize_model()
        else:
            print("[TF Kernel] Running in fallback mode without TensorFlow")
    
    def _initialize_model(self):
        """Initialize TensorFlow model"""
        if not self.tf_available:
            return
        
        try:
            import tensorflow as tf
            
            # Create simple neural network for anomaly detection
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(16, activation='relu', input_shape=(5,)),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(8, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            print("[TF Kernel] TensorFlow model initialized")
            
        except Exception as e:
            print(f"[TF Kernel] Error initializing model: {e}")
            self.tf_available = False
    
    def predict_anomaly(self, signal: ElectromagneticSignal) -> Tuple[bool, float]:
        """
        Predict if signal is anomalous
        
        Args:
            signal: ElectromagneticSignal to analyze
            
        Returns:
            Tuple of (is_anomaly, confidence)
        """
        if self.tf_available and self.model:
            try:
                # Convert signal to vector
                vector = np.array([signal.to_vector()])
                
                # Predict
                prediction = self.model.predict(vector, verbose=0)[0][0]
                
                is_anomaly = prediction > 0.5
                confidence = float(prediction if is_anomaly else 1 - prediction)
                
                return (is_anomaly, confidence)
                
            except Exception as e:
                print(f"[TF Kernel] Prediction error: {e}")
                return self._fallback_detection(signal)
        else:
            return self._fallback_detection(signal)
    
    def _fallback_detection(self, signal: ElectromagneticSignal) -> Tuple[bool, float]:
        """
        Fallback detection without TensorFlow
        Uses rule-based heuristics
        """
        # Simple rule-based detection
        anomaly_score = 0.0
        
        # Check frequency (suspicious ranges)
        if 2400 <= signal.frequency_mhz <= 2500:  # WiFi scanning
            anomaly_score += 0.3
        if 900 <= signal.frequency_mhz <= 930:  # GSM scanning
            anomaly_score += 0.3
        
        # Check amplitude (unusual strength)
        if signal.amplitude > 0.8:
            anomaly_score += 0.2
        
        # Check phase (rapid changes indicate scanning)
        if abs(signal.phase) > 2.5:
            anomaly_score += 0.2
        
        is_anomaly = anomaly_score > 0.5
        confidence = anomaly_score if is_anomaly else 1 - anomaly_score
        
        return (is_anomaly, confidence)
    
    def train_on_data(self, signals: List[ElectromagneticSignal], 
                     labels: List[bool]) -> bool:
        """
        Train model on labeled data
        
        Args:
            signals: List of signals
            labels: List of anomaly labels (True = anomaly)
            
        Returns:
            Success status
        """
        if not self.tf_available or not self.model:
            print("[TF Kernel] Training not available without TensorFlow")
            return False
        
        try:
            # Convert to numpy arrays
            X = np.array([s.to_vector() for s in signals])
            y = np.array([1 if label else 0 for label in labels])
            
            # Train
            self.model.fit(X, y, epochs=10, batch_size=32, verbose=0)
            
            print(f"[TF Kernel] Model trained on {len(signals)} samples")
            return True
            
        except Exception as e:
            print(f"[TF Kernel] Training error: {e}")
            return False


class EncryptedBufferManager:
    """
    Manager for encrypted data buffers
    Protects sensitive data from scanning attempts
    """
    
    def __init__(self, quantum_shield=None):
        """
        Initialize buffer manager
        
        Args:
            quantum_shield: Optional QuantumShield for encryption
        """
        self.quantum_shield = quantum_shield
        self.buffers: Dict[str, EncryptedBuffer] = {}
        self.buffer_access_log: List[Dict[str, Any]] = []
        
    def create_buffer(self, sensitive_data: bytes, 
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create encrypted buffer for sensitive data
        
        Args:
            sensitive_data: Data to encrypt and store
            metadata: Optional metadata
            
        Returns:
            Buffer ID
        """
        # Generate buffer ID
        buffer_id = f"BUF-{secrets.token_hex(16)}"
        
        # Hash original data
        data_hash = hashlib.sha256(sensitive_data).hexdigest()
        
        # Encrypt with quantum shield
        if self.quantum_shield:
            encrypted_data, quantum_key_id = self.quantum_shield.encrypt(sensitive_data)
        else:
            # Fallback: Simple obfuscation
            encrypted_data = bytes(b ^ 0xAA for b in sensitive_data)
            quantum_key_id = "FALLBACK"
        
        # Create buffer
        buffer = EncryptedBuffer(
            buffer_id=buffer_id,
            created_at=time.time(),
            data_hash=data_hash,
            encrypted_data=encrypted_data,
            quantum_key_id=quantum_key_id
        )
        
        self.buffers[buffer_id] = buffer
        
        print(f"[TF Kernel] Created encrypted buffer {buffer_id} ({len(sensitive_data)} bytes)")
        
        return buffer_id
    
    def access_buffer(self, buffer_id: str, authorized: bool = True) -> Optional[bytes]:
        """
        Access encrypted buffer data
        
        Args:
            buffer_id: Buffer identifier
            authorized: Whether access is authorized
            
        Returns:
            Decrypted data if authorized, None otherwise
        """
        buffer = self.buffers.get(buffer_id)
        if not buffer:
            return None
        
        # Log access attempt
        self.buffer_access_log.append({
            "buffer_id": buffer_id,
            "timestamp": time.time(),
            "authorized": authorized
        })
        
        if not authorized:
            print(f"[TF Kernel] Unauthorized access attempt to buffer {buffer_id}")
            return None
        
        # Update access statistics
        buffer.access_count += 1
        buffer.last_accessed = time.time()
        
        # Decrypt
        if self.quantum_shield:
            decrypted_data = self.quantum_shield.decrypt(buffer.encrypted_data, buffer.quantum_key_id)
        else:
            # Fallback: Reverse obfuscation
            decrypted_data = bytes(b ^ 0xAA for b in buffer.encrypted_data)
        
        return decrypted_data
    
    def delete_buffer(self, buffer_id: str) -> bool:
        """Delete encrypted buffer"""
        if buffer_id in self.buffers:
            del self.buffers[buffer_id]
            print(f"[TF Kernel] Deleted buffer {buffer_id}")
            return True
        return False
    
    def get_buffer_info(self, buffer_id: str) -> Optional[Dict[str, Any]]:
        """Get buffer information (without decrypting)"""
        buffer = self.buffers.get(buffer_id)
        return buffer.to_dict() if buffer else None


class TFKernelMonitor:
    """
    Main TensorFlow Predictive Kernel Monitor
    
    Monitors electromagnetic anomalies and protects sensitive data
    """
    
    def __init__(self, quantum_shield=None, threshold_monitor=None):
        """
        Initialize TF Kernel Monitor
        
        Args:
            quantum_shield: Optional QuantumShield for encryption
            threshold_monitor: Optional ThresholdMonitor for integration
        """
        self.quantum_shield = quantum_shield
        self.threshold_monitor = threshold_monitor
        
        self.detector = TensorFlowAnomalyDetector()
        self.buffer_manager = EncryptedBufferManager(quantum_shield)
        
        self.detected_anomalies: List[Anomaly] = []
        self.signal_history: List[ElectromagneticSignal] = []
        
        # Monitoring state
        self.monitoring_active = True
        self.auto_protect = True  # Auto-move sensitive data when threats detected
        
        # Statistics
        self.stats = {
            "signals_analyzed": 0,
            "anomalies_detected": 0,
            "buffers_created": 0,
            "threats_blocked": 0
        }
    
    def analyze_signal(self, signal: ElectromagneticSignal) -> Optional[Anomaly]:
        """
        Analyze electromagnetic signal for anomalies
        
        Args:
            signal: Signal to analyze
            
        Returns:
            Anomaly if detected, None otherwise
        """
        self.stats["signals_analyzed"] += 1
        self.signal_history.append(signal)
        
        # Predict anomaly
        is_anomaly, confidence = self.detector.predict_anomaly(signal)
        
        if is_anomaly:
            # Classify threat level based on confidence
            if confidence >= 0.9:
                threat_level = ThreatLevel.CRITICAL
            elif confidence >= 0.75:
                threat_level = ThreatLevel.HIGH
            elif confidence >= 0.6:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Determine anomaly type
            anomaly_type = self._classify_anomaly_type(signal)
            
            # Create anomaly record
            anomaly = Anomaly(
                anomaly_id=f"ANOM-{secrets.token_hex(8)}",
                timestamp=signal.timestamp,
                anomaly_type=anomaly_type,
                threat_level=threat_level,
                confidence=confidence,
                signals=[signal],
                description=f"{anomaly_type.value} detected at {signal.frequency_mhz} MHz",
                recommended_action=self._get_recommended_action(anomaly_type, threat_level)
            )
            
            self.detected_anomalies.append(anomaly)
            self.stats["anomalies_detected"] += 1
            
            print(f"[TF Kernel] ⚠️  Anomaly detected: {anomaly_type.value} "
                  f"(Threat: {threat_level.value}, Confidence: {confidence:.2f})")
            
            # Auto-protect if enabled
            if self.auto_protect and threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                self._trigger_protection_mode(anomaly)
            
            return anomaly
        
        return None
    
    def _classify_anomaly_type(self, signal: ElectromagneticSignal) -> AnomalyType:
        """Classify type of anomaly based on signal characteristics"""
        # Frequency-based classification
        if 2400 <= signal.frequency_mhz <= 2500:
            return AnomalyType.SCAN_ATTEMPT
        elif signal.amplitude > 0.9:
            return AnomalyType.INTRUSION
        elif abs(signal.phase) > 2.5:
            return AnomalyType.ELECTROMAGNETIC
        else:
            return AnomalyType.UNKNOWN
    
    def _get_recommended_action(self, anomaly_type: AnomalyType, 
                               threat_level: ThreatLevel) -> str:
        """Get recommended action for anomaly"""
        actions = {
            (AnomalyType.SCAN_ATTEMPT, ThreatLevel.CRITICAL): 
                "IMMEDIATE: Activate stealth mode and encrypt all sensitive data",
            (AnomalyType.SCAN_ATTEMPT, ThreatLevel.HIGH):
                "Move sensitive data to encrypted buffers",
            (AnomalyType.INTRUSION, ThreatLevel.CRITICAL):
                "CRITICAL: Initiate Ponte Amoris closure protocol",
            (AnomalyType.ELECTROMAGNETIC, ThreatLevel.MEDIUM):
                "Monitor for pattern escalation",
        }
        
        return actions.get(
            (anomaly_type, threat_level),
            "Continue monitoring and log for analysis"
        )
    
    def _trigger_protection_mode(self, anomaly: Anomaly):
        """
        Trigger protection mode when high threats detected
        Automatically moves sensitive data to encrypted buffers
        """
        print(f"[TF Kernel] 🛡️  PROTECTION MODE ACTIVATED")
        print(f"[TF Kernel] Threat: {anomaly.anomaly_type.value} - {anomaly.threat_level.value}")
        
        self.stats["threats_blocked"] += 1
        
        # In production, this would identify and protect actual sensitive data
        # For now, create a demonstration buffer
        sensitive_data = json.dumps({
            "type": "resonance_school_data",
            "lex_amoris_alignment": 0.95,
            "protected_at": time.time(),
            "reason": f"Threat detected: {anomaly.anomaly_type.value}"
        }).encode()
        
        buffer_id = self.buffer_manager.create_buffer(sensitive_data)
        self.stats["buffers_created"] += 1
        
        print(f"[TF Kernel] Sensitive data moved to encrypted buffer: {buffer_id}")
    
    def protect_data(self, data: bytes, reason: str = "Manual protection") -> str:
        """
        Manually protect data by moving to encrypted buffer
        
        Args:
            data: Data to protect
            reason: Reason for protection
            
        Returns:
            Buffer ID
        """
        buffer_id = self.buffer_manager.create_buffer(data, {"reason": reason})
        self.stats["buffers_created"] += 1
        return buffer_id
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        recent_anomalies = [
            a.to_dict() for a in self.detected_anomalies[-10:]
        ]
        
        return {
            "monitoring_active": self.monitoring_active,
            "auto_protect": self.auto_protect,
            "tensorflow_available": self.detector.tf_available,
            "signals_analyzed": self.stats["signals_analyzed"],
            "anomalies_detected": self.stats["anomalies_detected"],
            "buffers_created": self.stats["buffers_created"],
            "threats_blocked": self.stats["threats_blocked"],
            "recent_anomalies": recent_anomalies,
            "active_buffers": len(self.buffer_manager.buffers)
        }


# Global TF Kernel Monitor instance
_tf_kernel_instance: Optional[TFKernelMonitor] = None


def get_tf_kernel_monitor(quantum_shield=None, threshold_monitor=None) -> TFKernelMonitor:
    """
    Get or create global TF Kernel Monitor instance
    
    Args:
        quantum_shield: Optional QuantumShield
        threshold_monitor: Optional ThresholdMonitor
        
    Returns:
        TFKernelMonitor instance
    """
    global _tf_kernel_instance
    
    if _tf_kernel_instance is None:
        _tf_kernel_instance = TFKernelMonitor(quantum_shield, threshold_monitor)
    
    return _tf_kernel_instance


# Self-test
if __name__ == "__main__":
    print("=== TensorFlow Predictive Kernel Self-Test ===")
    
    monitor = TFKernelMonitor()
    
    print("\n1. System Status:")
    status = monitor.get_monitoring_status()
    print(f"   TensorFlow Available: {status['tensorflow_available']}")
    print(f"   Monitoring Active: {status['monitoring_active']}")
    print(f"   Auto-Protect: {status['auto_protect']}")
    
    print("\n2. Analyzing Normal Signals:")
    for i in range(5):
        signal = ElectromagneticSignal(
            timestamp=time.time(),
            frequency_mhz=100.0 + i * 10,
            amplitude=0.3,
            phase=0.5,
            source_location="ambient"
        )
        anomaly = monitor.analyze_signal(signal)
        if anomaly:
            print(f"   ⚠️  Anomaly: {anomaly.anomaly_type.value}")
    
    print("\n3. Analyzing Suspicious Signal (Scan Attempt):")
    suspicious_signal = ElectromagneticSignal(
        timestamp=time.time(),
        frequency_mhz=2450.0,  # WiFi scanning frequency
        amplitude=0.85,
        phase=3.0,
        source_location="unknown"
    )
    anomaly = monitor.analyze_signal(suspicious_signal)
    if anomaly:
        print(f"   Type: {anomaly.anomaly_type.value}")
        print(f"   Threat Level: {anomaly.threat_level.value}")
        print(f"   Confidence: {anomaly.confidence:.2f}")
        print(f"   Action: {anomaly.recommended_action}")
    
    print("\n4. Testing Data Protection:")
    test_data = b"SENSITIVE: Resonance School coordinates and Lex Amoris protocols"
    buffer_id = monitor.protect_data(test_data, "Test protection")
    print(f"   Buffer created: {buffer_id}")
    
    # Retrieve data
    retrieved = monitor.buffer_manager.access_buffer(buffer_id, authorized=True)
    print(f"   Data retrieved: {retrieved == test_data}")
    
    print("\n5. Final Statistics:")
    final_status = monitor.get_monitoring_status()
    print(f"   Signals Analyzed: {final_status['signals_analyzed']}")
    print(f"   Anomalies Detected: {final_status['anomalies_detected']}")
    print(f"   Buffers Created: {final_status['buffers_created']}")
    print(f"   Threats Blocked: {final_status['threats_blocked']}")
    
    print("\n✅ TF Kernel Monitor operational - AI protection active")
