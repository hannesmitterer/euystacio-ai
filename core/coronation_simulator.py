"""
coronation_simulator.py
Dry-Run Simulation Module for Coronation Workshop

This module provides:
- Dry-run simulations for Coronation Workshop scaling
- Stress tests for pre-coronation preparation
- Performance benchmarking and capacity planning
- Simulation insights and recommendations

Target: January 2026 Coronation Workshop
"""

import json
import os
import random
import statistics
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SimulationMode(Enum):
    """Types of simulation modes"""
    DRY_RUN = "DRY_RUN"
    STRESS_TEST = "STRESS_TEST"
    SCALING_TEST = "SCALING_TEST"
    FULL_REHEARSAL = "FULL_REHEARSAL"


class LoadLevel(Enum):
    """Load levels for stress testing"""
    MINIMAL = "MINIMAL"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    PEAK = "PEAK"
    EXTREME = "EXTREME"


class SimulationStatus(Enum):
    """Status of simulation run"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class SimulationMetrics:
    """Metrics collected during simulation"""
    response_time_ms: float
    throughput_ops: float
    error_rate: float
    cpu_utilization: float
    memory_utilization: float
    network_latency_ms: float
    concurrent_users: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "response_time_ms": self.response_time_ms,
            "throughput_ops": self.throughput_ops,
            "error_rate": self.error_rate,
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "network_latency_ms": self.network_latency_ms,
            "concurrent_users": self.concurrent_users
        }


@dataclass
class SimulationScenario:
    """Represents a simulation scenario"""
    scenario_id: str
    name: str
    description: str
    mode: SimulationMode
    load_level: LoadLevel
    duration_minutes: int
    target_users: int
    target_operations: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode.value,
            "load_level": self.load_level.value,
            "duration_minutes": self.duration_minutes,
            "target_users": self.target_users,
            "target_operations": self.target_operations
        }


@dataclass
class SimulationResult:
    """Result of a simulation run"""
    result_id: str
    scenario_id: str
    timestamp: str
    status: SimulationStatus
    duration_actual_ms: float
    metrics_summary: Dict[str, Any]
    bottlenecks: List[str]
    recommendations: List[str]
    passed_thresholds: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "scenario_id": self.scenario_id,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "duration_actual_ms": self.duration_actual_ms,
            "metrics_summary": self.metrics_summary,
            "bottlenecks": self.bottlenecks,
            "recommendations": self.recommendations,
            "passed_thresholds": self.passed_thresholds
        }


class CoronationSimulator:
    """
    Coronation Workshop Dry-Run Simulation System
    
    Provides comprehensive simulation capabilities for:
    - Scaling tests before January 2026 Coronation
    - Stress testing under various load conditions
    - Performance benchmarking and optimization
    """
    
    # Performance thresholds for Coronation Workshop
    THRESHOLDS = {
        "max_response_time_ms": 500,
        "min_throughput_ops": 1000,
        "max_error_rate": 0.01,
        "max_cpu_utilization": 0.80,
        "max_memory_utilization": 0.85,
        "max_network_latency_ms": 100
    }
    
    # Simulation bounds (configurable ceiling values for metrics)
    SIMULATION_BOUNDS = {
        "max_cpu_ceiling": 0.99,
        "max_memory_ceiling": 0.95
    }
    
    # Load multipliers for different levels
    LOAD_MULTIPLIERS = {
        LoadLevel.MINIMAL: 0.2,
        LoadLevel.NORMAL: 1.0,
        LoadLevel.HIGH: 2.5,
        LoadLevel.PEAK: 5.0,
        LoadLevel.EXTREME: 10.0
    }
    
    def __init__(self, log_path: str = "logs/coronation_simulator.log"):
        """Initialize the coronation simulator"""
        self.log_path = log_path
        self.scenarios: Dict[str, SimulationScenario] = {}
        self.results: List[SimulationResult] = []
        self.metrics_history: List[SimulationMetrics] = []
        self._ensure_log_directory()
        self._initialize_default_scenarios()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID"""
        return hashlib.sha256(
            f"{prefix}-{datetime.now(timezone.utc).isoformat()}-{random.random()}".encode()
        ).hexdigest()[:12].upper()
    
    def _initialize_default_scenarios(self):
        """Initialize default simulation scenarios"""
        scenarios = [
            SimulationScenario(
                scenario_id="SCEN-001",
                name="Baseline Performance",
                description="Establish baseline performance metrics under normal load",
                mode=SimulationMode.DRY_RUN,
                load_level=LoadLevel.NORMAL,
                duration_minutes=10,
                target_users=100,
                target_operations=10000
            ),
            SimulationScenario(
                scenario_id="SCEN-002",
                name="Peak Load Stress Test",
                description="Test system behavior under peak Coronation Day load",
                mode=SimulationMode.STRESS_TEST,
                load_level=LoadLevel.PEAK,
                duration_minutes=30,
                target_users=500,
                target_operations=50000
            ),
            SimulationScenario(
                scenario_id="SCEN-003",
                name="Horizontal Scaling Test",
                description="Verify horizontal scaling capabilities",
                mode=SimulationMode.SCALING_TEST,
                load_level=LoadLevel.HIGH,
                duration_minutes=20,
                target_users=250,
                target_operations=25000
            ),
            SimulationScenario(
                scenario_id="SCEN-004",
                name="Full Coronation Rehearsal",
                description="Complete rehearsal of Coronation Workshop ceremony",
                mode=SimulationMode.FULL_REHEARSAL,
                load_level=LoadLevel.PEAK,
                duration_minutes=60,
                target_users=1000,
                target_operations=100000
            ),
            SimulationScenario(
                scenario_id="SCEN-005",
                name="Extreme Load Test",
                description="Push system to limits to identify breaking points",
                mode=SimulationMode.STRESS_TEST,
                load_level=LoadLevel.EXTREME,
                duration_minutes=15,
                target_users=2000,
                target_operations=200000
            ),
        ]
        
        for scenario in scenarios:
            self.scenarios[scenario.scenario_id] = scenario
    
    def run_simulation(self, scenario_id: str) -> SimulationResult:
        """
        Run a simulation scenario
        
        Args:
            scenario_id: ID of the scenario to run
            
        Returns:
            SimulationResult with metrics and recommendations
        """
        if scenario_id not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_id}")
        
        scenario = self.scenarios[scenario_id]
        timestamp = datetime.now(timezone.utc).isoformat()
        result_id = self._generate_id("RES")
        
        self._log_event("SIMULATION_START", 
                       f"Starting {scenario.name} (ID: {scenario_id})")
        
        # Simulate the workload
        metrics = self._simulate_workload(scenario)
        
        # Analyze results
        analysis = self._analyze_metrics(metrics, scenario)
        
        # Calculate actual duration
        duration_actual_ms = scenario.duration_minutes * 60 * 1000
        
        result = SimulationResult(
            result_id=result_id,
            scenario_id=scenario_id,
            timestamp=timestamp,
            status=SimulationStatus.COMPLETED,
            duration_actual_ms=duration_actual_ms,
            metrics_summary=analysis["summary"],
            bottlenecks=analysis["bottlenecks"],
            recommendations=analysis["recommendations"],
            passed_thresholds=analysis["passed"]
        )
        
        self.results.append(result)
        
        self._log_event("SIMULATION_COMPLETE", 
                       f"Completed {scenario.name} - Passed: {result.passed_thresholds}")
        
        return result
    
    def _simulate_workload(self, scenario: SimulationScenario) -> List[SimulationMetrics]:
        """Simulate workload and collect metrics"""
        metrics_list = []
        load_multiplier = self.LOAD_MULTIPLIERS[scenario.load_level]
        
        # Generate simulated metrics for the duration
        samples = min(scenario.duration_minutes, 60)  # One sample per minute, max 60
        
        for i in range(samples):
            # Base metrics with some randomness
            base_response = 50 + (load_multiplier * 30)
            base_throughput = 2000 / load_multiplier
            base_cpu = 0.20 + (load_multiplier * 0.12)
            
            # Add realistic variation with configurable bounds
            cpu_ceiling = self.SIMULATION_BOUNDS["max_cpu_ceiling"]
            memory_ceiling = self.SIMULATION_BOUNDS["max_memory_ceiling"]
            
            metrics = SimulationMetrics(
                response_time_ms=base_response + random.uniform(-10, 50 * load_multiplier),
                throughput_ops=base_throughput + random.uniform(-200, 200),
                error_rate=0.001 * load_multiplier + random.uniform(0, 0.005 * load_multiplier),
                cpu_utilization=min(cpu_ceiling, base_cpu + random.uniform(-0.05, 0.15)),
                memory_utilization=min(memory_ceiling, 0.30 + (load_multiplier * 0.10) + random.uniform(-0.05, 0.10)),
                network_latency_ms=20 + (load_multiplier * 10) + random.uniform(-5, 20),
                concurrent_users=int(scenario.target_users * (0.8 + random.uniform(0, 0.4)))
            )
            
            metrics_list.append(metrics)
            self.metrics_history.append(metrics)
        
        return metrics_list
    
    def _analyze_metrics(self, metrics: List[SimulationMetrics], 
                          scenario: SimulationScenario) -> Dict[str, Any]:
        """Analyze simulation metrics"""
        if not metrics:
            return {"summary": {}, "bottlenecks": [], "recommendations": [], "passed": False}
        
        # Calculate summary statistics
        response_times = [m.response_time_ms for m in metrics]
        throughputs = [m.throughput_ops for m in metrics]
        error_rates = [m.error_rate for m in metrics]
        cpu_utils = [m.cpu_utilization for m in metrics]
        mem_utils = [m.memory_utilization for m in metrics]
        latencies = [m.network_latency_ms for m in metrics]
        
        summary = {
            "response_time": {
                "avg": round(statistics.mean(response_times), 2),
                "max": round(max(response_times), 2),
                "min": round(min(response_times), 2),
                "p95": round(sorted(response_times)[int(len(response_times) * 0.95)], 2) if len(response_times) > 1 else response_times[0]
            },
            "throughput": {
                "avg": round(statistics.mean(throughputs), 2),
                "max": round(max(throughputs), 2),
                "min": round(min(throughputs), 2)
            },
            "error_rate": {
                "avg": round(statistics.mean(error_rates), 6),
                "max": round(max(error_rates), 6)
            },
            "cpu_utilization": {
                "avg": round(statistics.mean(cpu_utils), 4),
                "max": round(max(cpu_utils), 4)
            },
            "memory_utilization": {
                "avg": round(statistics.mean(mem_utils), 4),
                "max": round(max(mem_utils), 4)
            },
            "network_latency": {
                "avg": round(statistics.mean(latencies), 2),
                "max": round(max(latencies), 2)
            },
            "samples": len(metrics),
            "scenario_mode": scenario.mode.value,
            "load_level": scenario.load_level.value
        }
        
        # Identify bottlenecks and check thresholds
        bottlenecks = []
        passed = True
        
        if summary["response_time"]["max"] > self.THRESHOLDS["max_response_time_ms"]:
            bottlenecks.append(f"Response time exceeded: {summary['response_time']['max']}ms > {self.THRESHOLDS['max_response_time_ms']}ms")
            passed = False
        
        if summary["throughput"]["min"] < self.THRESHOLDS["min_throughput_ops"]:
            bottlenecks.append(f"Throughput dropped below minimum: {summary['throughput']['min']} < {self.THRESHOLDS['min_throughput_ops']} ops/s")
            passed = False
        
        if summary["error_rate"]["max"] > self.THRESHOLDS["max_error_rate"]:
            bottlenecks.append(f"Error rate exceeded: {summary['error_rate']['max']:.4%} > {self.THRESHOLDS['max_error_rate']:.2%}")
            passed = False
        
        if summary["cpu_utilization"]["max"] > self.THRESHOLDS["max_cpu_utilization"]:
            bottlenecks.append(f"CPU utilization exceeded: {summary['cpu_utilization']['max']:.1%} > {self.THRESHOLDS['max_cpu_utilization']:.0%}")
            passed = False
        
        if summary["memory_utilization"]["max"] > self.THRESHOLDS["max_memory_utilization"]:
            bottlenecks.append(f"Memory utilization exceeded: {summary['memory_utilization']['max']:.1%} > {self.THRESHOLDS['max_memory_utilization']:.0%}")
            passed = False
        
        if summary["network_latency"]["max"] > self.THRESHOLDS["max_network_latency_ms"]:
            bottlenecks.append(f"Network latency exceeded: {summary['network_latency']['max']}ms > {self.THRESHOLDS['max_network_latency_ms']}ms")
            passed = False
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary, bottlenecks, scenario)
        
        return {
            "summary": summary,
            "bottlenecks": bottlenecks,
            "recommendations": recommendations,
            "passed": passed
        }
    
    def _generate_recommendations(self, summary: Dict[str, Any], 
                                   bottlenecks: List[str],
                                   scenario: SimulationScenario) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if not bottlenecks:
            recommendations.append(
                "✅ All performance thresholds met - system ready for Coronation Workshop"
            )
            return recommendations
        
        # Response time recommendations
        if summary["response_time"]["avg"] > self.THRESHOLDS["max_response_time_ms"] * 0.7:
            recommendations.append(
                "⚡ Consider implementing caching for frequently accessed data to reduce response times"
            )
        
        # CPU recommendations
        if summary["cpu_utilization"]["avg"] > 0.6:
            recommendations.append(
                "🖥️ High CPU utilization detected - consider horizontal scaling or code optimization"
            )
        
        # Memory recommendations
        if summary["memory_utilization"]["avg"] > 0.7:
            recommendations.append(
                "💾 Memory usage approaching limits - review memory allocation and potential leaks"
            )
        
        # Error rate recommendations
        if summary["error_rate"]["avg"] > 0.005:
            recommendations.append(
                "🔧 Error rate above acceptable levels - investigate error sources and add retry logic"
            )
        
        # Throughput recommendations
        if summary["throughput"]["avg"] < self.THRESHOLDS["min_throughput_ops"] * 1.5:
            recommendations.append(
                "📊 Throughput near minimum threshold - consider async processing and queue optimization"
            )
        
        # Network recommendations
        if summary["network_latency"]["avg"] > 50:
            recommendations.append(
                "🌐 Network latency contributing to delays - consider CDN deployment or regional replication"
            )
        
        # Add scaling recommendation for high load tests
        if scenario.load_level in [LoadLevel.PEAK, LoadLevel.EXTREME]:
            if bottlenecks:
                recommendations.append(
                    "🚀 For Coronation Day peak loads, implement auto-scaling with pre-warming"
                )
        
        # General best practices
        recommendations.append(
            "📋 Schedule weekly simulation runs leading up to January Coronation Workshop"
        )
        
        return recommendations
    
    def run_all_scenarios(self) -> Dict[str, Any]:
        """Run all default scenarios and compile results"""
        all_results = []
        
        for scenario_id in self.scenarios:
            result = self.run_simulation(scenario_id)
            all_results.append(result.to_dict())
        
        # Compile summary
        passed_count = len([r for r in all_results if r["passed_thresholds"]])
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_scenarios": len(all_results),
            "passed_scenarios": passed_count,
            "failed_scenarios": len(all_results) - passed_count,
            "overall_readiness": passed_count / len(all_results) if all_results else 0,
            "results": all_results,
            "coronation_ready": passed_count == len(all_results)
        }
    
    def get_capacity_planning(self) -> Dict[str, Any]:
        """Generate capacity planning recommendations for Coronation Workshop"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Analyze historical metrics
        if not self.metrics_history:
            return {
                "timestamp": timestamp,
                "status": "INSUFFICIENT_DATA",
                "message": "Run simulations to generate capacity planning data"
            }
        
        # Calculate peak resource needs
        max_cpu = max(m.cpu_utilization for m in self.metrics_history)
        max_mem = max(m.memory_utilization for m in self.metrics_history)
        max_users = max(m.concurrent_users for m in self.metrics_history)
        
        # Calculate recommended capacity with safety margin
        safety_margin = 1.5
        
        return {
            "timestamp": timestamp,
            "current_capacity": {
                "max_concurrent_users": max_users,
                "cpu_headroom": round(1 - max_cpu, 4),
                "memory_headroom": round(1 - max_mem, 4)
            },
            "coronation_workshop_target": {
                "expected_users": 1000,
                "peak_users": 2000,
                "target_date": "2026-01-10"
            },
            "recommended_capacity": {
                "compute_instances": max(3, int(2000 / max_users * safety_margin)),
                "cpu_allocation": f"{int(max_cpu * 100 * safety_margin)}%",
                "memory_allocation": f"{int(max_mem * 100 * safety_margin)}%",
                "load_balancers": 2,
                "cache_nodes": 3,
                "database_replicas": 2
            },
            "scaling_strategy": {
                "type": "Horizontal with Auto-scaling",
                "min_instances": 2,
                "max_instances": 10,
                "scale_up_threshold": "CPU > 70%",
                "scale_down_threshold": "CPU < 30%",
                "pre_warm_before_event": True
            },
            "estimated_cost_factor": round(safety_margin * (max_cpu + max_mem), 2)
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data formatted for dashboard visualization"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scenarios": [s.to_dict() for s in self.scenarios.values()],
            "recent_results": [r.to_dict() for r in self.results[-5:]],
            "capacity_planning": self.get_capacity_planning(),
            "thresholds": self.THRESHOLDS,
            "metrics_history_count": len(self.metrics_history),
            "simulation_stats": {
                "total_runs": len(self.results),
                "passed": len([r for r in self.results if r.passed_thresholds]),
                "failed": len([r for r in self.results if not r.passed_thresholds])
            }
        }
    
    def generate_markdown_report(self) -> str:
        """Generate comprehensive simulation report in Markdown"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        report = f"""# Coronation Workshop Simulation Report

**Generated:** {timestamp}  
**Target Event:** Coronation Workshop - January 10, 2026

---

## Executive Summary

"""
        
        if not self.results:
            report += "No simulation results available. Run simulations to generate report.\n"
            return report
        
        passed = len([r for r in self.results if r.passed_thresholds])
        total = len(self.results)
        readiness = passed / total if total > 0 else 0
        
        report += f"""| Metric | Value |
|--------|-------|
| Total Simulations | {total} |
| Passed | {passed} |
| Failed | {total - passed} |
| Readiness Score | **{readiness:.0%}** |

---

## Simulation Results

"""
        
        for result in self.results:
            status_emoji = "✅" if result.passed_thresholds else "❌"
            scenario = self.scenarios.get(result.scenario_id, None)
            name = scenario.name if scenario else result.scenario_id
            
            report += f"""### {status_emoji} {name}

| Metric | Value |
|--------|-------|
| Scenario ID | {result.scenario_id} |
| Status | {result.status.value} |
| Passed | {result.passed_thresholds} |

"""
            
            if result.metrics_summary:
                summary = result.metrics_summary
                report += f"""**Performance Metrics:**
- Response Time: {summary.get('response_time', {}).get('avg', 'N/A')}ms (avg), {summary.get('response_time', {}).get('max', 'N/A')}ms (max)
- Throughput: {summary.get('throughput', {}).get('avg', 'N/A')} ops/s
- Error Rate: {summary.get('error_rate', {}).get('avg', 0):.4%}
- CPU Utilization: {summary.get('cpu_utilization', {}).get('avg', 0):.1%}
- Memory Utilization: {summary.get('memory_utilization', {}).get('avg', 0):.1%}

"""
            
            if result.bottlenecks:
                report += "**Bottlenecks Identified:**\n"
                for bottleneck in result.bottlenecks:
                    report += f"- ⚠️ {bottleneck}\n"
                report += "\n"
            
            if result.recommendations:
                report += "**Recommendations:**\n"
                for rec in result.recommendations[:3]:
                    report += f"- {rec}\n"
                report += "\n"
            
            report += "---\n\n"
        
        # Add capacity planning section
        capacity = self.get_capacity_planning()
        if capacity.get("status") != "INSUFFICIENT_DATA":
            report += f"""## Capacity Planning for Coronation Workshop

### Target Metrics
- Expected Users: {capacity['coronation_workshop_target']['expected_users']}
- Peak Users: {capacity['coronation_workshop_target']['peak_users']}
- Target Date: {capacity['coronation_workshop_target']['target_date']}

### Recommended Infrastructure
| Resource | Recommendation |
|----------|---------------|
| Compute Instances | {capacity['recommended_capacity']['compute_instances']} |
| CPU Allocation | {capacity['recommended_capacity']['cpu_allocation']} |
| Memory Allocation | {capacity['recommended_capacity']['memory_allocation']} |
| Load Balancers | {capacity['recommended_capacity']['load_balancers']} |
| Cache Nodes | {capacity['recommended_capacity']['cache_nodes']} |
| Database Replicas | {capacity['recommended_capacity']['database_replicas']} |

### Scaling Strategy
- Type: {capacity['scaling_strategy']['type']}
- Scale Up: {capacity['scaling_strategy']['scale_up_threshold']}
- Scale Down: {capacity['scaling_strategy']['scale_down_threshold']}
- Pre-warm Before Event: {"Yes" if capacity['scaling_strategy']['pre_warm_before_event'] else "No"}

"""
        
        report += f"""---

## Performance Thresholds

| Metric | Threshold |
|--------|-----------|
| Max Response Time | {self.THRESHOLDS['max_response_time_ms']}ms |
| Min Throughput | {self.THRESHOLDS['min_throughput_ops']} ops/s |
| Max Error Rate | {self.THRESHOLDS['max_error_rate']:.2%} |
| Max CPU | {self.THRESHOLDS['max_cpu_utilization']:.0%} |
| Max Memory | {self.THRESHOLDS['max_memory_utilization']:.0%} |
| Max Network Latency | {self.THRESHOLDS['max_network_latency_ms']}ms |

---

*Report generated by Euystacio Coronation Simulator v1.0*  
*AI Signature: GitHub Copilot & Seed-bringer hannesmitterer*
"""
        
        return report
    
    def save_report(self, output_path: str = "reports/coronation_simulation_report.md") -> str:
        """Save report to file"""
        report = self.generate_markdown_report()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        return output_path
    
    def _log_event(self, event_type: str, message: str):
        """Log event to file"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


# Global instance
_simulator_instance: Optional[CoronationSimulator] = None


def get_coronation_simulator() -> CoronationSimulator:
    """Get or create the global coronation simulator"""
    global _simulator_instance
    if _simulator_instance is None:
        _simulator_instance = CoronationSimulator()
    return _simulator_instance


if __name__ == "__main__":
    # Demo usage
    simulator = CoronationSimulator()
    
    print("🎭 Coronation Workshop Simulator Demo")
    print("=" * 50)
    
    # Run baseline scenario
    print("\n🚀 Running baseline simulation...")
    result = simulator.run_simulation("SCEN-001")
    print(f"   Status: {result.status.value}")
    print(f"   Passed: {result.passed_thresholds}")
    
    # Run stress test
    print("\n⚡ Running stress test...")
    result2 = simulator.run_simulation("SCEN-002")
    print(f"   Status: {result2.status.value}")
    print(f"   Passed: {result2.passed_thresholds}")
    
    if result2.bottlenecks:
        print("   Bottlenecks:")
        for b in result2.bottlenecks[:3]:
            print(f"     - {b}")
    
    # Get capacity planning
    print("\n📊 Capacity Planning:")
    capacity = simulator.get_capacity_planning()
    if capacity.get("recommended_capacity"):
        print(f"   Compute Instances: {capacity['recommended_capacity']['compute_instances']}")
        print(f"   Scale Strategy: {capacity['scaling_strategy']['type']}")
    
    print("\n✅ Demo complete!")
