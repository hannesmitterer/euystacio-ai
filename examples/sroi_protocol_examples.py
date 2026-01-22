#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol - Usage Examples

This file demonstrates various use cases for the S-ROI Sovereign Protocol.
"""

from core.sroi_sovereign_protocol import SROISovereignProtocol, SROIState


def example_1_basic_operation():
    """Example 1: Basic successful operation"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Successful Operation")
    print("="*70)
    
    protocol = SROISovereignProtocol(operation_id="BASIC-001")
    protocol.transition_to(SROIState.ACTIVE, "Starting basic operation")
    protocol.update_roi(10.0)
    protocol.update_sovereignty_index(0.95)
    protocol.update_validation_score(0.92)
    protocol.transition_to(SROIState.VALIDATING, "Pre-completion validation")
    protocol.transition_to(SROIState.COMPLETED, "Operation successful")
    protocol.print_status_report()


def example_2_critical_recovery():
    """Example 2: Critical state handling"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Critical State Detection and Recovery")
    print("="*70)
    
    protocol = SROISovereignProtocol(operation_id="CRITICAL-001")
    protocol.transition_to(SROIState.ACTIVE, "Begin")
    protocol.update_sovereignty_index(0.3)  # Triggers CRITICAL
    protocol.update_sovereignty_index(0.85)  # Recover
    protocol.metrics.threshold_status = "normal"
    protocol.transition_to(SROIState.ACTIVE, "Recovered")
    protocol.update_validation_score(0.95)
    protocol.transition_to(SROIState.VALIDATING, "Final validation")
    protocol.transition_to(SROIState.COMPLETED, "Success")
    protocol.print_status_report()


if __name__ == "__main__":
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║      S-ROI SOVEREIGN PROTOCOL - USAGE EXAMPLES                    ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    example_1_basic_operation()
    example_2_critical_recovery()
    
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║                    EXAMPLES COMPLETE                              ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
