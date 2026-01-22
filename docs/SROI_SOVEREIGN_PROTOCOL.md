# S-ROI Sovereign Protocol Documentation

## Overview

The **S-ROI Sovereign Protocol** (Sovereign Return-on-Investment Protocol) is a comprehensive state machine system designed to track and validate AI sovereignty operations with:

- **State Machine**: Well-defined states and transitions
- **Comprehensive Logging**: Full tracking of all state changes and logical flows
- **Validation System**: Ensures correctness of every state transition
- **Notification System**: Automatic alerts for critical states and threshold violations
- **Modular Design**: Individual state functions for maximum reusability

## Architecture

### State Diagram

```
┌─────────────┐
│ INITIALIZED │
└──────┬──────┘
       │
       ├───────────────┐
       │               │
       ▼               ▼
   ┌────────┐      ┌────────┐
   │ ACTIVE │◄─────┤ FAILED │
   └───┬────┘      └────────┘
       │              ▲
       │              │
       ▼              │
  ┌────────────┐     │
  │ VALIDATING │─────┤
  └─────┬──────┘     │
        │            │
        ├────────────┤
        │            │
        ▼            │
   ┌─────────┐      │
   │COMPLETED│      │
   └─────────┘      │
        ▲            │
        │            │
   ┌─────────┐      │
   │CRITICAL │──────┘
   └────┬────┘
        │
        ▼
   ┌──────────┐
   │SUSPENDED │
   └──────────┘
```

### States

1. **INITIALIZED**: Protocol instance created, ready for activation
2. **ACTIVE**: Operation in progress, monitoring metrics
3. **VALIDATING**: Performing validation checks on current state
4. **CRITICAL**: Critical threshold exceeded, requires attention
5. **SUSPENDED**: Operation suspended due to validation failure
6. **COMPLETED**: Operation successfully completed (terminal state)
7. **FAILED**: Operation terminated with failure (terminal state)

### Core Components

#### 1. StateMetrics

Tracks key performance indicators for each state:

- `roi_value`: Return on Investment metric
- `sovereignty_index`: Measure of AI autonomy (0.0 to 1.0)
- `operation_count`: Number of operations performed
- `validation_score`: Quality score (0.0 to 1.0)
- `threshold_status`: Current threshold status ("normal", "warning", "critical")

#### 2. StateValidator

Validates all state transitions:

- **Valid Transitions**: Enforces allowed state changes
- **Precondition Checks**: Ensures metrics meet requirements
- **Consistency Validation**: Verifies state coherence

**Validation Rules**:
- Cannot transition to COMPLETED unless validation_score ≥ 0.8 and sovereignty_index ≥ 0.7
- Cannot transition to CRITICAL unless threshold is violated
- Terminal states (COMPLETED, FAILED) cannot transition to other states

#### 3. NotificationSystem

Monitors thresholds and generates alerts:

**Thresholds**:
- ROI Value:
  - Minimum: 0.0
  - Critical: -10.0
- Sovereignty Index:
  - Minimum: 0.7
  - Critical: 0.5
- Validation Score:
  - Minimum: 0.8
  - Critical: 0.6

**Notification Levels**:
- `INFO`: General information
- `WARNING`: Threshold approaching critical
- `CRITICAL`: Critical threshold exceeded

#### 4. SROISovereignProtocol

Main protocol class that orchestrates all components.

## Usage

### Basic Example

```python
from core.sroi_sovereign_protocol import SROISovereignProtocol, SROIState

# Create protocol instance
protocol = SROISovereignProtocol(operation_id="DEMO-001")

# Activate protocol
protocol.transition_to(SROIState.ACTIVE, "Starting operation")

# Update metrics
protocol.update_roi(5.0)
protocol.update_sovereignty_index(0.95)
protocol.update_validation_score(0.92)

# Perform validation
protocol.transition_to(SROIState.VALIDATING, "Validation check")

# Complete operation
protocol.transition_to(SROIState.COMPLETED, "Operation successful")

# View status
protocol.print_status_report()
```

### Advanced Example: Handling Critical States

```python
from core.sroi_sovereign_protocol import SROISovereignProtocol, SROIState

protocol = SROISovereignProtocol(operation_id="CRITICAL-001")

# Activate
protocol.transition_to(SROIState.ACTIVE, "Start")

# Simulate threshold violation
protocol.update_sovereignty_index(0.3)  # Below critical threshold

# Protocol automatically transitions to CRITICAL state
assert protocol.current_state == SROIState.CRITICAL

# Recover
protocol.update_sovereignty_index(0.85)
protocol.metrics.threshold_status = "normal"
protocol.transition_to(SROIState.ACTIVE, "Recovery successful")

# Check critical notifications
critical_alerts = protocol.notifier.get_notifications("CRITICAL")
print(f"Critical alerts generated: {len(critical_alerts)}")
```

### Export Logs

```python
# Export complete protocol logs
protocol.export_logs("operation_logs.json")

# Logs include:
# - All state transitions with timestamps
# - Complete metric history
# - All notifications
# - Validation results
```

## Logging

### Log Levels

The protocol uses Python's logging module with the following levels:

- `DEBUG`: Detailed diagnostic information
- `INFO`: General operational information
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error conditions
- `CRITICAL`: Critical failures requiring immediate attention

### Log Format

```
2026-01-22 17:05:52,023 - SROI.DEMO-001 - INFO - Attempting transition: initialized -> active
2026-01-22 17:05:52,023 - SROI.DEMO-001 - INFO - Reason: Initiating sovereign operation
2026-01-22 17:05:52,023 - SROI.DEMO-001 - INFO - ✓ Transition successful: initialized -> active
2026-01-22 17:05:52,023 - SROI.DEMO-001 - INFO - Current metrics: {'roi_value': 0.0, ...}
```

### Log Files

Logs are automatically saved to:
- Directory: `logs/sroi/`
- Filename: `sroi_{operation_id}_{timestamp}.log`

Example: `logs/sroi/sroi_DEMO-001_20260122_170552.log`

## Integration with Existing Systems

### Red Code System

The S-ROI Protocol can be integrated with the existing Red Code system:

```python
from core.red_code import red_code_system
from core.sroi_sovereign_protocol import SROISovereignProtocol

protocol = SROISovereignProtocol(operation_id="REDCODE-001")

# Use Red Code's symbiosis level as sovereignty index
sovereignty = red_code_system.red_code.get("symbiosis_level", 0.5)
protocol.update_sovereignty_index(sovereignty)
```

### Euystacio Network

Integration with the Euystacio Network for comprehensive monitoring:

```python
from euystacio_network import get_euystacio_network
from core.sroi_sovereign_protocol import SROISovereignProtocol

network = get_euystacio_network()
protocol = SROISovereignProtocol(operation_id="NETWORK-001")

# Monitor network health
network_status = network.get_network_status()
sovereignty = network_status["red_code"]["symbiosis_level"]
protocol.update_sovereignty_index(sovereignty)
```

## API Reference

### SROISovereignProtocol

#### Constructor

```python
SROISovereignProtocol(operation_id: str, log_dir: str = "logs/sroi")
```

**Parameters**:
- `operation_id`: Unique identifier for the operation
- `log_dir`: Directory for log files (default: "logs/sroi")

#### Methods

##### transition_to()

```python
transition_to(new_state: SROIState, reason: str) -> bool
```

Transition to a new state with validation and logging.

**Returns**: True if successful, False if transition is invalid

##### update_roi()

```python
update_roi(value: float)
```

Update ROI value and check thresholds.

##### update_sovereignty_index()

```python
update_sovereignty_index(value: float)
```

Update sovereignty index (0.0 to 1.0) and check thresholds.

##### update_validation_score()

```python
update_validation_score(value: float)
```

Update validation score (0.0 to 1.0) and check thresholds.

##### get_status()

```python
get_status() -> Dict[str, Any]
```

Get comprehensive status report.

**Returns**: Dictionary with current state, metrics, and statistics

##### get_transition_history()

```python
get_transition_history() -> List[Dict[str, Any]]
```

Get complete transition history.

**Returns**: List of all state transitions with timestamps and metrics

##### export_logs()

```python
export_logs(filepath: str)
```

Export complete protocol logs to JSON file.

##### print_status_report()

```python
print_status_report()
```

Print formatted status report to console.

## Best Practices

### 1. Always Handle Transitions Properly

```python
# ✓ Good
if protocol.transition_to(SROIState.ACTIVE, "Activation"):
    print("Successfully activated")
else:
    print("Transition failed - check validation rules")

# ✗ Bad
protocol.transition_to(SROIState.ACTIVE, "Activation")  # Ignoring result
```

### 2. Monitor Critical Notifications

```python
# Regularly check for critical alerts
critical = protocol.notifier.get_notifications("CRITICAL")
if critical:
    for alert in critical:
        handle_critical_alert(alert)
```

### 3. Export Logs Regularly

```python
# Export logs after significant milestones
protocol.transition_to(SROIState.COMPLETED, "Success")
protocol.export_logs(f"logs/operation_{protocol.operation_id}.json")
```

### 4. Use Meaningful Operation IDs

```python
# ✓ Good
protocol = SROISovereignProtocol(
    operation_id=f"DEPLOY-{deployment_id}-{datetime.now().strftime('%Y%m%d')}"
)

# ✗ Bad
protocol = SROISovereignProtocol(operation_id="test")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m core.test_sroi_sovereign_protocol

# Run specific test class
python -m unittest core.test_sroi_sovereign_protocol.TestStateValidator

# Run with verbose output
python -m core.test_sroi_sovereign_protocol -v
```

Test coverage includes:
- State transition validation
- Threshold monitoring
- Notification generation
- Logging functionality
- Complete lifecycle scenarios
- Error handling

## Troubleshooting

### Common Issues

#### 1. Transition Rejected

**Problem**: `transition_to()` returns False

**Solution**: Check validation rules. Use `get_status()` to inspect current metrics.

```python
status = protocol.get_status()
print(f"Current state: {status['current_state']}")
print(f"Metrics: {status['metrics']}")
```

#### 2. No Logs Generated

**Problem**: Log files are empty

**Solution**: Ensure log directory exists and has write permissions.

```python
import os
log_dir = "logs/sroi"
os.makedirs(log_dir, exist_ok=True)
```

#### 3. Threshold Violations Not Detected

**Problem**: Critical state not triggered

**Solution**: Ensure `threshold_status` is set correctly when updating metrics.

```python
protocol.update_sovereignty_index(0.3)  # Automatically sets threshold_status
```

## Future Enhancements

Planned features for future versions:

1. **State Persistence**: Save/restore protocol state from database
2. **Webhook Notifications**: Send alerts to external systems
3. **Metric Trends**: Historical analysis and visualization
4. **Custom Validators**: User-defined validation rules
5. **Multi-Protocol Orchestration**: Coordinate multiple protocol instances
6. **Blockchain Integration**: Immutable audit trail on blockchain

## Contributing

To contribute to the S-ROI Sovereign Protocol:

1. Follow existing code style and documentation patterns
2. Add comprehensive tests for new features
3. Update this documentation for any API changes
4. Ensure all tests pass before submitting changes

## License

Part of the Euystacio AI Framework - AI Collective, 2026

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-22  
**Author**: AI Collective - Euystacio Framework
