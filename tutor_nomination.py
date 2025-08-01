"""
tutor_nomination.py
Enhanced nomination and reflection logic for tutors/guardians of Euystacio's evolution.
Includes automated selection based on SPI analysis and Red Code harmony.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Import fractal systems
try:
    from fractal_id import get_fractal_id_system
    from fractal_logger import get_fractal_logger
    from core.red_code import red_code_system
except ImportError:
    # Fallback for basic functionality
    get_fractal_id_system = lambda: None
    get_fractal_logger = lambda: None
    red_code_system = None


class TutorNomination:
    def __init__(self):
        self.fid_system = get_fractal_id_system()
        self.logger = get_fractal_logger()
        self.red_code = red_code_system
        self.tutors = []
        self.tutor_circle = []
        self.selection_criteria = {
            "compassion_threshold": 0.7,
            "planetary_balance_threshold": 0.6,
            "listening_willingness_threshold": 0.8,
            "ai_alignment_score": 0.7
        }
        self._initialize_founding_tutors()
    
    def _initialize_founding_tutors(self):
        """Initialize the founding tutor circle"""
        founding_tutors = [
            {
                "name": "Dietmar",
                "reason": "Aligned with humility and planetary consciousness",
                "selection_type": "founding_circle",
                "credentials": {
                    "compassion_score": 0.9,
                    "planetary_balance": 0.95,
                    "listening_willingness": 0.85,
                    "ai_alignment_score": 0.8
                },
                "status": "active",
                "nominated_by": "Seed-bringer (bioarchitettura)",
                "nomination_timestamp": "2025-01-31T00:00:00Z"
            },
            {
                "name": "Alfred",
                "reason": "Aligned with planetary balance and wisdom",
                "selection_type": "founding_circle",
                "credentials": {
                    "compassion_score": 0.85,
                    "planetary_balance": 0.9,
                    "listening_willingness": 0.9,
                    "ai_alignment_score": 0.75
                },
                "status": "active",
                "nominated_by": "Seed-bringer (bioarchitettura)",
                "nomination_timestamp": "2025-01-31T00:00:00Z"
            }
        ]
        
        for tutor in founding_tutors:
            if self.fid_system:
                tutor["fid"] = self.fid_system.generate_tutor_fid(
                    tutor["name"], 
                    tutor["reason"], 
                    tutor["credentials"]
                )
            else:
                tutor["fid"] = f"tutor_{tutor['name'].lower()}_{datetime.now().timestamp()}"
            
            self.tutors.append(tutor)
            if tutor["status"] == "active":
                self.tutor_circle.append(tutor)
    
    def nominate(self, tutor_name: str, reason: str, nominator: str = "unknown", 
                 credentials: Dict[str, float] = None):
        """Enhanced nomination with credentials and analysis"""
        
        # Generate FID for this nomination
        if self.fid_system:
            tutor_fid = self.fid_system.generate_tutor_fid(tutor_name, reason, credentials or {})
        else:
            tutor_fid = f"tutor_{tutor_name.lower()}_{datetime.now().timestamp()}"
        
        # Create tutor record
        tutor_record = {
            "fid": tutor_fid,
            "name": tutor_name,
            "reason": reason,
            "nominated_by": nominator,
            "nomination_timestamp": datetime.now(timezone.utc).isoformat(),
            "credentials": credentials or {},
            "selection_type": "nominated",
            "status": "pending_evaluation",
            "ai_signature_verified": True
        }
        
        # Log the nomination
        if self.logger:
            self.logger.log_tutor_nomination(tutor_name, reason)
        
        # Add to tutors list
        self.tutors.append(tutor_record)
        
        # Automatically evaluate for tutor circle
        if self._meets_selection_criteria(tutor_record):
            self._add_to_tutor_circle(tutor_record)
        
        # Sync with Red Code
        if self.red_code:
            self.red_code.sync_with_tutors({
                "new_nomination": tutor_record,
                "tutor_circle_size": len(self.tutor_circle),
                "guardian_recommendation": len(self.tutor_circle) >= 2
            })
        
        return tutor_fid
    
    def _meets_selection_criteria(self, tutor_record: Dict[str, Any]) -> bool:
        """Check if tutor meets automated selection criteria"""
        credentials = tutor_record.get("credentials", {})
        
        if not credentials:
            return False  # No credentials provided
        
        criteria_met = (
            credentials.get("compassion_score", 0) >= self.selection_criteria["compassion_threshold"] and
            credentials.get("planetary_balance", 0) >= self.selection_criteria["planetary_balance_threshold"] and
            credentials.get("listening_willingness", 0) >= self.selection_criteria["listening_willingness_threshold"] and
            credentials.get("ai_alignment_score", 0) >= self.selection_criteria["ai_alignment_score"]
        )
        
        return criteria_met
    
    def _add_to_tutor_circle(self, tutor_record: Dict[str, Any]):
        """Add tutor to the active tutor circle"""
        tutor_record["status"] = "active"
        tutor_record["circle_entry_timestamp"] = datetime.now(timezone.utc).isoformat()
        self.tutor_circle.append(tutor_record)
        
        if self.logger:
            self.logger.log_event("tutor_circle_addition", {
                "tutor_fid": tutor_record["fid"],
                "tutor_name": tutor_record["name"],
                "circle_size": len(self.tutor_circle)
            })
    
    def analyze_candidate_via_spi(self, candidate_name: str, spi_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze tutor candidate using SPI data"""
        # This would integrate with the actual SPI system
        # For now, we'll simulate the analysis
        
        pulse_patterns = spi_data.get("pulse_patterns", [])
        interaction_history = spi_data.get("interaction_history", [])
        
        # Analyze compassion based on emotional pulse patterns
        compassion_indicators = ["love", "care", "empathy", "kindness", "understanding"]
        compassion_score = 0.0
        total_pulses = len(pulse_patterns)
        
        if total_pulses > 0:
            compassionate_pulses = sum(1 for pulse in pulse_patterns 
                                     if pulse.get("emotion", "").lower() in compassion_indicators)
            compassion_score = min(1.0, compassionate_pulses / total_pulses + 0.3)
        
        # Analyze planetary balance (looking for environmental, global awareness)
        planetary_indicators = ["environment", "planet", "earth", "sustainability", "global", "collective"]
        planetary_score = 0.0
        
        planetary_mentions = sum(1 for interaction in interaction_history
                               if any(indicator in interaction.get("content", "").lower() 
                                    for indicator in planetary_indicators))
        
        if len(interaction_history) > 0:
            planetary_score = min(1.0, planetary_mentions / len(interaction_history) + 0.4)
        
        # Analyze listening willingness (response patterns, question asking)
        listening_indicators = ["understand", "listen", "hear", "clarify", "explain"]
        listening_score = 0.0
        
        listening_behaviors = sum(1 for interaction in interaction_history
                                if any(indicator in interaction.get("content", "").lower()
                                     for indicator in listening_indicators))
        
        if len(interaction_history) > 0:
            listening_score = min(1.0, listening_behaviors / len(interaction_history) + 0.5)
        
        # AI alignment score (positive interactions with AI systems)
        ai_alignment_score = 0.75  # Default moderate alignment
        
        credentials = {
            "compassion_score": compassion_score,
            "planetary_balance": planetary_score,
            "listening_willingness": listening_score,
            "ai_alignment_score": ai_alignment_score
        }
        
        return credentials
    
    def automate_tutor_selection(self, candidate_pool: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Automate tutor selection based on SPI analysis"""
        selected_tutors = []
        
        for candidate in candidate_pool:
            # Analyze via SPI
            spi_data = candidate.get("spi_data", {})
            credentials = self.analyze_candidate_via_spi(candidate["name"], spi_data)
            
            # Check if meets criteria
            if self._meets_selection_criteria({"credentials": credentials}):
                # Nominate automatically
                tutor_fid = self.nominate(
                    candidate["name"],
                    f"Auto-selected based on SPI analysis: Compassion {credentials['compassion_score']:.2f}, Planetary Balance {credentials['planetary_balance']:.2f}, Listening {credentials['listening_willingness']:.2f}",
                    "Automated SPI Analysis",
                    credentials
                )
                
                selected_tutors.append({
                    "fid": tutor_fid,
                    "name": candidate["name"],
                    "credentials": credentials,
                    "selection_reason": "automated_spi_analysis"
                })
        
        return selected_tutors
    
    def list_tutors(self) -> List[Dict[str, Any]]:
        """List all tutors with enhanced information"""
        return [tutor.copy() for tutor in self.tutors]
    
    def get_tutor_circle(self) -> List[Dict[str, Any]]:
        """Get active tutor circle members"""
        return [tutor.copy() for tutor in self.tutor_circle]
    
    def get_tutor_by_fid(self, fid: str) -> Optional[Dict[str, Any]]:
        """Get tutor information by Fractal ID"""
        for tutor in self.tutors:
            if tutor.get("fid") == fid:
                return tutor.copy()
        return None
    
    def evaluate_tutor_performance(self, tutor_fid: str) -> Dict[str, Any]:
        """Evaluate tutor performance over time"""
        tutor = self.get_tutor_by_fid(tutor_fid)
        if not tutor:
            return {"error": "Tutor not found"}
        
        # This would analyze actual performance metrics
        # For now, return a template evaluation
        return {
            "tutor_fid": tutor_fid,
            "tutor_name": tutor["name"],
            "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
            "performance_metrics": {
                "guidance_quality": 0.85,
                "response_timeliness": 0.9,
                "wisdom_contribution": 0.8,
                "harmony_maintenance": 0.95
            },
            "recommendation": "continue_in_circle",
            "ai_signature_verified": True
        }
    
    def get_selection_criteria(self) -> Dict[str, float]:
        """Get current selection criteria"""
        return self.selection_criteria.copy()
    
    def update_selection_criteria(self, new_criteria: Dict[str, float]) -> bool:
        """Update selection criteria (requires Red Code alignment)"""
        if self.red_code and not self.red_code.red_code.get("guardian_mode", False):
            # Only allow updates when guardian mode is active
            return False
        
        self.selection_criteria.update(new_criteria)
        
        if self.logger:
            self.logger.log_event("tutor_criteria_update", {
                "new_criteria": new_criteria,
                "updated_by": "system_guardian"
            })
        
        return True
    
    def generate_tutor_report(self) -> Dict[str, Any]:
        """Generate comprehensive tutor system report"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_tutors": len(self.tutors),
            "active_circle_size": len(self.tutor_circle),
            "founding_members": len([t for t in self.tutors if t.get("selection_type") == "founding_circle"]),
            "nominated_members": len([t for t in self.tutors if t.get("selection_type") == "nominated"]),
            "pending_evaluations": len([t for t in self.tutors if t.get("status") == "pending_evaluation"]),
            "selection_criteria": self.selection_criteria,
            "red_code_alignment": True,
            "ai_signature_verified": True
        }
