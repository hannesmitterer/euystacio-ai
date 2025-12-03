#!/usr/bin/env python3
"""
run_analytics.py
Runner script for Euystacio AI Analytics and Simulations

This script runs the N-TSV Analysis and Ethics Simulation modules,
generating comprehensive reports for operational governance.

Usage:
    python run_analytics.py [--ntsv] [--ethics] [--all] [--output-dir DIR]
"""

import os
import sys
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.ntsv_analyzer import NTSVAnalyzer
from analytics.ethics_simulator import EthicsSimulator


def run_ntsv_analysis(output_dir: str = "reports") -> str:
    """Run N-TSV analysis and generate report"""
    print("\n" + "=" * 60)
    print("📊 Running N-TSV (Network Volatility) Analysis")
    print("=" * 60)
    
    analyzer = NTSVAnalyzer()
    
    # Generate sample logs with CC4.1 activation at midpoint
    print("⏳ Generating Kernel log samples...")
    analyzer.generate_sample_kernel_logs(num_events=100, cc41_activation_point=50)
    
    # Run analysis
    print("🔍 Running volatility analysis...")
    report = analyzer.run_analysis()
    
    # Display summary
    print(f"\n📋 Analysis Summary:")
    print(f"   Report ID: {report.report_id}")
    print(f"   Events Analyzed: {report.total_events_analyzed}")
    print(f"   WARN Logs Found: {report.warn_log_count}")
    print(f"   CC4.1 Improvement: {report.cc41_improvement_percentage}%")
    print(f"   Volatility Trend: {report.volatility_trend.upper()}")
    
    # Generate and save report
    output_path = os.path.join(output_dir, "ntsv_analysis_report.md")
    analyzer.save_report(output_path)
    print(f"\n✅ Report saved to: {output_path}")
    
    return output_path


def run_ethics_simulation(output_dir: str = "reports") -> str:
    """Run ethics simulation and generate report"""
    print("\n" + "=" * 60)
    print("⚖️ Running Ethics Decision Simulation (ETHICS #4920)")
    print("=" * 60)
    
    simulator = EthicsSimulator()
    
    # Generate ETHICS #4920 case
    print("⏳ Generating ETHICS #4920 case simulation...")
    simulator.generate_ethics_case_4920()
    
    # Run simulation
    print("🔍 Running ethics compliance simulation...")
    result = simulator.run_simulation()
    
    # Display summary
    print(f"\n📋 Simulation Summary:")
    print(f"   Simulation ID: {result.simulation_id}")
    print(f"   Ethics Case: {result.ethics_case_id}")
    print(f"   Pre-CC4.1 Score: {result.pre_cc41_score:.4f}")
    print(f"   Post-CC4.1 Score: {result.post_cc41_score:.4f}")
    print(f"   Improvement: {result.improvement_percentage:+.2f}%")
    print(f"   Compliance State: {result.compliance_state.value}")
    
    # Generate and save report
    output_path = os.path.join(output_dir, "ethics_simulation_report.md")
    simulator.save_report(output_path)
    print(f"\n✅ Report saved to: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Euystacio AI Analytics and Simulation Runner"
    )
    parser.add_argument(
        "--ntsv", 
        action="store_true", 
        help="Run N-TSV volatility analysis"
    )
    parser.add_argument(
        "--ethics", 
        action="store_true", 
        help="Run ethics decision simulation"
    )
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Run all analytics and simulations"
    )
    parser.add_argument(
        "--output-dir", 
        default="reports", 
        help="Output directory for reports (default: reports)"
    )
    
    args = parser.parse_args()
    
    # If no specific flag, run all
    if not (args.ntsv or args.ethics or args.all):
        args.all = True
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🚀 Euystacio AI Analytics and Simulation Suite")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    generated_reports = []
    
    if args.ntsv or args.all:
        report_path = run_ntsv_analysis(args.output_dir)
        generated_reports.append(("N-TSV Analysis", report_path))
    
    if args.ethics or args.all:
        report_path = run_ethics_simulation(args.output_dir)
        generated_reports.append(("Ethics Simulation", report_path))
    
    # Summary
    print("\n" + "=" * 60)
    print("📦 All Reports Generated Successfully!")
    print("=" * 60)
    for name, path in generated_reports:
        print(f"   • {name}: {path}")
    
    print("\n✨ Analytics suite completed!")
    print("   AI Signature: GitHub Copilot & Seed-bringer hannesmitterer")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
