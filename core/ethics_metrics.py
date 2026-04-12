"""
ethics_metrics.py
Ethics Gap and H-VAR Computation Module for IGHS

This module implements:
- Ethics Gap calculation using multi-dimensional welfare indicators
- Human Volatility Index (H-VAR) computation
- PCA-based dimensional reduction
- Euclidean distance metrics
- Data integration from multiple sources
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
import os


class DimensionType(Enum):
    """Types of ethical dimensions monitored"""
    HEALTH_ACCESS = "HEALTH_ACCESS"
    ECONOMIC_EQUITY = "ECONOMIC_EQUITY"
    ENVIRONMENTAL_QUALITY = "ENVIRONMENTAL_QUALITY"
    SOCIAL_STABILITY = "SOCIAL_STABILITY"
    EDUCATION_ACCESS = "EDUCATION_ACCESS"
    NUTRITION_SECURITY = "NUTRITION_SECURITY"


@dataclass
class DimensionState:
    """Represents the state of a single ethical dimension"""
    dimension: DimensionType
    current_value: float  # 0.0 to 1.0 (normalized)
    ideal_value: float  # Target value (typically 1.0)
    weight: float  # Importance weight
    confidence: float  # Confidence in measurement (0.0 to 1.0)
    timestamp: str
    data_sources: List[str] = field(default_factory=list)
    
    def gap(self) -> float:
        """Calculate the gap from ideal state"""
        return self.ideal_value - self.current_value
    
    def weighted_gap_squared(self) -> float:
        """Calculate weighted squared gap for Euclidean distance"""
        return self.weight * (self.gap() ** 2)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension.value,
            "current_value": round(self.current_value, 6),
            "ideal_value": self.ideal_value,
            "weight": self.weight,
            "gap": round(self.gap(), 6),
            "confidence": round(self.confidence, 4),
            "timestamp": self.timestamp,
            "data_sources": self.data_sources
        }


@dataclass
class EthicsGapResult:
    """Result of Ethics Gap calculation"""
    timestamp: str
    total_gap: float
    dimensions: Dict[str, DimensionState]
    euclidean_distance: float
    weighted_average_gap: float
    worst_dimension: DimensionType
    best_dimension: DimensionType
    overall_confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "total_gap": round(self.total_gap, 6),
            "euclidean_distance": round(self.euclidean_distance, 6),
            "weighted_average_gap": round(self.weighted_average_gap, 6),
            "worst_dimension": self.worst_dimension.value,
            "best_dimension": self.best_dimension.value,
            "overall_confidence": round(self.overall_confidence, 4),
            "dimensions": {
                dim.value: state.to_dict() 
                for dim, state in self.dimensions.items()
            }
        }


@dataclass
class HVARResult:
    """Result of H-VAR calculation"""
    timestamp: str
    h_var: float
    volatility_factor: float
    current_std: float
    baseline_mean: float
    trend: str  # "stable", "increasing", "decreasing"
    crisis_indicators: List[str]
    requires_attention: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "h_var": round(self.h_var, 6),
            "volatility_factor": round(self.volatility_factor, 4),
            "current_std": round(self.current_std, 6),
            "baseline_mean": round(self.baseline_mean, 6),
            "trend": self.trend,
            "crisis_indicators": self.crisis_indicators,
            "requires_attention": self.requires_attention
        }


@dataclass
class DataSource:
    """Represents an external data source"""
    source_name: str
    source_type: str  # "satellite", "social_media", "economic", "health", "conflict"
    last_update: str
    reliability: float  # 0.0 to 1.0
    dimensions_covered: List[DimensionType]


class EthicsMetricsCalculator:
    """
    Calculator for Ethics Gap and H-VAR metrics
    
    Implements the core IGHS metrics computation with support for:
    - Multi-dimensional ethics gap calculation
    - Human volatility index computation
    - PCA-based analysis
    - Data integration from multiple sources
    """
    
    # Default weights for ethical dimensions
    DEFAULT_WEIGHTS = {
        DimensionType.HEALTH_ACCESS: 0.20,
        DimensionType.ECONOMIC_EQUITY: 0.18,
        DimensionType.ENVIRONMENTAL_QUALITY: 0.15,
        DimensionType.SOCIAL_STABILITY: 0.17,
        DimensionType.EDUCATION_ACCESS: 0.15,
        DimensionType.NUTRITION_SECURITY: 0.15
    }
    
    # H-VAR thresholds
    HVAR_STABLE_THRESHOLD = 0.05
    HVAR_WARNING_THRESHOLD = 0.08
    HVAR_CRITICAL_THRESHOLD = 0.10
    
    def __init__(self, log_path: str = "logs/ethics_metrics.log"):
        """Initialize the ethics metrics calculator"""
        self.log_path = log_path
        self.dimension_weights = self.DEFAULT_WEIGHTS.copy()
        self.historical_data: List[EthicsGapResult] = []
        self.hvar_history: List[HVARResult] = []
        self.data_sources: List[DataSource] = []
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def register_data_source(self, source: DataSource):
        """Register a new data source"""
        self.data_sources.append(source)
        self._log(f"Registered data source: {source.source_name} ({source.source_type})")
    
    def set_dimension_weight(self, dimension: DimensionType, weight: float):
        """
        Update the weight for a specific dimension
        
        Args:
            dimension: The dimension to update
            weight: New weight value (should sum to 1.0 across all dimensions)
        """
        if weight < 0 or weight > 1:
            raise ValueError("Weight must be between 0 and 1")
        
        self.dimension_weights[dimension] = weight
        
        # Normalize to ensure sum equals 1.0
        total = sum(self.dimension_weights.values())
        if total > 0:
            for dim in self.dimension_weights:
                self.dimension_weights[dim] /= total
    
    def calculate_ethics_gap(
        self,
        dimension_states: Dict[DimensionType, DimensionState]
    ) -> EthicsGapResult:
        """
        Calculate the Ethics Gap using Euclidean distance
        
        Formula: Ethics_Gap = √(Σᵢ wᵢ × (ideal_stateᵢ - current_stateᵢ)²)
        
        Args:
            dimension_states: Current state for each dimension
            
        Returns:
            EthicsGapResult with comprehensive gap analysis
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate weighted squared gaps
        weighted_squared_gaps = []
        confidences = []
        gaps_by_dimension = {}
        
        for dimension, state in dimension_states.items():
            weighted_sq_gap = state.weighted_gap_squared()
            weighted_squared_gaps.append(weighted_sq_gap)
            confidences.append(state.confidence)
            gaps_by_dimension[dimension] = state.gap()
        
        # Calculate Euclidean distance (total ethics gap)
        euclidean_distance = np.sqrt(np.sum(weighted_squared_gaps))
        
        # Calculate weighted average gap
        weighted_gaps = [
            state.weight * state.gap() 
            for state in dimension_states.values()
        ]
        weighted_average_gap = np.sum(weighted_gaps)
        
        # Identify best and worst dimensions
        worst_dimension = max(gaps_by_dimension.items(), key=lambda x: x[1])[0]
        best_dimension = min(gaps_by_dimension.items(), key=lambda x: x[1])[0]
        
        # Calculate overall confidence
        overall_confidence = np.mean(confidences)
        
        result = EthicsGapResult(
            timestamp=timestamp,
            total_gap=euclidean_distance,
            dimensions=dimension_states,
            euclidean_distance=euclidean_distance,
            weighted_average_gap=weighted_average_gap,
            worst_dimension=worst_dimension,
            best_dimension=best_dimension,
            overall_confidence=overall_confidence
        )
        
        # Store in history
        self.historical_data.append(result)
        
        # Keep history manageable
        if len(self.historical_data) > 1000:
            self.historical_data = self.historical_data[-1000:]
        
        self._log(f"Ethics Gap calculated: {euclidean_distance:.6f} "
                 f"(worst: {worst_dimension.value}, best: {best_dimension.value})")
        
        return result
    
    def calculate_hvar(
        self,
        recent_window: int = 30,
        baseline_window: int = 90
    ) -> Optional[HVARResult]:
        """
        Calculate Human Volatility Index (H-VAR)
        
        Formula: H-VAR = (σ_current / μ_baseline) × volatility_factor
        
        Args:
            recent_window: Number of recent data points to analyze
            baseline_window: Number of baseline data points for comparison
            
        Returns:
            HVARResult with volatility analysis or None if insufficient data
        """
        if len(self.historical_data) < recent_window:
            return None
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Get recent ethics gap values
        recent_gaps = [
            result.total_gap 
            for result in self.historical_data[-recent_window:]
        ]
        
        # Get baseline for comparison
        baseline_start = max(0, len(self.historical_data) - baseline_window)
        baseline_gaps = [
            result.total_gap 
            for result in self.historical_data[baseline_start:baseline_start + baseline_window]
        ]
        
        # Calculate statistics
        current_std = np.std(recent_gaps)
        baseline_mean = np.mean(baseline_gaps) if baseline_gaps else np.mean(recent_gaps)
        
        # Avoid division by zero
        if baseline_mean == 0:
            baseline_mean = 0.001
        
        # Calculate volatility factor based on crisis indicators
        volatility_factor = self._calculate_volatility_factor()
        
        # Calculate H-VAR
        h_var = (current_std / baseline_mean) * volatility_factor
        
        # Determine trend
        first_half = recent_gaps[:len(recent_gaps)//2]
        second_half = recent_gaps[len(recent_gaps)//2:]
        
        first_mean = np.mean(first_half)
        second_mean = np.mean(second_half)
        
        if abs(second_mean - first_mean) < current_std * 0.1:
            trend = "stable"
        elif second_mean > first_mean:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        # Identify crisis indicators
        crisis_indicators = self._identify_crisis_indicators(h_var)
        
        # Determine if attention is required
        requires_attention = (
            h_var > self.HVAR_WARNING_THRESHOLD or
            len(crisis_indicators) > 0 or
            trend == "increasing"
        )
        
        result = HVARResult(
            timestamp=timestamp,
            h_var=h_var,
            volatility_factor=volatility_factor,
            current_std=current_std,
            baseline_mean=baseline_mean,
            trend=trend,
            crisis_indicators=crisis_indicators,
            requires_attention=requires_attention
        )
        
        # Store in history
        self.hvar_history.append(result)
        
        if len(self.hvar_history) > 1000:
            self.hvar_history = self.hvar_history[-1000:]
        
        self._log(f"H-VAR calculated: {h_var:.6f} (trend: {trend}, "
                 f"attention: {requires_attention})")
        
        return result
    
    def _calculate_volatility_factor(self) -> float:
        """
        Calculate volatility factor based on recent trends
        
        Returns value between 0.8 and 1.5
        """
        if len(self.historical_data) < 10:
            return 1.0
        
        # Get recent dimension values
        recent_results = self.historical_data[-10:]
        
        # Count dimensions showing high variance
        high_variance_count = 0
        
        for dimension in DimensionType:
            values = []
            for result in recent_results:
                if dimension in result.dimensions:
                    values.append(result.dimensions[dimension].current_value)
            
            if len(values) >= 5:
                std = np.std(values)
                if std > 0.1:  # High variance threshold
                    high_variance_count += 1
        
        # Scale factor based on number of volatile dimensions
        factor = 1.0 + (high_variance_count * 0.1)
        
        # Cap between 0.8 and 1.5
        return max(0.8, min(1.5, factor))
    
    def _identify_crisis_indicators(self, h_var: float) -> List[str]:
        """Identify active crisis indicators"""
        indicators = []
        
        if h_var > self.HVAR_CRITICAL_THRESHOLD:
            indicators.append("CRITICAL_VOLATILITY")
        elif h_var > self.HVAR_WARNING_THRESHOLD:
            indicators.append("HIGH_VOLATILITY")
        
        # Check for rapid deterioration in key dimensions
        if len(self.historical_data) >= 5:
            recent = self.historical_data[-5:]
            
            for dimension in DimensionType:
                values = [
                    r.dimensions[dimension].current_value 
                    for r in recent 
                    if dimension in r.dimensions
                ]
                
                if len(values) >= 3:
                    # Check for consistent decline
                    declining = all(
                        values[i] > values[i+1] 
                        for i in range(len(values)-1)
                    )
                    
                    if declining and (values[0] - values[-1]) > 0.15:
                        indicators.append(f"DECLINING_{dimension.value}")
        
        return indicators
    
    def perform_pca_analysis(
        self,
        n_components: int = 3
    ) -> Dict[str, Any]:
        """
        Perform Principal Component Analysis on historical data
        
        Reduces multi-dimensional ethics data to key principal components
        
        Args:
            n_components: Number of principal components to extract
            
        Returns:
            Dictionary with PCA results and explained variance
        """
        if len(self.historical_data) < 10:
            return {
                "error": "Insufficient data for PCA analysis",
                "required": 10,
                "available": len(self.historical_data)
            }
        
        # Prepare data matrix
        data_matrix = []
        for result in self.historical_data[-100:]:  # Last 100 data points
            row = [
                result.dimensions[dim].current_value
                for dim in DimensionType
                if dim in result.dimensions
            ]
            if len(row) == len(DimensionType):
                data_matrix.append(row)
        
        if len(data_matrix) < 10:
            return {"error": "Insufficient complete data points"}
        
        # Convert to numpy array
        X = np.array(data_matrix)
        
        # Standardize the data
        X_mean = np.mean(X, axis=0)
        X_std = np.std(X, axis=0)
        X_std[X_std == 0] = 1  # Avoid division by zero
        X_standardized = (X - X_mean) / X_std
        
        # Compute covariance matrix
        cov_matrix = np.cov(X_standardized.T)
        
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Sort by eigenvalues (descending)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Calculate explained variance (use absolute eigenvalues to handle numerical issues)
        eigenvalues = np.abs(eigenvalues)
        total_variance = np.sum(eigenvalues)
        if total_variance > 0:
            explained_variance = eigenvalues / total_variance
        else:
            explained_variance = np.zeros_like(eigenvalues)
        
        # Get top n components
        top_components = eigenvectors[:, :n_components]
        
        # Project data onto principal components
        projected_data = X_standardized.dot(top_components)
        
        result = {
            "n_components": n_components,
            "explained_variance": explained_variance[:n_components].tolist(),
            "cumulative_variance": np.cumsum(explained_variance[:n_components]).tolist(),
            "component_loadings": {
                f"PC{i+1}": {
                    dim.value: float(top_components[j, i])
                    for j, dim in enumerate(DimensionType)
                }
                for i in range(n_components)
            },
            "data_points_analyzed": len(data_matrix)
        }
        
        self._log(f"PCA analysis completed: {n_components} components, "
                 f"{result['cumulative_variance'][-1]:.2%} variance explained")
        
        return result
    
    def get_intervention_priorities(self) -> List[Dict[str, Any]]:
        """
        Determine intervention priorities based on current metrics
        
        Returns list of dimensions ordered by priority
        """
        if not self.historical_data:
            return []
        
        latest_result = self.historical_data[-1]
        
        priorities = []
        for dimension, state in latest_result.dimensions.items():
            priority_score = (
                state.gap() * 0.6 +  # Gap contribution
                state.weight * 0.3 +  # Importance weight
                (1.0 - state.confidence) * 0.1  # Uncertainty factor
            )
            
            priorities.append({
                "dimension": dimension.value,
                "priority_score": round(priority_score, 4),
                "gap": round(state.gap(), 4),
                "current_value": round(state.current_value, 4),
                "confidence": round(state.confidence, 4),
                "recommended_action": self._get_recommended_action(dimension, state)
            })
        
        # Sort by priority score (descending)
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return priorities
    
    def _get_recommended_action(
        self,
        dimension: DimensionType,
        state: DimensionState
    ) -> str:
        """Generate recommended action for a dimension"""
        gap = state.gap()
        
        if gap < 0.1:
            return "MAINTAIN - Continue current interventions"
        elif gap < 0.3:
            return "ENHANCE - Scale up existing programs"
        elif gap < 0.5:
            return "URGENT - Deploy new interventions immediately"
        else:
            return "CRITICAL - Emergency response required"
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get comprehensive data for dashboard visualization
        
        Returns:
            Dashboard-ready data structure
        """
        if not self.historical_data:
            return {
                "error": "No data available",
                "message": "No ethics gap calculations have been performed yet"
            }
        
        latest_gap = self.historical_data[-1]
        latest_hvar = self.hvar_history[-1] if self.hvar_history else None
        
        # Get time series data
        gap_time_series = [
            {
                "timestamp": result.timestamp,
                "total_gap": result.total_gap,
                "weighted_average_gap": result.weighted_average_gap
            }
            for result in self.historical_data[-50:]
        ]
        
        hvar_time_series = [
            {
                "timestamp": result.timestamp,
                "h_var": result.h_var,
                "trend": result.trend
            }
            for result in self.hvar_history[-50:]
        ] if self.hvar_history else []
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_ethics_gap": latest_gap.to_dict(),
            "current_hvar": latest_hvar.to_dict() if latest_hvar else None,
            "intervention_priorities": self.get_intervention_priorities(),
            "time_series": {
                "ethics_gap": gap_time_series,
                "hvar": hvar_time_series
            },
            "pca_analysis": self.perform_pca_analysis(),
            "data_sources": [
                {
                    "name": source.source_name,
                    "type": source.source_type,
                    "reliability": source.reliability,
                    "last_update": source.last_update
                }
                for source in self.data_sources
            ]
        }
    
    def _log(self, message: str):
        """Log message to file"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except (OSError, IOError):
            pass


# Global calculator instance
_calculator_instance: Optional[EthicsMetricsCalculator] = None


def get_ethics_metrics_calculator() -> EthicsMetricsCalculator:
    """Get or create the global ethics metrics calculator instance"""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = EthicsMetricsCalculator()
    return _calculator_instance


if __name__ == "__main__":
    # Demo usage
    import random
    
    calculator = EthicsMetricsCalculator()
    
    print("🌍 Ethics Metrics Calculator Demo")
    print("=" * 60)
    
    # Register some data sources
    calculator.register_data_source(DataSource(
        source_name="WHO Health Statistics",
        source_type="health",
        last_update=datetime.now(timezone.utc).isoformat(),
        reliability=0.95,
        dimensions_covered=[DimensionType.HEALTH_ACCESS]
    ))
    
    calculator.register_data_source(DataSource(
        source_name="World Bank Economic Data",
        source_type="economic",
        last_update=datetime.now(timezone.utc).isoformat(),
        reliability=0.92,
        dimensions_covered=[DimensionType.ECONOMIC_EQUITY]
    ))
    
    # Simulate ethics gap calculations over time
    print("\n📊 Simulating 30 time periods...")
    for i in range(30):
        # Create dimension states with some random variation
        dimension_states = {
            DimensionType.HEALTH_ACCESS: DimensionState(
                dimension=DimensionType.HEALTH_ACCESS,
                current_value=0.65 + random.uniform(-0.05, 0.05),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.HEALTH_ACCESS],
                confidence=0.90,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["WHO Health Statistics"]
            ),
            DimensionType.ECONOMIC_EQUITY: DimensionState(
                dimension=DimensionType.ECONOMIC_EQUITY,
                current_value=0.55 + random.uniform(-0.08, 0.08),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.ECONOMIC_EQUITY],
                confidence=0.85,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["World Bank Economic Data"]
            ),
            DimensionType.ENVIRONMENTAL_QUALITY: DimensionState(
                dimension=DimensionType.ENVIRONMENTAL_QUALITY,
                current_value=0.70 + random.uniform(-0.06, 0.04),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.ENVIRONMENTAL_QUALITY],
                confidence=0.88,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["Satellite Environmental Data"]
            ),
            DimensionType.SOCIAL_STABILITY: DimensionState(
                dimension=DimensionType.SOCIAL_STABILITY,
                current_value=0.72 + random.uniform(-0.10, 0.05),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.SOCIAL_STABILITY],
                confidence=0.80,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["Conflict Database", "Social Media Sentiment"]
            ),
            DimensionType.EDUCATION_ACCESS: DimensionState(
                dimension=DimensionType.EDUCATION_ACCESS,
                current_value=0.68 + random.uniform(-0.04, 0.06),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.EDUCATION_ACCESS],
                confidence=0.92,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["UNESCO Statistics"]
            ),
            DimensionType.NUTRITION_SECURITY: DimensionState(
                dimension=DimensionType.NUTRITION_SECURITY,
                current_value=0.60 + random.uniform(-0.07, 0.07),
                ideal_value=1.0,
                weight=calculator.dimension_weights[DimensionType.NUTRITION_SECURITY],
                confidence=0.87,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=["FAO Food Security"]
            )
        }
        
        # Calculate ethics gap
        gap_result = calculator.calculate_ethics_gap(dimension_states)
        
        # Calculate H-VAR (after enough data)
        if i >= 10:
            hvar_result = calculator.calculate_hvar()
    
    # Get final results
    print("\n📈 Current Ethics Gap Status:")
    latest_gap = calculator.historical_data[-1]
    print(f"   Total Gap: {latest_gap.total_gap:.4f}")
    print(f"   Worst Dimension: {latest_gap.worst_dimension.value}")
    print(f"   Best Dimension: {latest_gap.best_dimension.value}")
    print(f"   Overall Confidence: {latest_gap.overall_confidence:.2%}")
    
    if calculator.hvar_history:
        print("\n📊 Current H-VAR Status:")
        latest_hvar = calculator.hvar_history[-1]
        print(f"   H-VAR: {latest_hvar.h_var:.4f}")
        print(f"   Trend: {latest_hvar.trend}")
        print(f"   Requires Attention: {latest_hvar.requires_attention}")
        if latest_hvar.crisis_indicators:
            print(f"   Crisis Indicators: {', '.join(latest_hvar.crisis_indicators)}")
    
    # Get intervention priorities
    print("\n🎯 Intervention Priorities:")
    priorities = calculator.get_intervention_priorities()
    for i, priority in enumerate(priorities[:3], 1):
        print(f"   {i}. {priority['dimension']}: "
              f"Score {priority['priority_score']:.4f} - "
              f"{priority['recommended_action']}")
    
    # Perform PCA analysis
    print("\n🔬 PCA Analysis:")
    pca_result = calculator.perform_pca_analysis()
    if "error" not in pca_result:
        print(f"   Components: {pca_result['n_components']}")
        print(f"   Variance Explained: {pca_result['cumulative_variance'][-1]:.2%}")
    
    print("\n✅ Demo complete!")
