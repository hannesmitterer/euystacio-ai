"""
lex_amoris_security.py
Lex Amoris Security Framework for Euystacio AI

Implements:
1. Dynamic Blacklist with Rhythm Validation
2. Lazy Security with energy-based protection
3. Behavioral pattern analysis
4. Integration with Sentimento Pulse and Red Code systems

Based on Lex Amoris principles: security through harmony, not force.
"""

import hashlib
import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time


class RhythmStatus(Enum):
    """Status of rhythm validation"""
    VALID = "VALID"
    INVALID = "INVALID"
    SUSPICIOUS = "SUSPICIOUS"
    BLOCKED = "BLOCKED"


class ThreatLevel(Enum):
    """Threat level classification"""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ProtectionMode(Enum):
    """Protection mode states"""
    DORMANT = "DORMANT"      # Lazy mode - minimal protection
    ACTIVE = "ACTIVE"        # Normal protection
    VIGILANT = "VIGILANT"    # High alert
    EMERGENCY = "EMERGENCY"  # Maximum protection


@dataclass
class DataPacket:
    """Represents a data packet for validation"""
    packet_id: str
    source_ip: str
    timestamp: str
    data: bytes
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_rhythm_signature(self) -> str:
        """Calculate rhythm signature based on packet characteristics"""
        # Rhythm is determined by:
        # - Timing pattern (timestamp variance)
        # - Data entropy
        # - Size consistency
        # - Metadata harmony
        
        rhythm_data = {
            "timestamp": self.timestamp,
            "size": len(self.data),
            "entropy": self._calculate_entropy(),
            "metadata_keys": sorted(self.metadata.keys())
        }
        
        rhythm_string = json.dumps(rhythm_data, sort_keys=True)
        return hashlib.sha256(rhythm_string.encode()).hexdigest()
    
    def _calculate_entropy(self) -> float:
        """Calculate Shannon entropy of packet data"""
        if not self.data:
            return 0.0
        
        # Calculate byte frequency
        freq = {}
        for byte in self.data:
            freq[byte] = freq.get(byte, 0) + 1
        
        # Calculate entropy
        import math
        entropy = 0.0
        data_len = len(self.data)
        for count in freq.values():
            p = count / data_len
            entropy -= p * math.log2(p)
        
        return entropy


@dataclass
class RhythmPattern:
    """Pattern of rhythmic behavior"""
    pattern_id: str
    frequency: float  # Expected frequency in Hz (packets/second)
    variance_threshold: float  # Allowed variance
    last_seen: str
    packet_count: int
    is_trusted: bool


@dataclass
class BlacklistEntry:
    """Entry in the dynamic blacklist"""
    source_ip: str
    reason: str
    threat_level: ThreatLevel
    blocked_at: str
    expires_at: Optional[str]
    violation_count: int
    behavioral_signature: str


class RhythmValidator:
    """
    Validates data packets based on rhythm and frequency
    
    Every packet must vibrate at the correct frequency,
    regardless of IP origin (Lex Amoris principle).
    """
    
    def __init__(self):
        self.known_patterns: Dict[str, RhythmPattern] = {}
        self.rhythm_history: List[Tuple[str, float]] = []
        self.base_frequency = 1.0  # 1 Hz baseline
        self.harmony_threshold = 0.15  # 15% variance allowed
    
    def validate_packet_rhythm(self, packet: DataPacket) -> Tuple[RhythmStatus, float]:
        """
        Validate if packet vibrates at correct frequency
        
        Returns:
            Tuple of (status, harmony_score)
        """
        rhythm_sig = packet.calculate_rhythm_signature()
        current_time = time.time()
        
        # Calculate rhythm score based on temporal consistency
        if self.rhythm_history:
            recent_history = [
                (sig, t) for sig, t in self.rhythm_history 
                if current_time - t < 60  # Last minute
            ]
            
            if recent_history:
                # Check frequency consistency
                time_diffs = []
                for i in range(1, len(recent_history)):
                    time_diffs.append(recent_history[i][1] - recent_history[i-1][1])
                
                if time_diffs:
                    avg_interval = sum(time_diffs) / len(time_diffs)
                    actual_frequency = 1.0 / avg_interval if avg_interval > 0 else 0
                    
                    # Check if frequency is within harmony threshold
                    freq_variance = abs(actual_frequency - self.base_frequency) / self.base_frequency
                    
                    harmony_score = 1.0 - min(freq_variance / self.harmony_threshold, 1.0)
                    
                    if freq_variance > self.harmony_threshold:
                        status = RhythmStatus.SUSPICIOUS
                    else:
                        status = RhythmStatus.VALID
                    
                    # Record this rhythm
                    self.rhythm_history.append((rhythm_sig, current_time))
                    
                    # Limit history size
                    if len(self.rhythm_history) > 1000:
                        self.rhythm_history = self.rhythm_history[-500:]
                    
                    return status, harmony_score
        
        # First packet or not enough history
        self.rhythm_history.append((rhythm_sig, current_time))
        return RhythmStatus.VALID, 1.0
    
    def register_trusted_pattern(self, pattern: RhythmPattern):
        """Register a trusted rhythm pattern"""
        self.known_patterns[pattern.pattern_id] = pattern
    
    def get_rhythm_report(self) -> Dict[str, Any]:
        """Get current rhythm validation report"""
        current_time = time.time()
        recent_rhythms = [
            (sig, t) for sig, t in self.rhythm_history 
            if current_time - t < 300  # Last 5 minutes
        ]
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_patterns": len(self.known_patterns),
            "recent_packets": len(recent_rhythms),
            "base_frequency_hz": self.base_frequency,
            "harmony_threshold": self.harmony_threshold,
            "trusted_patterns": len([p for p in self.known_patterns.values() if p.is_trusted])
        }


class DynamicBlacklist:
    """
    Dynamic blacklist based on behavioral patterns
    
    Blocks sources that consistently violate rhythm validation,
    not just based on IP address (Lex Amoris: judge by behavior, not identity).
    """
    
    def __init__(self, log_path: str = "logs/lex_amoris_blacklist.log"):
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self.violation_history: Dict[str, List[str]] = {}
        self.log_path = log_path
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def record_violation(self, source_ip: str, reason: str, 
                        threat_level: ThreatLevel = ThreatLevel.LOW):
        """Record a violation for behavioral analysis"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        if source_ip not in self.violation_history:
            self.violation_history[source_ip] = []
        
        self.violation_history[source_ip].append(timestamp)
        
        # Check if should be blacklisted
        recent_violations = self._count_recent_violations(source_ip, minutes=10)
        
        if recent_violations >= 5:  # 5 violations in 10 minutes
            self.add_to_blacklist(source_ip, reason, ThreatLevel.HIGH, duration_hours=24)
        elif recent_violations >= 3:
            self.add_to_blacklist(source_ip, reason, ThreatLevel.MEDIUM, duration_hours=1)
        
        self._log_event("VIOLATION_RECORDED", f"IP: {source_ip}, Reason: {reason}, Level: {threat_level.value}")
    
    def _count_recent_violations(self, source_ip: str, minutes: int) -> int:
        """Count violations in recent time window"""
        if source_ip not in self.violation_history:
            return 0
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        cutoff_str = cutoff_time.isoformat()
        
        recent = [v for v in self.violation_history[source_ip] if v > cutoff_str]
        return len(recent)
    
    def add_to_blacklist(self, source_ip: str, reason: str, 
                        threat_level: ThreatLevel,
                        duration_hours: Optional[int] = None):
        """Add source to blacklist"""
        timestamp = datetime.now(timezone.utc)
        
        # Calculate behavioral signature
        violation_count = len(self.violation_history.get(source_ip, []))
        behavioral_sig = hashlib.sha256(
            f"{source_ip}-{violation_count}-{reason}".encode()
        ).hexdigest()[:16]
        
        expires_at = None
        if duration_hours:
            expires_at = (timestamp + timedelta(hours=duration_hours)).isoformat()
        
        entry = BlacklistEntry(
            source_ip=source_ip,
            reason=reason,
            threat_level=threat_level,
            blocked_at=timestamp.isoformat(),
            expires_at=expires_at,
            violation_count=violation_count,
            behavioral_signature=behavioral_sig
        )
        
        self.blacklist[source_ip] = entry
        self._log_event("BLACKLIST_ADD", 
                       f"IP: {source_ip}, Threat: {threat_level.value}, Duration: {duration_hours}h")
    
    def is_blacklisted(self, source_ip: str) -> Tuple[bool, Optional[BlacklistEntry]]:
        """Check if source is blacklisted"""
        if source_ip not in self.blacklist:
            return False, None
        
        entry = self.blacklist[source_ip]
        
        # Check if expired
        if entry.expires_at:
            if datetime.now(timezone.utc).isoformat() > entry.expires_at:
                # Remove expired entry
                del self.blacklist[source_ip]
                self._log_event("BLACKLIST_EXPIRED", f"IP: {source_ip}")
                return False, None
        
        return True, entry
    
    def remove_from_blacklist(self, source_ip: str, reason: str = "Manual removal"):
        """Remove source from blacklist"""
        if source_ip in self.blacklist:
            del self.blacklist[source_ip]
            self._log_event("BLACKLIST_REMOVE", f"IP: {source_ip}, Reason: {reason}")
    
    def cleanup_expired(self):
        """Remove expired blacklist entries"""
        current_time = datetime.now(timezone.utc).isoformat()
        expired = [
            ip for ip, entry in self.blacklist.items()
            if entry.expires_at and current_time > entry.expires_at
        ]
        
        for ip in expired:
            del self.blacklist[ip]
        
        if expired:
            self._log_event("BLACKLIST_CLEANUP", f"Removed {len(expired)} expired entries")
    
    def get_blacklist_report(self) -> Dict[str, Any]:
        """Get blacklist status report"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_blacklisted": len(self.blacklist),
            "by_threat_level": {
                level.value: len([e for e in self.blacklist.values() if e.threat_level == level])
                for level in ThreatLevel
            },
            "sources_with_violations": len(self.violation_history),
            "entries": [
                {
                    "ip": entry.source_ip,
                    "reason": entry.reason,
                    "threat_level": entry.threat_level.value,
                    "blocked_at": entry.blocked_at,
                    "expires_at": entry.expires_at,
                    "violation_count": entry.violation_count
                }
                for entry in list(self.blacklist.values())[:20]  # Top 20
            ]
        }
    
    def _log_event(self, event_type: str, message: str):
        """Log event to file"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


class LazySecurity:
    """
    Lazy Security: Energy-efficient protection
    
    Activates protections only when Rotesschild scan detects
    electromagnetic pressure > 50 mV/m.
    
    Based on Lex Amoris: Don't waste energy on unnecessary defense.
    """
    
    def __init__(self):
        self.current_mode = ProtectionMode.DORMANT
        self.em_pressure_threshold = 50.0  # mV/m
        self.pressure_history: List[Tuple[float, str]] = []
        self.mode_changes: List[Dict[str, Any]] = []
    
    def scan_rotesschild(self) -> float:
        """
        Simulate Rotesschild electromagnetic scan
        
        In production, this would interface with actual EM sensors.
        Returns pressure in mV/m.
        """
        # Simulate EM pressure based on time and environmental factors
        import random
        timestamp = time.time()
        
        # Base pressure (background EM noise)
        base_pressure = 20.0
        
        # Add some variance
        variance = random.uniform(-10, 10)
        
        # Occasional spikes (simulating actual EM events)
        if random.random() < 0.1:  # 10% chance of spike
            variance += random.uniform(30, 80)
        
        pressure = base_pressure + variance
        
        # Record pressure
        self.pressure_history.append((pressure, datetime.now(timezone.utc).isoformat()))
        
        # Limit history
        if len(self.pressure_history) > 1000:
            self.pressure_history = self.pressure_history[-500:]
        
        return max(0, pressure)
    
    def update_protection_mode(self) -> ProtectionMode:
        """
        Update protection mode based on EM pressure
        
        Returns current protection mode
        """
        current_pressure = self.scan_rotesschild()
        old_mode = self.current_mode
        
        # Determine new mode based on pressure
        if current_pressure < self.em_pressure_threshold * 0.5:
            # Very low pressure - stay dormant
            self.current_mode = ProtectionMode.DORMANT
        elif current_pressure < self.em_pressure_threshold:
            # Below threshold - normal activity
            self.current_mode = ProtectionMode.ACTIVE
        elif current_pressure < self.em_pressure_threshold * 1.5:
            # Above threshold - be vigilant
            self.current_mode = ProtectionMode.VIGILANT
        else:
            # High pressure - emergency mode
            self.current_mode = ProtectionMode.EMERGENCY
        
        # Record mode change
        if old_mode != self.current_mode:
            self.mode_changes.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "from_mode": old_mode.value,
                "to_mode": self.current_mode.value,
                "em_pressure": current_pressure,
                "reason": f"EM pressure: {current_pressure:.2f} mV/m"
            })
        
        return self.current_mode
    
    def should_activate_protection(self, protection_type: str) -> bool:
        """
        Check if a specific protection should be active
        
        Args:
            protection_type: Type of protection to check
            
        Returns:
            True if protection should be active
        """
        mode = self.update_protection_mode()
        
        # Different protections activate at different levels
        protection_requirements = {
            "basic_validation": ProtectionMode.ACTIVE,
            "rhythm_check": ProtectionMode.ACTIVE,
            "blacklist": ProtectionMode.ACTIVE,
            "deep_inspection": ProtectionMode.VIGILANT,
            "aggressive_filtering": ProtectionMode.VIGILANT,
            "emergency_lockdown": ProtectionMode.EMERGENCY
        }
        
        required_mode = protection_requirements.get(protection_type, ProtectionMode.ACTIVE)
        
        # Check if current mode is at or above required level
        mode_levels = {
            ProtectionMode.DORMANT: 0,
            ProtectionMode.ACTIVE: 1,
            ProtectionMode.VIGILANT: 2,
            ProtectionMode.EMERGENCY: 3
        }
        
        return mode_levels[mode] >= mode_levels[required_mode]
    
    def get_energy_report(self) -> Dict[str, Any]:
        """Get energy and protection status report"""
        current_pressure = self.scan_rotesschild()
        
        # Calculate average pressure
        recent_pressures = [p for p, _ in self.pressure_history[-100:]]
        avg_pressure = sum(recent_pressures) / len(recent_pressures) if recent_pressures else 0
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_mode": self.current_mode.value,
            "current_em_pressure": round(current_pressure, 2),
            "average_em_pressure": round(avg_pressure, 2),
            "threshold_mv_per_m": self.em_pressure_threshold,
            "protection_active": self.current_mode != ProtectionMode.DORMANT,
            "mode_changes_count": len(self.mode_changes),
            "recent_mode_changes": self.mode_changes[-5:],
            "energy_efficiency": "HIGH" if self.current_mode == ProtectionMode.DORMANT else "NORMAL"
        }


class LexAmorisSecurityManager:
    """
    Main security manager integrating all Lex Amoris security components
    """
    
    def __init__(self):
        self.rhythm_validator = RhythmValidator()
        self.blacklist = DynamicBlacklist()
        self.lazy_security = LazySecurity()
        self.log_path = "logs/lex_amoris_security.log"
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def validate_packet(self, packet: DataPacket) -> Tuple[bool, str]:
        """
        Validate a data packet through complete Lex Amoris security
        
        Returns:
            Tuple of (is_valid, reason)
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # 1. Check blacklist first (most efficient)
        is_blocked, entry = self.blacklist.is_blacklisted(packet.source_ip)
        if is_blocked:
            reason = f"Source blacklisted: {entry.reason}"
            self._log_event("PACKET_BLOCKED", f"IP: {packet.source_ip}, Reason: {reason}")
            return False, reason
        
        # 2. Check if protection should be active (Lazy Security)
        if not self.lazy_security.should_activate_protection("rhythm_check"):
            # Dormant mode - let it through with minimal check
            self._log_event("PACKET_ACCEPTED", f"IP: {packet.source_ip}, Mode: DORMANT")
            return True, "Accepted (dormant mode)"
        
        # 3. Validate rhythm (Rhythm Validation)
        rhythm_status, harmony_score = self.rhythm_validator.validate_packet_rhythm(packet)
        
        if rhythm_status == RhythmStatus.INVALID:
            reason = "Invalid rhythm signature"
            self.blacklist.record_violation(packet.source_ip, reason, ThreatLevel.MEDIUM)
            self._log_event("PACKET_REJECTED", f"IP: {packet.source_ip}, Reason: {reason}")
            return False, reason
        
        if rhythm_status == RhythmStatus.SUSPICIOUS:
            if harmony_score < 0.5:
                reason = f"Suspicious rhythm (harmony: {harmony_score:.2f})"
                self.blacklist.record_violation(packet.source_ip, reason, ThreatLevel.LOW)
                self._log_event("PACKET_REJECTED", f"IP: {packet.source_ip}, Reason: {reason}")
                return False, reason
            else:
                # Allow but log
                self._log_event("PACKET_WARNING", 
                              f"IP: {packet.source_ip}, Harmony: {harmony_score:.2f}")
        
        # Packet is valid
        self._log_event("PACKET_ACCEPTED", 
                       f"IP: {packet.source_ip}, Harmony: {harmony_score:.2f}")
        return True, f"Valid (harmony: {harmony_score:.2f})"
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get complete security status dashboard"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lex_amoris_version": "1.0.0",
            "rhythm_validation": self.rhythm_validator.get_rhythm_report(),
            "blacklist": self.blacklist.get_blacklist_report(),
            "lazy_security": self.lazy_security.get_energy_report(),
            "overall_status": {
                "protection_mode": self.lazy_security.current_mode.value,
                "rhythm_patterns": len(self.rhythm_validator.known_patterns),
                "blacklisted_sources": len(self.blacklist.blacklist),
                "system_health": "OPERATIONAL"
            }
        }
    
    def _log_event(self, event_type: str, message: str):
        """Log security event"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


# Global instance
_security_manager: Optional[LexAmorisSecurityManager] = None


def get_security_manager() -> LexAmorisSecurityManager:
    """Get or create global security manager"""
    global _security_manager
    if _security_manager is None:
        _security_manager = LexAmorisSecurityManager()
    return _security_manager


if __name__ == "__main__":
    # Demo
    print("🔒 Lex Amoris Security System Demo")
    print("=" * 60)
    
    manager = LexAmorisSecurityManager()
    
    # Create some test packets
    print("\n📦 Testing packet validation...")
    
    # Valid packet
    packet1 = DataPacket(
        packet_id="PKT-001",
        source_ip="192.168.1.100",
        timestamp=datetime.now(timezone.utc).isoformat(),
        data=b"Valid data with good rhythm",
        metadata={"type": "heartbeat"}
    )
    
    valid, reason = manager.validate_packet(packet1)
    print(f"   Packet 1: {'✅ VALID' if valid else '❌ INVALID'} - {reason}")
    
    # Simulate multiple packets from suspicious source
    print("\n🔍 Testing rhythm validation...")
    for i in range(3):
        packet = DataPacket(
            packet_id=f"PKT-{i+2:03d}",
            source_ip="10.0.0.50",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=b"Test data " * i,
            metadata={}
        )
        valid, reason = manager.validate_packet(packet)
        time.sleep(0.1)
    
    # Get security dashboard
    print("\n📊 Security Dashboard:")
    dashboard = manager.get_security_dashboard()
    print(f"   Protection Mode: {dashboard['overall_status']['protection_mode']}")
    print(f"   EM Pressure: {dashboard['lazy_security']['current_em_pressure']:.2f} mV/m")
    print(f"   Blacklisted Sources: {dashboard['overall_status']['blacklisted_sources']}")
    print(f"   System Health: {dashboard['overall_status']['system_health']}")
    
    print("\n✅ Lex Amoris Security Demo Complete!")
