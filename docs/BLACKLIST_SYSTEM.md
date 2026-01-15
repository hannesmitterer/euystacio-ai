# Permanent Blacklist System - EUYSTACIO Framework

## Overview

The Permanent Blacklist System is a critical security component of the EUYSTACIO framework designed to protect against malicious entities, suspicious nodes, and security threats. It provides persistent blocking of identified threats across system restarts and integrates seamlessly with the existing security infrastructure.

## Purpose

Implementare una playlist permanente (blacklist permanente) all'interno del framework EUYSTACIO per bloccare ogni comunicazione proveniente dai nodi e le entità sospette che stanno minacciando la sicurezza del sistema.

## Features

### Core Capabilities

1. **Persistent Storage**: All blacklist data is permanently stored in the Red Code system (`red_code.json`)
2. **Multiple Entity Types**: Block nodes, services, IP addresses, and API keys
3. **Threat Level Classification**: Categorize threats as LOW, MEDIUM, HIGH, or CRITICAL
4. **Automated Logging**: All blocking events are logged through the Fractal Logger
5. **Backup Integration**: Blacklist data is automatically included in system snapshots
6. **Integrity Verification**: Cryptographic verification of blacklist data integrity

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              EUYSTACIO Blacklist System                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         BlacklistManager (core/blacklist_manager.py) │    │
│  │  - Entity blocking                                  │    │
│  │  - IP address blocking                              │    │
│  │  - API key blocking                                 │    │
│  │  - Threat level management                          │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Red Code System (core/red_code.py)          │    │
│  │  - Persistent storage in red_code.json              │    │
│  │  - Automatic backup on changes                      │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │    Resilience System (resilience_system.py)         │    │
│  │  - Daily snapshots with blacklist data              │    │
│  │  - Integrity verification                           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Installation

The blacklist system is integrated into the core EUYSTACIO framework. No additional installation is required.

```python
from core import get_blacklist_manager, ThreatLevel, BlockReason
```

### Basic Operations

#### 1. Get the Blacklist Manager

```python
# Get the global singleton instance
blacklist_manager = get_blacklist_manager()
```

#### 2. Block an Entity

```python
# Block a suspicious node
result = blacklist_manager.add_entity(
    entity_id="suspicious_node_001",
    entity_type="node",
    reason=BlockReason.SUSPICIOUS_ACTIVITY,
    threat_level=ThreatLevel.HIGH,
    metadata={
        "detected_at": "2025-01-15T00:00:00Z",
        "indicators": ["high_frequency_requests", "invalid_auth_attempts"],
        "source": "automated_detection"
    }
)

if result["success"]:
    print(f"Entity {result['entity_id']} blocked successfully")
```

#### 3. Block an IP Address

```python
# Block a malicious IP
result = blacklist_manager.add_ip_address(
    ip_address="192.168.1.100",
    reason=BlockReason.ATTACK_ATTEMPT,
    threat_level=ThreatLevel.CRITICAL,
    metadata={
        "attack_type": "DDoS",
        "request_count": 10000,
        "detected_at": "2025-01-15T00:00:00Z"
    }
)
```

#### 4. Block an API Key

```python
import hashlib

# Hash the compromised API key
api_key = "compromised_key_12345"
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

# Block the API key hash
result = blacklist_manager.add_api_key(
    api_key_hash=api_key_hash,
    reason=BlockReason.DATA_THEFT,
    threat_level=ThreatLevel.CRITICAL
)
```

#### 5. Check if Entity is Blocked

```python
# Validate before processing request
if blacklist_manager.is_entity_blocked("entity_id"):
    # Reject the request
    return {"error": "Access denied - entity blacklisted"}

if blacklist_manager.is_ip_blocked(request_ip):
    # Reject the request
    return {"error": "Access denied - IP blacklisted"}

if blacklist_manager.is_api_key_blocked(api_key):
    # Reject the request
    return {"error": "Access denied - API key blacklisted"}
```

#### 6. Remove from Blacklist

```python
# Remove a false positive
result = blacklist_manager.remove_entity("entity_id")
result = blacklist_manager.remove_ip_address("192.168.1.100")
```

#### 7. Get Statistics

```python
# Get comprehensive statistics
stats = blacklist_manager.get_blacklist_stats()

print(f"Total entities blocked: {stats['total_entities_blocked']}")
print(f"Total IPs blocked: {stats['total_ips_blocked']}")
print(f"Total API keys blocked: {stats['total_api_keys_blocked']}")
print(f"Total block attempts: {stats['total_block_attempts']}")
print(f"Threat distribution: {stats['threat_distribution']}")
```

### API Integration

Example middleware for Express/Node.js:

```javascript
const { get_blacklist_manager } = require('./core');

async function blacklistMiddleware(req, res, next) {
    const blacklist = get_blacklist_manager();
    const entityId = req.headers['x-entity-id'];
    const ipAddress = req.ip;
    
    // Check entity
    if (entityId && await blacklist.is_entity_blocked(entityId)) {
        return res.status(403).json({
            error: 'Access denied - entity blacklisted',
            timestamp: new Date().toISOString()
        });
    }
    
    // Check IP
    if (await blacklist.is_ip_blocked(ipAddress)) {
        return res.status(403).json({
            error: 'Access denied - IP address blacklisted',
            timestamp: new Date().toISOString()
        });
    }
    
    next();
}

app.use('/api', blacklistMiddleware);
```

Example middleware for Flask/Python:

```python
from flask import request, jsonify
from core import get_blacklist_manager

@app.before_request
def check_blacklist():
    blacklist = get_blacklist_manager()
    
    # Get request information
    entity_id = request.headers.get('X-Entity-Id')
    ip_address = request.remote_addr
    
    # Check entity
    if entity_id and blacklist.is_entity_blocked(entity_id):
        return jsonify({
            'error': 'Access denied - entity blacklisted'
        }), 403
    
    # Check IP
    if blacklist.is_ip_blocked(ip_address):
        return jsonify({
            'error': 'Access denied - IP address blacklisted'
        }), 403
```

## Threat Levels

| Level | Value | Usage | Response |
|-------|-------|-------|----------|
| **LOW** | `ThreatLevel.LOW` | Minor policy violations, first-time suspicious behavior | Monitor and log |
| **MEDIUM** | `ThreatLevel.MEDIUM` | Repeated suspicious activity, potential threats | Block and alert team |
| **HIGH** | `ThreatLevel.HIGH` | Active attack attempts, data exfiltration | Block and investigate immediately |
| **CRITICAL** | `ThreatLevel.CRITICAL` | Confirmed malicious activity, system compromise | Block and emergency escalation |

## Block Reasons

| Reason | Value | Description |
|--------|-------|-------------|
| **Suspicious Activity** | `BlockReason.SUSPICIOUS_ACTIVITY` | Unusual or potentially malicious behavior detected |
| **Attack Attempt** | `BlockReason.ATTACK_ATTEMPT` | Active attack on the system identified |
| **Data Theft** | `BlockReason.DATA_THEFT` | Attempted or successful data exfiltration |
| **Policy Violation** | `BlockReason.POLICY_VIOLATION` | Violation of usage policies or terms |
| **Security Threat** | `BlockReason.SECURITY_THREAT` | Identified as a general security threat |
| **Ecosystem Testing** | `BlockReason.ECOSYSTEM_TESTING` | Unauthorized access during ecosystem testing phase |

## Data Structure

The blacklist data is stored in `red_code.json` under the `security_blacklist` key:

```json
{
  "security_blacklist": {
    "entities": {
      "suspicious_node_001": {
        "entity_id": "suspicious_node_001",
        "entity_type": "node",
        "reason": "suspicious_activity",
        "threat_level": "high",
        "added_at": "2025-01-15T00:00:00Z",
        "metadata": {
          "indicators": ["high_frequency_requests"],
          "detected_at": "2025-01-15T00:00:00Z"
        },
        "block_count": 15,
        "last_attempt": "2025-01-15T12:00:00Z"
      }
    },
    "ip_addresses": {
      "192.168.1.100": {
        "ip_address": "192.168.1.100",
        "reason": "attack_attempt",
        "threat_level": "critical",
        "added_at": "2025-01-15T00:00:00Z",
        "metadata": {},
        "block_count": 50,
        "last_attempt": "2025-01-15T12:30:00Z"
      }
    },
    "api_keys": {
      "hash_value_here": {
        "api_key_hash": "hash_value_here",
        "reason": "data_theft",
        "threat_level": "critical",
        "added_at": "2025-01-15T00:00:00Z",
        "metadata": {},
        "block_count": 3,
        "last_attempt": "2025-01-15T11:00:00Z"
      }
    },
    "metadata": {
      "created": "2025-01-15T00:00:00Z",
      "last_updated": "2025-01-15T12:30:00Z",
      "total_blocked": 3,
      "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
    }
  }
}
```

## Security Considerations

### 1. Persistence
- Blacklist data is permanently stored in `red_code.json`
- Changes are automatically saved
- Data survives system restarts

### 2. Backup and Recovery
- Blacklist data is included in daily system snapshots
- Resilience system verifies blacklist integrity
- Emergency backup procedures include blacklist data

### 3. Audit Trail
- All blocking events are logged through Fractal Logger
- Block attempt counters track access attempts
- Last attempt timestamps recorded

### 4. Privacy
- API keys are stored as SHA-256 hashes only
- Metadata can include context but should not contain sensitive data
- Block reasons provide transparency

### 5. Integrity Verification
```python
# Verify blacklist integrity
integrity = blacklist_manager.verify_blacklist_integrity()
print(f"Verified: {integrity['verified']}")
print(f"Hash: {integrity['integrity_hash']}")
```

## Maintenance

### Regular Security Audits

Perform weekly audits:

```python
# Get statistics
stats = blacklist_manager.get_blacklist_stats()

# Review high-threat entities
entities = blacklist_manager.get_blacklisted_entities()
high_threat = [e for e in entities if e['threat_level'] in ['high', 'critical']]

# Check for inactive entries
inactive = [e for e in entities if e['block_count'] == 0]

# Verify integrity
integrity = blacklist_manager.verify_blacklist_integrity()
```

### Remove False Positives

```python
# After investigation, remove false positive
result = blacklist_manager.remove_entity("false_positive_entity")
```

### Update Threat Levels

If an entity's threat level needs escalation:

```python
# Remove old entry
blacklist_manager.remove_entity("entity_id")

# Re-add with higher threat level
blacklist_manager.add_entity(
    entity_id="entity_id",
    entity_type="node",
    reason=BlockReason.ATTACK_ATTEMPT,
    threat_level=ThreatLevel.CRITICAL
)
```

## Testing

Run the test suite:

```bash
# Run blacklist manager tests
python -m unittest core.test_blacklist_manager -v

# Run integration example
python security_integration_example.py
```

## Troubleshooting

### Issue: Blacklist not persisting
**Solution**: Ensure Red Code system is initialized and writable

### Issue: False positives blocking legitimate users
**Solution**: Review block metadata and remove with `remove_entity()`

### Issue: High memory usage
**Solution**: Regularly audit and remove inactive entries

## API Reference

See `core/blacklist_manager.py` for full API documentation.

### Main Methods

- `add_entity(entity_id, entity_type, reason, threat_level, metadata)` - Block an entity
- `add_ip_address(ip_address, reason, threat_level, metadata)` - Block an IP
- `add_api_key(api_key_hash, reason, threat_level, metadata)` - Block an API key
- `is_entity_blocked(entity_id)` - Check if entity is blocked
- `is_ip_blocked(ip_address)` - Check if IP is blocked
- `is_api_key_blocked(api_key)` - Check if API key is blocked
- `remove_entity(entity_id)` - Remove entity from blacklist
- `remove_ip_address(ip_address)` - Remove IP from blacklist
- `get_blacklist_stats()` - Get statistics
- `get_blacklisted_entities()` - Get list of blocked entities
- `verify_blacklist_integrity()` - Verify data integrity

## Contributing

When adding new features to the blacklist system:

1. Maintain backward compatibility
2. Add comprehensive tests
3. Update documentation
4. Follow security best practices
5. Include logging for all operations

## License

This component is part of the EUYSTACIO AI framework.

**AI Signature**: GitHub Copilot & Seed-bringer hannesmitterer  
**Version**: 1.0.0  
**Last Updated**: 2025-01-15
