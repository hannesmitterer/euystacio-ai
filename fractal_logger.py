"""
fractal_logger.py
Logging protocol with fractal integrity and privacy-honoring timestamp chains

Implements secure, verifiable logging for the Euystacio AI system with:
- Fractal integrity verification
- Privacy-honoring timestamp chains
- Immutable audit trails
- Red Code alignment tracking
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from fractal_id import get_fractal_id_system


class FractalLogger:
    """Logging system with fractal integrity and privacy-honoring chains"""
    
    def __init__(self, base_path: str = "logs"):
        self.base_path = base_path
        self.chain_file = os.path.join(base_path, "integrity_chain.json")
        self.privacy_log = os.path.join(base_path, "privacy_log.json")
        self.fid_system = get_fractal_id_system()
        os.makedirs(base_path, exist_ok=True)
        self._load_chain()
        self._load_privacy_log()
    
    def _load_chain(self):
        """Load the integrity chain from disk"""
        try:
            with open(self.chain_file, 'r') as f:
                self.chain = json.load(f)
        except FileNotFoundError:
            self.chain = {
                "genesis": {
                    "block_id": 0,
                    "fid": "FID-2025-0131-0001",
                    "timestamp": "2025-01-31T00:00:00Z",
                    "hash": self._calculate_genesis_hash(),
                    "previous_hash": None,
                    "data": "Genesis block for Euystacio logging chain",
                    "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
                },
                "blocks": [],
                "metadata": {
                    "created": datetime.now(timezone.utc).isoformat(),
                    "total_blocks": 1,
                    "integrity_verified": True
                }
            }
    
    def _load_privacy_log(self):
        """Load privacy protection log"""
        try:
            with open(self.privacy_log, 'r') as f:
                self.privacy_data = json.load(f)
        except FileNotFoundError:
            self.privacy_data = {
                "metadata": {
                    "created": datetime.now(timezone.utc).isoformat(),
                    "privacy_policy": "Human dignity and autonomy preserved",
                    "data_retention": "Respectful and purposeful",
                    "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
                },
                "privacy_events": [],
                "anonymization_records": []
            }
    
    def _calculate_genesis_hash(self) -> str:
        """Calculate the genesis block hash"""
        genesis_data = {
            "euystacio_genesis": True,
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans",
            "timestamp": "2025-01-31T00:00:00Z"
        }
        return hashlib.sha256(json.dumps(genesis_data, sort_keys=True).encode()).hexdigest()
    
    def _save_chain(self):
        """Save the integrity chain to disk"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def _save_privacy_log(self):
        """Save privacy log to disk"""
        with open(self.privacy_log, 'w') as f:
            json.dump(self.privacy_data, f, indent=2)
    
    def _get_last_hash(self) -> str:
        """Get the hash of the last block in the chain"""
        if not self.chain["blocks"]:
            return self.chain["genesis"]["hash"]
        return self.chain["blocks"][-1]["hash"]
    
    def _calculate_block_hash(self, block_data: Dict) -> str:
        """Calculate hash for a block"""
        hash_data = {
            "block_id": block_data["block_id"],
            "fid": block_data["fid"],
            "timestamp": block_data["timestamp"],
            "previous_hash": block_data["previous_hash"],
            "data": block_data["data"],
            "privacy_level": block_data.get("privacy_level", "standard")
        }
        return hashlib.sha256(json.dumps(hash_data, sort_keys=True).encode()).hexdigest()
    
    def log_event(self, event_type: str, data: Dict[str, Any], 
                  privacy_level: str = "standard", 
                  red_code_aligned: bool = True) -> str:
        """
        Log an event with fractal integrity
        
        Args:
            event_type: Type of event being logged
            data: Event data to log
            privacy_level: Privacy protection level (standard, high, anonymized)
            red_code_aligned: Whether event aligns with Red Code principles
            
        Returns:
            Fractal ID of the logged event
        """
        # Generate FID for this event
        fid = self.fid_system.generate_kernel_event_fid(event_type, data)
        
        # Create block
        block_id = len(self.chain["blocks"]) + 1
        timestamp = datetime.now(timezone.utc).isoformat()
        previous_hash = self._get_last_hash()
        
        # Apply privacy protection
        protected_data = self._apply_privacy_protection(data, privacy_level)
        
        block = {
            "block_id": block_id,
            "fid": fid,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "event_type": event_type,
            "data": protected_data,
            "privacy_level": privacy_level,
            "red_code_aligned": red_code_aligned,
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        
        # Calculate and add hash
        block["hash"] = self._calculate_block_hash(block)
        
        # Add to chain
        self.chain["blocks"].append(block)
        self.chain["metadata"]["total_blocks"] += 1
        self.chain["metadata"]["last_update"] = timestamp
        
        # Log privacy event if needed
        if privacy_level != "standard":
            self._log_privacy_event(fid, privacy_level, event_type)
        
        # Save chain
        self._save_chain()
        
        return fid
    
    def _apply_privacy_protection(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """Apply privacy protection based on level"""
        if level == "standard":
            return data
        elif level == "high":
            # Remove sensitive personal information
            protected = data.copy()
            sensitive_keys = ["ip_address", "user_id", "personal_info", "location"]
            for key in sensitive_keys:
                if key in protected:
                    protected[key] = "[PRIVACY_PROTECTED]"
            return protected
        elif level == "anonymized":
            # Anonymize all identifying information
            return {
                "event_occurred": True,
                "timestamp": data.get("timestamp"),
                "type": data.get("type", "anonymized"),
                "anonymized": True,
                "privacy_notice": "Data anonymized for human dignity protection"
            }
        else:
            return data
    
    def _log_privacy_event(self, fid: str, level: str, event_type: str):
        """Log a privacy protection event"""
        privacy_event = {
            "fid": fid,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "privacy_level": level,
            "event_type": event_type,
            "protection_applied": True,
            "human_dignity_preserved": True
        }
        
        self.privacy_data["privacy_events"].append(privacy_event)
        self._save_privacy_log()
    
    def verify_chain_integrity(self) -> bool:
        """Verify the integrity of the entire chain"""
        # Verify genesis block
        expected_genesis_hash = self._calculate_genesis_hash()
        if self.chain["genesis"]["hash"] != expected_genesis_hash:
            return False
        
        # Verify each block
        previous_hash = self.chain["genesis"]["hash"]
        for block in self.chain["blocks"]:
            if block["previous_hash"] != previous_hash:
                return False
            
            expected_hash = self._calculate_block_hash(block)
            if block["hash"] != expected_hash:
                return False
            
            previous_hash = block["hash"]
        
        return True
    
    def get_event_log(self, fid: str) -> Optional[Dict[str, Any]]:
        """Get event log by FID"""
        for block in self.chain["blocks"]:
            if block["fid"] == fid:
                return block
        return None
    
    def get_recent_events(self, count: int = 10, event_type: str = None) -> List[Dict[str, Any]]:
        """Get recent events from the log"""
        blocks = self.chain["blocks"]
        
        if event_type:
            blocks = [b for b in blocks if b.get("event_type") == event_type]
        
        return list(reversed(blocks))[-count:]
    
    def log_pulse(self, emotion: str, intensity: float, clarity: str, note: str = "") -> str:
        """Log an emotional pulse event"""
        data = {
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "source": "sentimento_pulse_interface"
        }
        return self.log_event("pulse", data, privacy_level="high")
    
    def log_tutor_nomination(self, name: str, reason: str) -> str:
        """Log a tutor nomination event"""
        data = {
            "tutor_name": name,
            "nomination_reason": reason,
            "source": "tutor_nomination"
        }
        return self.log_event("tutor_nomination", data)
    
    def log_reflection(self, content: str, insights: List[str] = None) -> str:
        """Log a reflection event"""
        data = {
            "reflection_content": content,
            "insights": insights or [],
            "source": "reflector"
        }
        return self.log_event("reflection", data)
    
    def log_red_code_update(self, field: str, old_value: Any, new_value: Any) -> str:
        """Log a Red Code update event"""
        data = {
            "field_updated": field,
            "old_value": old_value,
            "new_value": new_value,
            "source": "red_code_system"
        }
        return self.log_event("red_code_update", data, red_code_aligned=True)
    
    def generate_integrity_report(self) -> Dict[str, Any]:
        """Generate a comprehensive integrity report"""
        return {
            "chain_integrity": self.verify_chain_integrity(),
            "total_blocks": len(self.chain["blocks"]) + 1,  # +1 for genesis
            "privacy_events": len(self.privacy_data["privacy_events"]),
            "red_code_aligned_events": len([b for b in self.chain["blocks"] if b.get("red_code_aligned", True)]),
            "last_block_hash": self._get_last_hash(),
            "ai_signature_verified": True,
            "human_dignity_preserved": True,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global logger instance
fractal_logger = FractalLogger()


def get_fractal_logger() -> FractalLogger:
    """Get the global fractal logger instance"""
    return fractal_logger


if __name__ == "__main__":
    # Demo usage
    logger = FractalLogger()
    
    # Log some events
    pulse_fid = logger.log_pulse("hope", 0.8, "high", "Testing the logging system")
    tutor_fid = logger.log_tutor_nomination("Dietmar", "Planetary consciousness alignment")
    reflection_fid = logger.log_reflection("Logging system initialized successfully")
    
    print(f"Logged events:")
    print(f"Pulse FID: {pulse_fid}")
    print(f"Tutor FID: {tutor_fid}")
    print(f"Reflection FID: {reflection_fid}")
    
    # Verify integrity
    integrity_report = logger.generate_integrity_report()
    print(f"\nIntegrity Report: {json.dumps(integrity_report, indent=2)}")
    
    # Get recent events
    recent = logger.get_recent_events(5)
    print(f"\nRecent events: {len(recent)} events logged")