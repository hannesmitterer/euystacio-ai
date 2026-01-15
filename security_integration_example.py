"""
security_integration_example.py
Example integration of the Blacklist Manager with EUYSTACIO security systems

This demonstrates how to integrate the blacklist manager into existing
security workflows and API endpoints.
"""

from typing import Dict, Any, List, Optional
from core import get_blacklist_manager, ThreatLevel, BlockReason
from datetime import datetime, timezone


def validate_incoming_request(entity_id: str, ip_address: str, api_key: str = None):
    """
    Validate an incoming request against the blacklist
    
    Args:
        entity_id: Identifier of the requesting entity
        ip_address: IP address of the request
        api_key: Optional API key
    
    Returns:
        Tuple of (is_valid, reason)
    """
    blacklist_manager = get_blacklist_manager()
    
    # Check entity
    if blacklist_manager.is_entity_blocked(entity_id):
        return False, f"Entity {entity_id} is blacklisted"
    
    # Check IP address
    if blacklist_manager.is_ip_blocked(ip_address):
        return False, f"IP address {ip_address} is blacklisted"
    
    # Check API key if provided
    if api_key and blacklist_manager.is_api_key_blocked(api_key):
        return False, "API key is blacklisted"
    
    return True, "Request validated"


def detect_and_block_suspicious_activity(entity_id: str, activity_data: dict):
    """
    Detect suspicious activity and automatically add to blacklist
    
    Args:
        entity_id: Identifier of the entity
        activity_data: Data about the suspicious activity
    
    Returns:
        Dictionary with detection results
    """
    blacklist_manager = get_blacklist_manager()
    
    # Example detection rules (implement actual detection logic)
    suspicious_indicators = []
    threat_level = ThreatLevel.LOW
    
    # Check for high-frequency requests (potential DoS)
    if activity_data.get("request_count", 0) > 1000:
        suspicious_indicators.append("high_frequency_requests")
        threat_level = ThreatLevel.HIGH
    
    # Check for invalid authentication attempts
    if activity_data.get("failed_auth_attempts", 0) > 10:
        suspicious_indicators.append("multiple_failed_auth")
        threat_level = ThreatLevel.MEDIUM
    
    # Check for data exfiltration patterns
    if activity_data.get("data_volume_mb", 0) > 1000:
        suspicious_indicators.append("high_data_volume")
        threat_level = ThreatLevel.HIGH
    
    # Check for ecosystem testing state violations
    if activity_data.get("ecosystem_state") == "TESTING" and activity_data.get("unauthorized_access") is not None:
        suspicious_indicators.append("ecosystem_testing_violation")
        threat_level = ThreatLevel.CRITICAL
    
    # If suspicious activity detected, add to blacklist
    if suspicious_indicators:
        result = blacklist_manager.add_entity(
            entity_id=entity_id,
            entity_type=activity_data.get("entity_type", "unknown"),
            reason=BlockReason.SUSPICIOUS_ACTIVITY,
            threat_level=threat_level,
            metadata={
                "indicators": suspicious_indicators,
                "activity_data": activity_data,
                "detected_at": datetime.now(timezone.utc).isoformat()
            }
        )
        
        return {
            "suspicious": True,
            "blocked": result["success"],
            "threat_level": threat_level,
            "indicators": suspicious_indicators
        }
    
    return {
        "suspicious": False,
        "blocked": False
    }


def setup_initial_blacklist():
    """
    Setup initial blacklist entries for known threats
    
    This should be called during system initialization to populate
    the blacklist with known malicious entities.
    """
    blacklist_manager = get_blacklist_manager()
    
    # Example: Block known malicious entities from ecosystem testing
    # These would be actual identified threats in production
    known_threats = [
        {
            "entity_id": "malicious_node_001",
            "entity_type": "node",
            "reason": BlockReason.SECURITY_THREAT,
            "threat_level": ThreatLevel.CRITICAL,
            "metadata": {
                "description": "Known malicious node from previous incidents",
                "first_detected": "2025-01-10T00:00:00Z"
            }
        },
        {
            "entity_id": "suspicious_service_002",
            "entity_type": "service",
            "reason": BlockReason.ECOSYSTEM_TESTING,
            "threat_level": ThreatLevel.HIGH,
            "metadata": {
                "description": "Unauthorized access during ecosystem testing phase",
                "source": "upstream_ip_repository"
            }
        }
    ]
    
    results = []
    for threat in known_threats:
        result = blacklist_manager.add_entity(
            entity_id=threat["entity_id"],
            entity_type=threat["entity_type"],
            reason=threat["reason"],
            threat_level=threat["threat_level"],
            metadata=threat.get("metadata")
        )
        results.append(result)
    
    return results


def get_security_dashboard_data():
    """
    Get blacklist data for security dashboard
    
    Returns:
        Dictionary with security metrics
    """
    blacklist_manager = get_blacklist_manager()
    
    stats = blacklist_manager.get_blacklist_stats()
    entities = blacklist_manager.get_blacklisted_entities()
    ips = blacklist_manager.get_blacklisted_ips()
    integrity = blacklist_manager.verify_blacklist_integrity()
    
    # Get recent high-threat entities
    high_threat_entities = [
        entity for entity in entities
        if entity.get("threat_level") in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
    ]
    
    # Sort by most recent
    high_threat_entities.sort(key=lambda x: x.get("added_at", ""), reverse=True)
    
    return {
        "statistics": stats,
        "high_threat_entities": high_threat_entities[:10],  # Top 10
        "total_ips_blocked": len(ips),
        "integrity_verified": integrity["verified"],
        "integrity_hash": integrity["integrity_hash"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def handle_api_request_with_blacklist_check(request_data):
    """
    Example API request handler with blacklist validation
    
    Args:
        request_data: Dictionary containing request information
    
    Returns:
        Response data or error
    """
    entity_id = request_data.get("entity_id")
    ip_address = request_data.get("ip_address")
    api_key = request_data.get("api_key")
    
    # Validate against blacklist
    is_valid, reason = validate_incoming_request(entity_id, ip_address, api_key)
    
    if not is_valid:
        return {
            "status": "blocked",
            "message": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Process the request (implement actual logic here)
    return {
        "status": "success",
        "message": "Request processed",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def periodic_security_audit():
    """
    Perform periodic security audit of blacklist
    
    This should be scheduled to run regularly (e.g., daily)
    to review and maintain the blacklist.
    """
    blacklist_manager = get_blacklist_manager()
    
    stats = blacklist_manager.get_blacklist_stats()
    entities = blacklist_manager.get_blacklisted_entities()
    
    audit_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_entities": stats["total_entities_blocked"],
        "total_ips": stats["total_ips_blocked"],
        "total_api_keys": stats["total_api_keys_blocked"],
        "total_block_attempts": stats["total_block_attempts"],
        "threat_distribution": stats["threat_distribution"],
        "recommendations": []
    }
    
    # Analyze threat distribution
    critical_count = stats["threat_distribution"].get(ThreatLevel.CRITICAL, 0)
    if critical_count > 10:
        audit_report["recommendations"].append(
            "High number of critical threats detected. Review security measures."
        )
    
    # Check for inactive entities (no recent block attempts)
    inactive_entities = [
        entity for entity in entities
        if entity.get("block_count", 0) == 0
    ]
    
    if len(inactive_entities) > len(entities) * 0.5:
        audit_report["recommendations"].append(
            f"More than 50% of blacklisted entities have no block attempts. "
            f"Consider reviewing {len(inactive_entities)} entries for removal."
        )
    
    # Verify integrity
    integrity = blacklist_manager.verify_blacklist_integrity()
    audit_report["integrity_verified"] = integrity["verified"]
    audit_report["integrity_hash"] = integrity["integrity_hash"]
    
    return audit_report


# Example usage
if __name__ == "__main__":
    print("EUYSTACIO Blacklist Manager - Security Integration Example")
    print("=" * 60)
    
    # Initialize blacklist with known threats
    print("\n1. Setting up initial blacklist...")
    results = setup_initial_blacklist()
    for result in results:
        print(f"   - {result['message']}")
    
    # Get security dashboard data
    print("\n2. Security Dashboard Data:")
    dashboard_data = get_security_dashboard_data()
    print(f"   Total entities blocked: {dashboard_data['statistics']['total_entities_blocked']}")
    print(f"   Total IPs blocked: {dashboard_data['statistics']['total_ips_blocked']}")
    print(f"   High-threat entities: {len(dashboard_data['high_threat_entities'])}")
    
    # Test request validation
    print("\n3. Testing request validation...")
    test_request = {
        "entity_id": "normal_user",
        "ip_address": "192.168.1.1"
    }
    response = handle_api_request_with_blacklist_check(test_request)
    print(f"   Response: {response['status']} - {response['message']}")
    
    # Test suspicious activity detection
    print("\n4. Testing suspicious activity detection...")
    suspicious_activity = {
        "entity_id": "suspicious_bot",
        "entity_type": "bot",
        "request_count": 1500,
        "failed_auth_attempts": 15
    }
    detection_result = detect_and_block_suspicious_activity(
        "suspicious_bot",
        suspicious_activity
    )
    print(f"   Suspicious: {detection_result['suspicious']}")
    print(f"   Blocked: {detection_result['blocked']}")
    if detection_result['suspicious']:
        print(f"   Threat level: {detection_result['threat_level']}")
        print(f"   Indicators: {', '.join(detection_result['indicators'])}")
    
    # Perform security audit
    print("\n5. Performing security audit...")
    audit = periodic_security_audit()
    print(f"   Total block attempts: {audit['total_block_attempts']}")
    print(f"   Integrity verified: {audit['integrity_verified']}")
    if audit["recommendations"]:
        print("   Recommendations:")
        for rec in audit["recommendations"]:
            print(f"     - {rec}")
    
    print("\n" + "=" * 60)
    print("Security integration example completed.")
