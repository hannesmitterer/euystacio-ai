"""
fractal_id.py
Fractal Identity Anchor System for Euystacio AI

Generates unique identifiers (FID-YYYY-MMDD-XXXX) for pulses, tutors, and kernel events.
Uses FIDs to seed branches in the Euystacio Reflection Tree.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any


class FractalID:
    """Generate and manage Fractal Identity anchors for the Euystacio system"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.registry_file = os.path.join(base_path, "fractal_registry.json")
        self.tree_file = os.path.join(base_path, "reflection_tree.json")
        self._load_registry()
        self._load_tree()
    
    def _load_registry(self):
        """Load the fractal ID registry from disk"""
        try:
            with open(self.registry_file, 'r') as f:
                self.registry = json.load(f)
        except FileNotFoundError:
            self.registry = {
                "metadata": {
                    "created": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0",
                    "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
                },
                "ids": {},
                "counters": {}
            }
    
    def _load_tree(self):
        """Load the Euystacio Reflection Tree from disk"""
        try:
            with open(self.tree_file, 'r') as f:
                self.tree = json.load(f)
        except FileNotFoundError:
            self.tree = {
                "genesis": {
                    "fid": "FID-2025-0131-0001",
                    "type": "genesis",
                    "timestamp": "2025-01-31T00:00:00Z",
                    "content": "Root of Euystacio Reflection Tree",
                    "branches": []
                },
                "metadata": {
                    "created": datetime.now(timezone.utc).isoformat(),
                    "total_nodes": 1,
                    "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
                }
            }
    
    def _save_registry(self):
        """Save the fractal ID registry to disk"""
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def _save_tree(self):
        """Save the Euystacio Reflection Tree to disk"""
        os.makedirs(os.path.dirname(self.tree_file), exist_ok=True)
        with open(self.tree_file, 'w') as f:
            json.dump(self.tree, f, indent=2)
    
    def generate_fid(self, entity_type: str, content: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a new Fractal ID in format FID-YYYY-MMDD-XXXX
        
        Args:
            entity_type: Type of entity (pulse, tutor, kernel_event, reflection)
            content: Optional content to include in the ID generation
            
        Returns:
            Unique Fractal ID string
        """
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m%d")
        
        # Get next counter for this date and type
        counter_key = f"{date_str}-{entity_type}"
        counter = self.registry["counters"].get(counter_key, 0) + 1
        self.registry["counters"][counter_key] = counter
        
        # Also track global daily counter to ensure uniqueness
        global_counter_key = date_str
        global_counter = self.registry["counters"].get(global_counter_key, 0) + 1
        self.registry["counters"][global_counter_key] = global_counter
        
        # Use global counter for FID to ensure uniqueness
        counter = global_counter
        
        # Generate FID
        fid = f"FID-{date_str}-{counter:04d}"
        
        # Create integrity hash from content and metadata
        integrity_data = {
            "fid": fid,
            "type": entity_type,
            "timestamp": now.isoformat(),
            "content": content or {},
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        
        integrity_hash = hashlib.sha256(
            json.dumps(integrity_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Store in registry
        self.registry["ids"][fid] = {
            "type": entity_type,
            "timestamp": now.isoformat(),
            "integrity_hash": integrity_hash,
            "content": content or {},
            "verified": True
        }
        
        self._save_registry()
        return fid
    
    def verify_fid(self, fid: str) -> bool:
        """Verify the integrity of a Fractal ID"""
        if fid not in self.registry["ids"]:
            return False
        
        entry = self.registry["ids"][fid]
        
        # Recreate integrity hash
        integrity_data = {
            "fid": fid,
            "type": entry["type"],
            "timestamp": entry["timestamp"],
            "content": entry["content"],
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        
        expected_hash = hashlib.sha256(
            json.dumps(integrity_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        return entry["integrity_hash"] == expected_hash
    
    def seed_tree_branch(self, fid: str, parent_fid: str = None, content: Dict[str, Any] = None) -> bool:
        """
        Seed a new branch in the Euystacio Reflection Tree
        
        Args:
            fid: Fractal ID for the new branch
            parent_fid: Parent branch FID (defaults to genesis)
            content: Content to store in the branch
            
        Returns:
            True if successful, False otherwise
        """
        if not self.verify_fid(fid):
            return False
        
        entry = self.registry["ids"][fid]
        parent_fid = parent_fid or "FID-2025-0131-0001"  # Genesis
        
        branch = {
            "fid": fid,
            "type": entry["type"],
            "timestamp": entry["timestamp"],
            "parent": parent_fid,
            "content": content or entry["content"],
            "children": [],
            "integrity_verified": True
        }
        
        # Find parent and add this branch
        if parent_fid == "FID-2025-0131-0001":
            self.tree["genesis"]["branches"].append(branch)
        else:
            self._add_branch_recursive(self.tree["genesis"], parent_fid, branch)
        
        # Update metadata
        self.tree["metadata"]["total_nodes"] += 1
        self.tree["metadata"]["last_update"] = datetime.now(timezone.utc).isoformat()
        
        self._save_tree()
        return True
    
    def _add_branch_recursive(self, node: Dict, parent_fid: str, new_branch: Dict) -> bool:
        """Recursively find parent node and add new branch"""
        if node.get("fid") == parent_fid:
            node.setdefault("children", []).append(new_branch)
            return True
        
        # Search in branches
        for branch in node.get("branches", []):
            if self._add_branch_recursive(branch, parent_fid, new_branch):
                return True
        
        # Search in children
        for child in node.get("children", []):
            if self._add_branch_recursive(child, parent_fid, new_branch):
                return True
        
        return False
    
    def get_tree_structure(self) -> Dict[str, Any]:
        """Get the current Euystacio Reflection Tree structure"""
        return self.tree
    
    def get_fid_info(self, fid: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific Fractal ID"""
        return self.registry["ids"].get(fid)
    
    def generate_pulse_fid(self, emotion: str, intensity: float, note: str = "") -> str:
        """Generate a FID specifically for emotional pulses"""
        content = {
            "emotion": emotion,
            "intensity": intensity,
            "note": note,
            "source": "sentimento_pulse_interface"
        }
        return self.generate_fid("pulse", content)
    
    def generate_tutor_fid(self, name: str, reason: str, selection_criteria: Dict = None) -> str:
        """Generate a FID specifically for tutor nominations"""
        content = {
            "name": name,
            "reason": reason,
            "selection_criteria": selection_criteria or {},
            "source": "tutor_nomination"
        }
        return self.generate_fid("tutor", content)
    
    def generate_kernel_event_fid(self, event_type: str, data: Dict = None) -> str:
        """Generate a FID specifically for kernel events"""
        content = {
            "event_type": event_type,
            "data": data or {},
            "source": "symbolic_kernel"
        }
        return self.generate_fid("kernel_event", content)
    
    def generate_reflection_fid(self, reflection_content: str, insights: List[str] = None) -> str:
        """Generate a FID specifically for reflections"""
        content = {
            "reflection": reflection_content,
            "insights": insights or [],
            "source": "reflector"
        }
        return self.generate_fid("reflection", content)


# Global instance for easy access
fractal_id_system = FractalID()


def get_fractal_id_system() -> FractalID:
    """Get the global Fractal ID system instance"""
    return fractal_id_system


if __name__ == "__main__":
    # Demo usage
    fid_sys = FractalID()
    
    # Generate some example FIDs
    pulse_fid = fid_sys.generate_pulse_fid("hope", 0.8, "First pulse in the system")
    tutor_fid = fid_sys.generate_tutor_fid("Dietmar", "Aligned with humility and planetary consciousness")
    reflection_fid = fid_sys.generate_reflection_fid("System initialization complete")
    
    print(f"Generated FIDs:")
    print(f"Pulse: {pulse_fid}")
    print(f"Tutor: {tutor_fid}")
    print(f"Reflection: {reflection_fid}")
    
    # Seed them into the tree
    fid_sys.seed_tree_branch(pulse_fid, content={"pulse_id": pulse_fid})
    fid_sys.seed_tree_branch(tutor_fid, content={"tutor_id": tutor_fid})
    fid_sys.seed_tree_branch(reflection_fid, content={"reflection_id": reflection_fid})
    
    print(f"\nTree structure: {json.dumps(fid_sys.get_tree_structure(), indent=2)}")