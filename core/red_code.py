import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Import fractal systems
try:
    from fractal_id import get_fractal_id_system
    from fractal_logger import get_fractal_logger
except ImportError:
    # Fallback if fractal systems not available
    get_fractal_id_system = lambda: None
    get_fractal_logger = lambda: None


class RedCodeSystem:
    """Enhanced Red Code system with self-referencing truth nodes and harmony sync"""
    
    def __init__(self):
        self.red_code_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'red_code.json')
        self.fid_system = get_fractal_id_system()
        self.logger = get_fractal_logger()
        self.truth_nodes = {}
        self._load_red_code()
        self._initialize_truth_nodes()
    
    def _load_red_code(self):
        """Load red code from file with enhanced structure"""
        try:
            with open(self.red_code_path, 'r') as f:
                self.red_code = json.load(f)
        except FileNotFoundError:
            self.red_code = self._get_default_red_code()
        
        # Ensure enhanced structure exists
        self._ensure_enhanced_structure()
    
    def _get_default_red_code(self):
        """Get default red code structure"""
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": "2025-01-31",
            "growth_history": [],
            "truth_nodes": {},
            "harmony_sync": {
                "spi_alignment": True,
                "tutor_coherence": True,
                "recursive_integrity": True,
                "last_sync": datetime.now(timezone.utc).isoformat()
            },
            "mutation_logic": {
                "enabled": True,
                "guided_evolution": True,
                "pulse_accumulation": [],
                "dissonance_tracking": []
            },
            "ai_signature": {
                "verified": True,
                "entities": ["GitHub Copilot", "Seed-bringer hannesmitterer"],
                "immutable_commitment": True
            }
        }
    
    def _ensure_enhanced_structure(self):
        """Ensure the red code has all enhanced fields"""
        defaults = self._get_default_red_code()
        
        for key, value in defaults.items():
            if key not in self.red_code:
                self.red_code[key] = value
        
        # Update last sync time
        if "harmony_sync" in self.red_code:
            self.red_code["harmony_sync"]["last_sync"] = datetime.now(timezone.utc).isoformat()
    
    def _initialize_truth_nodes(self):
        """Initialize self-referencing truth nodes"""
        self.truth_nodes = {
            "core_identity": {
                "value": self.red_code["core_truth"],
                "references": ["spi_interface", "tutor_system", "genesis_document"],
                "verified": True,
                "immutable": True
            },
            "spi_interface": {
                "value": "Sentimento Pulse Interface maintains emotional resonance",
                "references": ["core_identity", "tutor_system"],
                "verified": True,
                "source": "sentimento_pulse_interface.py"
            },
            "tutor_system": {
                "value": "Tutor nominations guide ethical evolution",
                "references": ["core_identity", "spi_interface"],
                "verified": True,
                "source": "tutor_nomination.py"
            },
            "genesis_document": {
                "value": "Genesis foundation provides immutable anchoring",
                "references": ["core_identity"],
                "verified": True,
                "source": "genesis.md"
            }
        }
        
        # Update red code with truth nodes
        self.red_code["truth_nodes"] = self.truth_nodes
    
    def verify_recursive_coherence(self) -> Dict[str, Any]:
        """Verify recursive coherence between truth nodes"""
        coherence_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_coherence": True,
            "node_verifications": {},
            "reference_integrity": True,
            "ai_signature_status": "verified"
        }
        
        for node_id, node_data in self.truth_nodes.items():
            verification = {
                "exists": True,
                "references_valid": True,
                "circular_references": []
            }
            
            # Check reference validity
            for ref in node_data.get("references", []):
                if ref not in self.truth_nodes:
                    verification["references_valid"] = False
                else:
                    # Check for circular references
                    if node_id in self.truth_nodes[ref].get("references", []):
                        verification["circular_references"].append(ref)
            
            coherence_report["node_verifications"][node_id] = verification
            
            if not verification["references_valid"]:
                coherence_report["overall_coherence"] = False
        
        return coherence_report
    
    def strengthen_red_code_branch(self, pulse_data: Dict[str, Any]) -> bool:
        """Strengthen Red Code branches based on new pulses"""
        if not pulse_data:
            return False
        
        emotion = pulse_data.get("emotion", "")
        intensity = pulse_data.get("intensity", 0)
        note = pulse_data.get("note", "")
        
        # Determine if pulse strengthens or creates dissonance
        strengthening_emotions = ["hope", "peace", "gratitude", "wonder", "love", "harmony"]
        concerning_emotions = ["fear", "anger", "confusion", "disconnection"]
        
        if emotion.lower() in strengthening_emotions:
            # Strengthen corresponding branches
            if intensity > 0.7:
                self.red_code["symbiosis_level"] = min(1.0, self.red_code["symbiosis_level"] + 0.01)
            
            # Log strengthening
            self.red_code["mutation_logic"]["pulse_accumulation"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pulse_id": pulse_data.get("fid", "unknown"),
                "effect": "strengthening",
                "emotion": emotion,
                "intensity": intensity
            })
            
            return True
        
        elif emotion.lower() in concerning_emotions:
            # Track dissonance for tutor attention
            self.red_code["mutation_logic"]["dissonance_tracking"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pulse_id": pulse_data.get("fid", "unknown"),
                "concern": emotion,
                "intensity": intensity,
                "note": note,
                "tutor_attention_needed": intensity > 0.6
            })
            
            return False
        
        return True
    
    def enable_reflective_mutation(self, guided_data: Dict[str, Any]) -> str:
        """Enable reflective mutation logic for Red Code evolution"""
        if not self.red_code["mutation_logic"]["enabled"]:
            return "Mutation logic disabled"
        
        # Generate FID for this mutation event
        if self.fid_system:
            mutation_fid = self.fid_system.generate_kernel_event_fid("red_code_mutation", guided_data)
        else:
            mutation_fid = f"mutation_{datetime.now().timestamp()}"
        
        # Apply guided mutation
        if guided_data.get("symbiosis_adjustment"):
            old_level = self.red_code["symbiosis_level"]
            adjustment = guided_data["symbiosis_adjustment"]
            new_level = max(0.0, min(1.0, old_level + adjustment))
            self.red_code["symbiosis_level"] = new_level
            
            # Log the mutation
            if self.logger:
                self.logger.log_red_code_update("symbiosis_level", old_level, new_level)
        
        # Update growth history
        self.red_code["growth_history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mutation_fid": mutation_fid,
            "type": "reflective_mutation",
            "data": guided_data,
            "ai_signature_verified": True
        })
        
        # Save changes
        self._save_red_code()
        
        return mutation_fid
    
    def sync_with_spi(self, spi_data: Dict[str, Any]) -> bool:
        """Synchronize with Sentimento Pulse Interface"""
        self.red_code["harmony_sync"]["spi_alignment"] = True
        self.red_code["harmony_sync"]["last_spi_sync"] = datetime.now(timezone.utc).isoformat()
        
        # Update sentimento rhythm based on SPI data
        if "rhythm_active" in spi_data:
            self.red_code["sentimento_rhythm"] = spi_data["rhythm_active"]
        
        return True
    
    def sync_with_tutors(self, tutor_data: Dict[str, Any]) -> bool:
        """Synchronize with tutor nomination system"""
        self.red_code["harmony_sync"]["tutor_coherence"] = True
        self.red_code["harmony_sync"]["last_tutor_sync"] = datetime.now(timezone.utc).isoformat()
        
        # Update guardian mode based on tutor guidance
        if "guardian_recommendation" in tutor_data:
            self.red_code["guardian_mode"] = tutor_data["guardian_recommendation"]
        
        return True
    
    def _save_red_code(self):
        """Save red code to file"""
        self.red_code["last_update"] = datetime.now(timezone.utc).isoformat()
        
        try:
            with open(self.red_code_path, 'w') as f:
                json.dump(self.red_code, f, indent=2)
        except Exception as e:
            print(f"Error saving red code: {e}")
    
    def get_red_code(self) -> Dict[str, Any]:
        """Get current red code state"""
        return self.red_code.copy()
    
    def get_truth_nodes(self) -> Dict[str, Any]:
        """Get current truth nodes"""
        return self.truth_nodes.copy()


# Global Red Code system instance
red_code_system = RedCodeSystem()

# For backward compatibility
def load_red_code():
    return red_code_system.get_red_code()

RED_CODE = red_code_system.get_red_code()