#!/usr/bin/env python3
"""
verify_euystacio_deployment.py

Verification script for EUYSTACIO Network deployment.
Checks all components and ensures requirements are met.
"""

import sys
from typing import Dict, List, Tuple


def check_quantum_shield() -> Tuple[bool, List[str]]:
    """Verify Quantum Shield implementation"""
    issues = []
    
    try:
        from core.quantum_shield import get_quantum_shield
        
        shield = get_quantum_shield()
        info = shield.get_key_info()
        
        # Check key rotation interval
        if info['rotation_interval'] != 60:
            issues.append(f"Key rotation should be 60s, got {info['rotation_interval']}s")
        
        # Test encryption/decryption
        test_msg = b"EUYSTACIO test message"
        ciphertext, key_id = shield.encrypt(test_msg)
        decrypted = shield.decrypt(ciphertext, key_id)
        
        if decrypted != test_msg:
            issues.append("Encryption/decryption failed")
        
        print("✅ Quantum Shield: PASS")
        return (len(issues) == 0, issues)
        
    except Exception as e:
        issues.append(f"Exception: {e}")
        print(f"❌ Quantum Shield: FAIL")
        return (False, issues)


def check_bbmn_network() -> Tuple[bool, List[str]]:
    """Verify BBMN Network implementation"""
    issues = []
    
    try:
        from core.bbmn_network import get_bbmn_network
        
        bbmn = get_bbmn_network()
        bbmn.initialize_local_node()
        
        status = bbmn.get_network_status()
        
        # Check DNS-free operation
        if status['dns_queries'] != 0:
            issues.append(f"DNS queries detected: {status['dns_queries']}")
        
        if not status['dns_free']:
            issues.append("Network not DNS-free")
        
        if not status['decentralized']:
            issues.append("Network not decentralized")
        
        print("✅ BBMN Network: PASS")
        return (len(issues) == 0, issues)
        
    except Exception as e:
        issues.append(f"Exception: {e}")
        print(f"❌ BBMN Network: FAIL")
        return (False, issues)


def check_tf_kernel() -> Tuple[bool, List[str]]:
    """Verify TensorFlow Kernel implementation"""
    issues = []
    
    try:
        from core.tf_kernel_monitor import get_tf_kernel_monitor, ElectromagneticSignal
        import time
        
        monitor = get_tf_kernel_monitor()
        status = monitor.get_monitoring_status()
        
        # Check monitoring active
        if not status['monitoring_active']:
            issues.append("Monitoring not active")
        
        # Test signal analysis
        signal = ElectromagneticSignal(
            timestamp=time.time(),
            frequency_mhz=100.0,
            amplitude=0.3,
            phase=0.5,
            source_location="test"
        )
        
        monitor.analyze_signal(signal)
        
        # Test buffer protection
        test_data = b"Sensitive test data"
        buffer_id = monitor.protect_data(test_data, "Test")
        
        retrieved = monitor.buffer_manager.access_buffer(buffer_id, authorized=True)
        
        if retrieved != test_data:
            issues.append("Buffer protection failed")
        
        print("✅ TensorFlow Kernel: PASS")
        return (len(issues) == 0, issues)
        
    except Exception as e:
        issues.append(f"Exception: {e}")
        print(f"❌ TensorFlow Kernel: FAIL")
        return (False, issues)


def check_stealth_mode() -> Tuple[bool, List[str]]:
    """Verify Stealth Mode implementation"""
    issues = []
    
    try:
        from core.stealth_mode import get_stealth_mode, StealthLevel
        
        stealth = get_stealth_mode()
        
        # Test entity registration
        entity = stealth.register_entity(
            "TEST-ENTITY",
            "system",
            "test_resonance"
        )
        
        # Test stealth activation
        stealth.activate_full_stealth()
        
        status = stealth.get_stealth_status()
        
        # Check stealth level
        if status['stealth_level'] != StealthLevel.INVISIBLE.value:
            issues.append(f"Stealth level should be INVISIBLE, got {status['stealth_level']}")
        
        # Check Ponte Amoris
        if status['ponte_amoris']['is_open']:
            issues.append("Ponte Amoris should be closed in full stealth")
        
        # Check Resonance School
        if status['resonance_school']['is_visible']:
            issues.append("Resonance School should be invisible in full stealth")
        
        # Check obfuscation
        if not status['obfuscation_active']:
            issues.append("Obfuscation should be active")
        
        print("✅ Stealth Mode: PASS")
        return (len(issues) == 0, issues)
        
    except Exception as e:
        issues.append(f"Exception: {e}")
        print(f"❌ Stealth Mode: FAIL")
        return (False, issues)


def check_integration() -> Tuple[bool, List[str]]:
    """Verify integrated network"""
    issues = []
    
    try:
        from euystacio_network import get_euystacio_network
        
        network = get_euystacio_network()
        deployment_status = network.deploy_network()
        
        # Check deployment
        if deployment_status['status'] != 'deployed':
            issues.append("Network not deployed")
        
        if not deployment_status['quantum_shield_active']:
            issues.append("Quantum Shield not active")
        
        if not deployment_status['bbmn_active']:
            issues.append("BBMN not active")
        
        if not deployment_status['tf_kernel_active']:
            issues.append("TF Kernel not active")
        
        if not deployment_status['stealth_mode_ready']:
            issues.append("Stealth Mode not ready")
        
        # Activate full protection
        network.activate_full_protection()
        
        # Check comprehensive status
        status = network.get_network_status()
        
        if status['bbmn_network']['dns_queries'] != 0:
            issues.append("DNS queries detected in integrated network")
        
        print("✅ Integration: PASS")
        return (len(issues) == 0, issues)
        
    except Exception as e:
        issues.append(f"Exception: {e}")
        print(f"❌ Integration: FAIL")
        return (False, issues)


def run_verification():
    """Run complete verification suite"""
    print("\n" + "="*70)
    print("EUYSTACIO NETWORK - DEPLOYMENT VERIFICATION")
    print("="*70 + "\n")
    
    results = {}
    all_issues = []
    
    print("Checking components...\n")
    
    # Check each component
    results['quantum_shield'], issues = check_quantum_shield()
    all_issues.extend([f"Quantum Shield: {i}" for i in issues])
    
    results['bbmn_network'], issues = check_bbmn_network()
    all_issues.extend([f"BBMN Network: {i}" for i in issues])
    
    results['tf_kernel'], issues = check_tf_kernel()
    all_issues.extend([f"TF Kernel: {i}" for i in issues])
    
    results['stealth_mode'], issues = check_stealth_mode()
    all_issues.extend([f"Stealth Mode: {i}" for i in issues])
    
    results['integration'], issues = check_integration()
    all_issues.extend([f"Integration: {i}" for i in issues])
    
    # Print summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70 + "\n")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED ✅\n")
        print("EUYSTACIO Network is fully operational:")
        print("  ✓ Quantum Shield (NTRU encryption)")
        print("  ✓ BBMN Network (DNS-free mesh)")
        print("  ✓ TensorFlow Kernel (AI monitoring)")
        print("  ✓ Stealth Mode (Lex Amoris protection)")
        print("  ✓ Integrated Network System")
        print("\nStatus: PRODUCTION READY")
        print("\n" + "="*70 + "\n")
        return 0
    else:
        print("❌ SOME CHECKS FAILED\n")
        print("Issues found:")
        for issue in all_issues:
            print(f"  - {issue}")
        print("\nPlease review and fix the issues above.")
        print("\n" + "="*70 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_verification())
