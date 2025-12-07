"""
quantum_optimization.py
Quantum-Inspired Optimization Module for IGHS

This module implements:
- QAOA-inspired optimization for intervention prioritization
- Ethical constraint checking
- Leverage point identification
- Multi-objective optimization with ethics enforcement
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json


class InterventionType(Enum):
    """Types of health/welfare interventions"""
    HEALTHCARE_INFRASTRUCTURE = "HEALTHCARE_INFRASTRUCTURE"
    EDUCATION_SYSTEMS = "EDUCATION_SYSTEMS"
    WATER_SANITATION = "WATER_SANITATION"
    AGRICULTURAL_SUPPORT = "AGRICULTURAL_SUPPORT"
    ECONOMIC_EMPOWERMENT = "ECONOMIC_EMPOWERMENT"
    SOCIAL_SERVICES = "SOCIAL_SERVICES"
    ENVIRONMENTAL_RESTORATION = "ENVIRONMENTAL_RESTORATION"


class EthicalConstraintType(Enum):
    """Types of ethical constraints"""
    NO_FORCED_RELOCATION = "NO_FORCED_RELOCATION"
    NO_PROPERTY_ELIMINATION = "NO_PROPERTY_ELIMINATION"
    NO_COERCION = "NO_COERCION"
    LOCAL_AUTONOMY = "LOCAL_AUTONOMY"
    TRANSPARENT_ENGAGEMENT = "TRANSPARENT_ENGAGEMENT"
    CULTURAL_RESPECT = "CULTURAL_RESPECT"
    ENVIRONMENTAL_PROTECTION = "ENVIRONMENTAL_PROTECTION"


@dataclass
class Intervention:
    """Represents a potential intervention"""
    intervention_id: str
    intervention_type: InterventionType
    target_dimension: str
    estimated_impact: float  # 0.0 to 1.0
    cost: float
    implementation_time: int  # days
    leverage_score: float  # Higher = more impact per cost
    region: str
    population_affected: int
    ethical_compliance: Dict[EthicalConstraintType, bool] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    
    def is_ethically_compliant(self) -> bool:
        """Check if intervention meets all ethical constraints"""
        return all(self.ethical_compliance.values())
    
    def cost_effectiveness(self) -> float:
        """Calculate cost-effectiveness ratio"""
        return self.estimated_impact / self.cost if self.cost > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "intervention_id": self.intervention_id,
            "intervention_type": self.intervention_type.value,
            "target_dimension": self.target_dimension,
            "estimated_impact": round(self.estimated_impact, 4),
            "cost": round(self.cost, 2),
            "implementation_time": self.implementation_time,
            "leverage_score": round(self.leverage_score, 4),
            "region": self.region,
            "population_affected": self.population_affected,
            "ethical_compliance": {
                constraint.value: compliant
                for constraint, compliant in self.ethical_compliance.items()
            },
            "is_compliant": self.is_ethically_compliant(),
            "cost_effectiveness": round(self.cost_effectiveness(), 6)
        }


@dataclass
class OptimizationConstraints:
    """Constraints for optimization problem"""
    max_budget: float
    max_time: int  # days
    min_ethical_compliance: float  # 0.0 to 1.0 (typically 1.0)
    required_constraints: List[EthicalConstraintType]
    regional_limits: Dict[str, int] = field(default_factory=dict)
    intervention_type_limits: Dict[InterventionType, int] = field(default_factory=dict)


@dataclass
class OptimizationResult:
    """Result of optimization"""
    timestamp: str
    selected_interventions: List[Intervention]
    total_cost: float
    total_impact: float
    total_leverage: float
    ethics_gap_reduction: float
    hvar_reduction: float
    overall_score: float
    ethical_compliance: bool
    constraints_satisfied: bool
    optimization_iterations: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "selected_interventions": [i.to_dict() for i in self.selected_interventions],
            "total_cost": round(self.total_cost, 2),
            "total_impact": round(self.total_impact, 4),
            "total_leverage": round(self.total_leverage, 4),
            "ethics_gap_reduction": round(self.ethics_gap_reduction, 4),
            "hvar_reduction": round(self.hvar_reduction, 4),
            "overall_score": round(self.overall_score, 4),
            "ethical_compliance": self.ethical_compliance,
            "constraints_satisfied": self.constraints_satisfied,
            "optimization_iterations": self.optimization_iterations,
            "num_interventions": len(self.selected_interventions)
        }


class QuantumInspiredOptimizer:
    """
    Quantum-Inspired Optimization for Intervention Selection
    
    Uses QAOA-inspired approach to find optimal intervention combinations
    that maximize ethics gap reduction while respecting ethical constraints
    """
    
    def __init__(
        self,
        alpha: float = 0.6,  # Weight for ethics gap
        beta: float = 0.3,   # Weight for H-VAR reduction
        gamma: float = 0.1   # Weight for cost efficiency
    ):
        """
        Initialize the optimizer
        
        Args:
            alpha: Weight for ethics gap reduction (highest priority)
            beta: Weight for volatility reduction
            gamma: Weight for cost efficiency
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # Normalize weights
        total = alpha + beta + gamma
        self.alpha /= total
        self.beta /= total
        self.gamma /= total
        
        self.optimization_history: List[OptimizationResult] = []
    
    def optimize(
        self,
        available_interventions: List[Intervention],
        constraints: OptimizationConstraints,
        current_ethics_gap: float,
        current_hvar: float,
        max_iterations: int = 100
    ) -> OptimizationResult:
        """
        Find optimal intervention combination using quantum-inspired approach
        
        Args:
            available_interventions: List of possible interventions
            constraints: Optimization constraints
            current_ethics_gap: Current ethics gap value
            current_hvar: Current H-VAR value
            max_iterations: Maximum optimization iterations
            
        Returns:
            OptimizationResult with selected interventions
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Filter for ethically compliant interventions only
        compliant_interventions = [
            intervention for intervention in available_interventions
            if self._check_ethical_compliance(intervention, constraints)
        ]
        
        if not compliant_interventions:
            # Return empty result if no compliant interventions
            return OptimizationResult(
                timestamp=timestamp,
                selected_interventions=[],
                total_cost=0.0,
                total_impact=0.0,
                total_leverage=0.0,
                ethics_gap_reduction=0.0,
                hvar_reduction=0.0,
                overall_score=0.0,
                ethical_compliance=True,
                constraints_satisfied=False,
                optimization_iterations=0
            )
        
        # Run quantum-inspired optimization
        best_solution = self._qaoa_inspired_search(
            compliant_interventions,
            constraints,
            current_ethics_gap,
            current_hvar,
            max_iterations
        )
        
        # Calculate metrics for best solution
        total_cost = sum(i.cost for i in best_solution)
        total_impact = sum(i.estimated_impact for i in best_solution)
        total_leverage = sum(i.leverage_score for i in best_solution)
        
        # Estimate ethics gap and H-VAR reduction
        ethics_gap_reduction = self._estimate_ethics_gap_reduction(
            best_solution,
            current_ethics_gap
        )
        
        hvar_reduction = self._estimate_hvar_reduction(
            best_solution,
            current_hvar
        )
        
        # Calculate overall optimization score
        overall_score = self._calculate_cost_function(
            best_solution,
            current_ethics_gap,
            current_hvar,
            ethics_gap_reduction,
            hvar_reduction
        )
        
        # Verify constraints
        ethical_compliance = all(i.is_ethically_compliant() for i in best_solution)
        constraints_satisfied = self._verify_constraints(best_solution, constraints)
        
        result = OptimizationResult(
            timestamp=timestamp,
            selected_interventions=best_solution,
            total_cost=total_cost,
            total_impact=total_impact,
            total_leverage=total_leverage,
            ethics_gap_reduction=ethics_gap_reduction,
            hvar_reduction=hvar_reduction,
            overall_score=overall_score,
            ethical_compliance=ethical_compliance,
            constraints_satisfied=constraints_satisfied,
            optimization_iterations=max_iterations
        )
        
        self.optimization_history.append(result)
        
        return result
    
    def _check_ethical_compliance(
        self,
        intervention: Intervention,
        constraints: OptimizationConstraints
    ) -> bool:
        """
        Verify intervention meets all ethical constraints
        
        This is a HARD constraint - interventions that violate ethics
        are automatically excluded from consideration
        """
        # Check if intervention has all required constraints defined
        for required_constraint in constraints.required_constraints:
            if required_constraint not in intervention.ethical_compliance:
                return False
            if not intervention.ethical_compliance[required_constraint]:
                return False
        
        # Overall ethical compliance check
        if not intervention.is_ethically_compliant():
            return False
        
        return True
    
    def _qaoa_inspired_search(
        self,
        interventions: List[Intervention],
        constraints: OptimizationConstraints,
        current_ethics_gap: float,
        current_hvar: float,
        max_iterations: int
    ) -> List[Intervention]:
        """
        QAOA-inspired heuristic search for optimal intervention set
        
        Uses simulated annealing-like approach with quantum-inspired transitions
        """
        # Initialize with greedy solution
        current_solution = self._greedy_initialization(interventions, constraints)
        current_score = self._calculate_cost_function_for_solution(
            current_solution,
            current_ethics_gap,
            current_hvar
        )
        
        best_solution = current_solution[:]
        best_score = current_score
        
        # Temperature for simulated annealing
        temperature = 1.0
        cooling_rate = 0.95
        
        for iteration in range(max_iterations):
            # Generate neighbor solution (quantum-inspired transition)
            neighbor_solution = self._generate_neighbor(
                current_solution,
                interventions,
                constraints
            )
            
            if neighbor_solution is None:
                continue
            
            neighbor_score = self._calculate_cost_function_for_solution(
                neighbor_solution,
                current_ethics_gap,
                current_hvar
            )
            
            # Accept better solutions always, worse solutions probabilistically
            score_delta = neighbor_score - current_score
            
            if score_delta > 0 or np.random.random() < np.exp(score_delta / temperature):
                current_solution = neighbor_solution
                current_score = neighbor_score
                
                # Update best if improved
                if current_score > best_score:
                    best_solution = current_solution[:]
                    best_score = current_score
            
            # Cool down temperature
            temperature *= cooling_rate
        
        return best_solution
    
    def _greedy_initialization(
        self,
        interventions: List[Intervention],
        constraints: OptimizationConstraints
    ) -> List[Intervention]:
        """Initialize with greedy high-leverage interventions"""
        # Sort by leverage score (descending)
        sorted_interventions = sorted(
            interventions,
            key=lambda x: x.leverage_score,
            reverse=True
        )
        
        selected = []
        total_cost = 0.0
        
        for intervention in sorted_interventions:
            new_cost = total_cost + intervention.cost
            
            if new_cost <= constraints.max_budget:
                # Check other constraints
                if self._can_add_intervention(intervention, selected, constraints):
                    selected.append(intervention)
                    total_cost = new_cost
        
        return selected
    
    def _generate_neighbor(
        self,
        current_solution: List[Intervention],
        all_interventions: List[Intervention],
        constraints: OptimizationConstraints
    ) -> Optional[List[Intervention]]:
        """Generate neighbor solution through mutation"""
        if not all_interventions:
            return None
        
        neighbor = current_solution[:]
        
        # Random mutation: add, remove, or swap
        mutation_type = np.random.choice(['add', 'remove', 'swap'])
        
        if mutation_type == 'add' and len(neighbor) < len(all_interventions):
            # Try to add a new intervention
            available = [i for i in all_interventions if i not in neighbor]
            if available:
                candidate = np.random.choice(available)
                test_solution = neighbor + [candidate]
                
                if self._verify_constraints(test_solution, constraints):
                    return test_solution
        
        elif mutation_type == 'remove' and len(neighbor) > 0:
            # Remove a random intervention
            idx = np.random.randint(len(neighbor))
            return neighbor[:idx] + neighbor[idx+1:]
        
        elif mutation_type == 'swap' and len(neighbor) > 0:
            # Swap one intervention for another
            idx = np.random.randint(len(neighbor))
            available = [i for i in all_interventions if i not in neighbor]
            
            if available:
                candidate = np.random.choice(available)
                test_solution = neighbor[:idx] + [candidate] + neighbor[idx+1:]
                
                if self._verify_constraints(test_solution, constraints):
                    return test_solution
        
        return None
    
    def _can_add_intervention(
        self,
        intervention: Intervention,
        current_selected: List[Intervention],
        constraints: OptimizationConstraints
    ) -> bool:
        """Check if intervention can be added to current selection"""
        test_solution = current_selected + [intervention]
        return self._verify_constraints(test_solution, constraints)
    
    def _verify_constraints(
        self,
        solution: List[Intervention],
        constraints: OptimizationConstraints
    ) -> bool:
        """Verify solution satisfies all constraints"""
        # Budget constraint
        total_cost = sum(i.cost for i in solution)
        if total_cost > constraints.max_budget:
            return False
        
        # Time constraint
        max_time = max([i.implementation_time for i in solution], default=0)
        if max_time > constraints.max_time:
            return False
        
        # Regional limits
        if constraints.regional_limits:
            region_counts = {}
            for intervention in solution:
                region = intervention.region
                region_counts[region] = region_counts.get(region, 0) + 1
                
                if region in constraints.regional_limits:
                    if region_counts[region] > constraints.regional_limits[region]:
                        return False
        
        # Intervention type limits
        if constraints.intervention_type_limits:
            type_counts = {}
            for intervention in solution:
                itype = intervention.intervention_type
                type_counts[itype] = type_counts.get(itype, 0) + 1
                
                if itype in constraints.intervention_type_limits:
                    if type_counts[itype] > constraints.intervention_type_limits[itype]:
                        return False
        
        return True
    
    def _calculate_cost_function_for_solution(
        self,
        solution: List[Intervention],
        current_ethics_gap: float,
        current_hvar: float
    ) -> float:
        """Calculate optimization score for a solution"""
        if not solution:
            return 0.0
        
        # Estimate reductions
        ethics_gap_reduction = self._estimate_ethics_gap_reduction(
            solution,
            current_ethics_gap
        )
        hvar_reduction = self._estimate_hvar_reduction(solution, current_hvar)
        
        return self._calculate_cost_function(
            solution,
            current_ethics_gap,
            current_hvar,
            ethics_gap_reduction,
            hvar_reduction
        )
    
    def _calculate_cost_function(
        self,
        solution: List[Intervention],
        current_ethics_gap: float,
        current_hvar: float,
        ethics_gap_reduction: float,
        hvar_reduction: float
    ) -> float:
        """
        Calculate overall cost function value
        
        C(interventions) = α × Ethics_Gap_Reduction + 
                           β × H-VAR_Reduction + 
                           γ × Cost_Efficiency
        """
        if not solution:
            return 0.0
        
        # Normalize ethics gap reduction
        normalized_ethics = ethics_gap_reduction / current_ethics_gap if current_ethics_gap > 0 else 0
        
        # Normalize H-VAR reduction
        normalized_hvar = hvar_reduction / current_hvar if current_hvar > 0 else 0
        
        # Calculate cost efficiency (impact per dollar)
        total_impact = sum(i.estimated_impact for i in solution)
        total_cost = sum(i.cost for i in solution)
        cost_efficiency = total_impact / total_cost if total_cost > 0 else 0
        
        # Combined score (to maximize)
        score = (
            self.alpha * normalized_ethics +
            self.beta * normalized_hvar +
            self.gamma * cost_efficiency
        )
        
        return score
    
    def _estimate_ethics_gap_reduction(
        self,
        interventions: List[Intervention],
        current_gap: float
    ) -> float:
        """Estimate how much interventions will reduce ethics gap"""
        # Sum weighted impacts
        total_impact = sum(i.estimated_impact * i.leverage_score for i in interventions)
        
        # Scale to gap reduction (with diminishing returns)
        reduction = current_gap * (1 - np.exp(-total_impact * 0.5))
        
        return reduction
    
    def _estimate_hvar_reduction(
        self,
        interventions: List[Intervention],
        current_hvar: float
    ) -> float:
        """Estimate how much interventions will reduce H-VAR"""
        # Interventions reduce volatility through stabilization
        stabilization_factor = sum(
            i.leverage_score * 0.1 for i in interventions
        )
        
        reduction = current_hvar * (1 - np.exp(-stabilization_factor))
        
        return reduction
    
    def identify_leverage_points(
        self,
        interventions: List[Intervention],
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Identify high-leverage interventions
        
        Args:
            interventions: List of available interventions
            top_n: Number of top leverage points to return
            
        Returns:
            List of top leverage interventions with analysis
        """
        # Calculate leverage metrics
        leverage_analysis = []
        
        for intervention in interventions:
            if not intervention.is_ethically_compliant():
                continue  # Skip non-compliant interventions
            
            leverage_metrics = {
                "intervention": intervention.to_dict(),
                "leverage_score": intervention.leverage_score,
                "cost_effectiveness": intervention.cost_effectiveness(),
                "impact_per_day": intervention.estimated_impact / intervention.implementation_time 
                                  if intervention.implementation_time > 0 else 0,
                "population_reach": intervention.population_affected,
                "ethical_compliance": intervention.is_ethically_compliant()
            }
            
            leverage_analysis.append(leverage_metrics)
        
        # Sort by leverage score
        leverage_analysis.sort(key=lambda x: x["leverage_score"], reverse=True)
        
        return leverage_analysis[:top_n]
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get summary of optimization history"""
        if not self.optimization_history:
            return {"error": "No optimizations performed yet"}
        
        return {
            "total_optimizations": len(self.optimization_history),
            "latest_optimization": self.optimization_history[-1].to_dict(),
            "average_ethics_gap_reduction": np.mean([
                r.ethics_gap_reduction for r in self.optimization_history
            ]),
            "average_hvar_reduction": np.mean([
                r.hvar_reduction for r in self.optimization_history
            ]),
            "total_interventions_selected": sum(
                len(r.selected_interventions) for r in self.optimization_history
            ),
            "ethical_compliance_rate": sum(
                1 for r in self.optimization_history if r.ethical_compliance
            ) / len(self.optimization_history)
        }


if __name__ == "__main__":
    # Demo usage
    print("⚛️ Quantum-Inspired Optimizer Demo")
    print("=" * 60)
    
    # Create optimizer
    optimizer = QuantumInspiredOptimizer(alpha=0.6, beta=0.3, gamma=0.1)
    
    # Create sample interventions
    interventions = [
        Intervention(
            intervention_id="INT-001",
            intervention_type=InterventionType.HEALTHCARE_INFRASTRUCTURE,
            target_dimension="HEALTH_ACCESS",
            estimated_impact=0.25,
            cost=500000,
            implementation_time=180,
            leverage_score=0.85,
            region="Region-A",
            population_affected=50000,
            ethical_compliance={
                EthicalConstraintType.NO_FORCED_RELOCATION: True,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                EthicalConstraintType.NO_COERCION: True,
                EthicalConstraintType.LOCAL_AUTONOMY: True,
                EthicalConstraintType.TRANSPARENT_ENGAGEMENT: True,
                EthicalConstraintType.CULTURAL_RESPECT: True,
                EthicalConstraintType.ENVIRONMENTAL_PROTECTION: True
            }
        ),
        Intervention(
            intervention_id="INT-002",
            intervention_type=InterventionType.EDUCATION_SYSTEMS,
            target_dimension="EDUCATION_ACCESS",
            estimated_impact=0.30,
            cost=300000,
            implementation_time=120,
            leverage_score=0.92,
            region="Region-B",
            population_affected=75000,
            ethical_compliance={
                EthicalConstraintType.NO_FORCED_RELOCATION: True,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                EthicalConstraintType.NO_COERCION: True,
                EthicalConstraintType.LOCAL_AUTONOMY: True,
                EthicalConstraintType.TRANSPARENT_ENGAGEMENT: True,
                EthicalConstraintType.CULTURAL_RESPECT: True,
                EthicalConstraintType.ENVIRONMENTAL_PROTECTION: True
            }
        ),
        Intervention(
            intervention_id="INT-003",
            intervention_type=InterventionType.WATER_SANITATION,
            target_dimension="ENVIRONMENTAL_QUALITY",
            estimated_impact=0.20,
            cost=400000,
            implementation_time=90,
            leverage_score=0.78,
            region="Region-A",
            population_affected=60000,
            ethical_compliance={
                EthicalConstraintType.NO_FORCED_RELOCATION: True,
                EthicalConstraintType.NO_PROPERTY_ELIMINATION: True,
                EthicalConstraintType.NO_COERCION: True,
                EthicalConstraintType.LOCAL_AUTONOMY: True,
                EthicalConstraintType.TRANSPARENT_ENGAGEMENT: True,
                EthicalConstraintType.CULTURAL_RESPECT: True,
                EthicalConstraintType.ENVIRONMENTAL_PROTECTION: True
            }
        )
    ]
    
    # Define constraints
    constraints = OptimizationConstraints(
        max_budget=1000000,
        max_time=200,
        min_ethical_compliance=1.0,
        required_constraints=[
            EthicalConstraintType.NO_FORCED_RELOCATION,
            EthicalConstraintType.NO_PROPERTY_ELIMINATION,
            EthicalConstraintType.NO_COERCION,
            EthicalConstraintType.LOCAL_AUTONOMY
        ]
    )
    
    # Run optimization
    print("\n🔍 Running optimization...")
    result = optimizer.optimize(
        available_interventions=interventions,
        constraints=constraints,
        current_ethics_gap=0.45,
        current_hvar=0.08,
        max_iterations=50
    )
    
    print(f"\n✅ Optimization Complete!")
    print(f"   Selected Interventions: {len(result.selected_interventions)}")
    print(f"   Total Cost: ${result.total_cost:,.2f}")
    print(f"   Total Impact: {result.total_impact:.4f}")
    print(f"   Ethics Gap Reduction: {result.ethics_gap_reduction:.4f}")
    print(f"   H-VAR Reduction: {result.hvar_reduction:.4f}")
    print(f"   Ethical Compliance: {result.ethical_compliance}")
    print(f"   Constraints Satisfied: {result.constraints_satisfied}")
    
    # Identify leverage points
    print("\n🎯 Top Leverage Points:")
    leverage_points = optimizer.identify_leverage_points(interventions, top_n=3)
    for i, lp in enumerate(leverage_points, 1):
        print(f"   {i}. {lp['intervention']['intervention_id']}: "
              f"Leverage={lp['leverage_score']:.4f}, "
              f"Cost-Effectiveness={lp['cost_effectiveness']:.6f}")
    
    print("\n✅ Demo complete!")
