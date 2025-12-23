# Seedbringer Treasury System Documentation

## Overview

The Seedbringer Treasury System is a comprehensive framework for managing and monitoring treasury assets (BTC/ETH), calculating sustainability runway, and providing real-time longevity metrics for the Euystacio AI project.

This system integrates with the Apollo Assistant to provide natural language command interface for treasury inquiries, aligned with NSR (Natural State Recognition) and OLF (Organic Living Framework) principles.

## Architecture

### Core Components

1. **Treasury Manager** (`core/treasury_manager.py`)
   - Real-time BTC/ETH balance management
   - Sustainability Runway calculations
   - Treasury health monitoring
   - IPFS data integration for long-term resilience

2. **Apollo Assistant** (`apollo_assistant.py`)
   - Natural language command interface
   - User-friendly treasury queries
   - Project longevity metrics
   - Health status reporting

3. **Notification System** (`notification_propagation.yml`)
   - Discord integration
   - Telegram integration
   - Instant update propagation
   - Event filtering and rate limiting

## Treasury Manager

### Features

- **Multi-Asset Support**: BTC, ETH, Stable coins, and other assets
- **Real-time Balances**: Track current holdings and USD values
- **Sustainability Runway**: Calculate how long treasury will last
- **Health Monitoring**: Automatic health status assessment
- **Snapshot System**: Create point-in-time treasury snapshots
- **IPFS Integration**: Long-term data persistence and resilience

### Usage

```python
from decimal import Decimal
from core.treasury_manager import TreasuryManager, TreasuryAssetType

# Initialize manager
manager = TreasuryManager(
    default_burn_rate_usd=Decimal("5000"),
    health_thresholds={
        "critical": 30,
        "warning": 90,
        "moderate": 180
    }
)

# Update BTC balance
manager.update_balance(
    asset_type=TreasuryAssetType.BTC,
    amount=Decimal("2.5"),
    usd_value=Decimal("100000"),
    blockchain_address="bc1q...",
    confirmation_count=6
)

# Update ETH balance
manager.update_balance(
    asset_type=TreasuryAssetType.ETH,
    amount=Decimal("50.0"),
    usd_value=Decimal("100000"),
    blockchain_address="0x...",
    confirmation_count=12
)

# Get sustainability runway
runway = manager.calculate_sustainability_runway()
print(f"Runway: {runway.runway_days} days ({runway.runway_months} months)")
print(f"Health Status: {runway.health_status.value}")

# Create snapshot
snapshot = manager.create_snapshot(
    metadata={"source": "scheduled_update"}
)

# Export for IPFS
json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)

# Attach IPFS CID after upload
manager.attach_ipfs_cid(snapshot.snapshot_id, "QmXYZ...")

# Get summary
summary = manager.get_treasury_summary()
```

### Health Status Thresholds

| Status | Default Threshold | Description |
|--------|------------------|-------------|
| **CRITICAL** | ≤ 30 days | Immediate action required |
| **WARNING** | ≤ 90 days | Below recommended threshold |
| **MODERATE** | ≤ 180 days | Acceptable range, monitor closely |
| **HEALTHY** | > 180 days | Well-funded for sustainable operations |

## Apollo Assistant

### Features

- **Natural Language Processing**: Understands conversational commands
- **Balance Queries**: Check BTC, ETH, or all balances
- **Treasury Overview**: Complete treasury summary
- **Longevity Metrics**: Project sustainability and runway
- **Health Status**: Quick health assessment
- **Help System**: Interactive command guidance

### Usage

```python
from apollo_assistant import ApolloAssistant
from core.treasury_manager import TreasuryManager

# Initialize
manager = TreasuryManager()
assistant = ApolloAssistant(manager)

# Process commands
response = assistant.process_command("show BTC balance")
print(response.message)

response = assistant.process_command("project longevity")
print(response.message)

response = assistant.process_command("treasury health")
print(response.message)
```

### Available Commands

#### Balance Queries
- `"show BTC balance"` - View Bitcoin balance
- `"show ETH balance"` - View Ethereum balance
- `"show balance"` - View all asset balances
- `"what's the bitcoin balance"` - Natural language variation
- `"get ethereum balance"` - Natural language variation

#### Treasury Queries
- `"show treasury"` - View complete treasury summary
- `"treasury status"` - View treasury overview
- `"treasury summary"` - Detailed treasury information

#### Longevity Metrics
- `"project longevity"` - View sustainability runway
- `"how long can we last"` - Project timeline
- `"sustainability runway"` - Detailed metrics
- `"when will we run out"` - Depletion projection

#### Health Status
- `"treasury health"` - View current health status
- `"health check"` - Quick health assessment
- `"is the treasury healthy"` - Natural language query

#### Help
- `"help"` - Show available commands
- `"commands"` - List all commands

### Response Format

All commands return a `CommandResponse` object:

```python
@dataclass
class CommandResponse:
    success: bool           # Whether command executed successfully
    category: CommandCategory  # Command category
    message: str           # Human-readable response
    data: Dict[str, Any]  # Structured data
    timestamp: str        # ISO 8601 timestamp
```

## Notification System

### Configuration

The notification system is configured via `notification_propagation.yml`:

#### Discord Integration

```yaml
discord:
  enabled: true
  webhook_env: "DISCORD_TREASURY_WEBHOOK"
  channels:
    treasury_updates:
      events:
        - balance_update
        - snapshot_created
    sustainability_alerts:
      events:
        - runway_warning
        - runway_critical
```

**Setup**:
1. Create Discord webhook in your server
2. Set environment variable: `export DISCORD_TREASURY_WEBHOOK="https://discord.com/api/webhooks/..."`
3. Enable in configuration

#### Telegram Integration

```yaml
telegram:
  enabled: true
  bot_token_env: "TELEGRAM_BOT_TOKEN"
  chat_id_env: "TELEGRAM_CHAT_ID"
```

**Setup**:
1. Create Telegram bot via [@BotFather](https://t.me/botfather)
2. Get bot token
3. Get chat ID (your user ID or group ID)
4. Set environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
   export TELEGRAM_CHAT_ID="-1001234567890"
   ```

### Event Types

| Event | Description | Channels |
|-------|-------------|----------|
| `balance_update` | Asset balance changed | Discord, Telegram |
| `snapshot_created` | New treasury snapshot | Discord, Telegram |
| `runway_warning` | Runway below warning threshold | Discord, Telegram |
| `runway_critical` | Runway critical (≤ 30 days) | Discord, Telegram (Priority) |
| `health_status_change` | Health status changed | Discord, Telegram |
| `ipfs_sync` | IPFS synchronization event | Discord |

### Rate Limiting

```yaml
rate_limiting:
  enabled: true
  max_messages_per_minute: 10
  max_messages_per_hour: 100
  burst_allowance: 3
```

## IPFS Integration

### Overview

Treasury snapshots are stored on IPFS for:
- **Long-term resilience**: Decentralized storage
- **Data integrity**: Content-addressed storage
- **Immutability**: Historical data preservation
- **Transparency**: Public verifiability

### Workflow

1. **Create Snapshot**: Generate treasury snapshot with all current data
2. **Export to JSON**: Serialize snapshot for IPFS storage
3. **Upload to IPFS**: Store on IPFS network
4. **Record CID**: Attach IPFS CID to snapshot
5. **Verify**: Cross-verify data integrity

### Example

```python
# Create snapshot
snapshot = manager.create_snapshot()

# Export for IPFS
json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)

# Upload to IPFS (using your IPFS client)
# ipfs_cid = ipfs_client.add(json_data)
ipfs_cid = "QmX7T9Zk3kV4hN8wYpL2mR5nQ6jP1xW9dS8cB7fE6gH5i"

# Attach CID to snapshot
manager.attach_ipfs_cid(snapshot.snapshot_id, ipfs_cid)
```

## Testing

### Running Tests

```bash
# Treasury Manager tests
python3 core/test_treasury.py

# Apollo Assistant tests
python3 test_apollo_assistant.py

# All tests
python3 core/test_treasury.py && python3 test_apollo_assistant.py
```

### Test Coverage

**Treasury Manager**: 16 tests covering:
- Initialization
- Balance updates (BTC, ETH)
- Total value calculation
- Sustainability runway (all health statuses)
- Snapshot management
- IPFS integration
- Custom burn rates
- Edge cases (zero burn rate)

**Apollo Assistant**: 18 tests covering:
- Command parsing
- All command categories
- Natural language variations
- Edge cases (empty data, unknown commands)
- Case insensitivity
- Response formatting

## Scheduled Test - January 10

### Test Plan

The comprehensive test scheduled for **January 10, 2025** will verify:

1. ✅ **Core Functionality**
   - Real-time balance queries (BTC/ETH)
   - Sustainability runway calculations
   - Health status monitoring

2. ✅ **Apollo Assistant**
   - Command processing
   - Natural language understanding
   - Response formatting

3. ✅ **Integration**
   - IPFS data storage and retrieval
   - Snapshot management
   - Data export/import

4. 📋 **Notification System** (To be tested with live credentials)
   - Discord webhook delivery
   - Telegram bot messaging
   - Event filtering
   - Rate limiting

5. 📋 **End-to-End Workflow**
   - Balance update → Snapshot → IPFS → Notification
   - Health degradation → Alert → Recovery

### Pre-Test Checklist

- [x] Treasury Manager implemented and tested
- [x] Apollo Assistant implemented and tested
- [x] IPFS integration ready
- [x] Notification configuration created
- [ ] Discord webhook configured (requires credentials)
- [ ] Telegram bot configured (requires credentials)
- [ ] Live treasury addresses configured
- [ ] Burn rate calibrated to actual expenses

## NSR and OLF Alignment

### Natural State Recognition (NSR)

The Seedbringer Treasury System honors natural cycles and recognizes:
- **Sustainability**: Treasury runway mirrors natural resource management
- **Health Monitoring**: Like natural systems, early warning signals prevent collapse
- **Transparency**: Open data aligns with natural information flow

### Organic Living Framework (OLF)

The system embodies organic principles:
- **Growth**: Treasury grows through sustainable practices
- **Resilience**: IPFS integration ensures long-term data survival
- **Interconnection**: Apollo Assistant bridges human intent and system data
- **Adaptability**: Configurable thresholds adapt to changing conditions

## API Reference

### TreasuryManager

```python
class TreasuryManager:
    def __init__(
        self,
        default_burn_rate_usd: Decimal = Decimal("5000"),
        health_thresholds: Optional[Dict[str, int]] = None
    )
    
    def update_balance(
        self,
        asset_type: TreasuryAssetType,
        amount: Decimal,
        usd_value: Decimal,
        blockchain_address: Optional[str] = None,
        confirmation_count: int = 6
    ) -> AssetBalance
    
    def get_balance(self, asset_type: TreasuryAssetType) -> Optional[AssetBalance]
    
    def get_total_usd_value(self) -> Decimal
    
    def calculate_sustainability_runway(
        self,
        monthly_burn_rate_usd: Optional[Decimal] = None
    ) -> SustainabilityRunway
    
    def create_snapshot(
        self,
        monthly_burn_rate_usd: Optional[Decimal] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TreasurySnapshot
    
    def get_latest_snapshot(self) -> Optional[TreasurySnapshot]
    
    def attach_ipfs_cid(self, snapshot_id: str, ipfs_cid: str) -> bool
    
    def export_snapshot_for_ipfs(self, snapshot_id: str) -> Optional[str]
    
    def get_treasury_summary(self) -> Dict[str, Any]
```

### ApolloAssistant

```python
class ApolloAssistant:
    def __init__(self, treasury_manager: TreasuryManager)
    
    def process_command(self, command: str) -> CommandResponse
    
    def get_command_suggestions(self) -> List[str]
```

## Troubleshooting

### Common Issues

**Q: Balance query returns "No data available"**
- Ensure balances have been updated using `manager.update_balance()`
- Check that the correct asset type is being queried

**Q: Health status always shows CRITICAL**
- Verify burn rate is set correctly
- Check treasury balance values are accurate
- Adjust health thresholds if needed

**Q: Commands not recognized**
- Commands are case-insensitive but check spelling
- Try alternative phrasings (e.g., "show BTC balance" vs "get bitcoin balance")
- Use `"help"` command to see available options

**Q: IPFS CID not attaching**
- Verify snapshot ID is correct
- Ensure snapshot was created before attaching CID
- Check CID format is valid

## Future Enhancements

- **Real-time Price Feeds**: Integrate with price oracles for live USD values
- **Multi-chain Support**: Add support for more blockchain networks
- **Advanced Analytics**: Historical trends, predictions, optimization
- **Web Dashboard**: Visual interface for treasury monitoring
- **Automated Rebalancing**: Smart treasury allocation
- **DeFi Integration**: Yield generation on idle assets

## Support and Contact

For issues, questions, or contributions:
- Repository: `hannesmitterer/euystacio-ai`
- Related: `hannesmitterer/euystacio-helmi-ai`, `hannesmitterer/peacebonds`
- January 10 Workshop: Comprehensive testing and validation

---

**Version**: 1.0  
**Last Updated**: December 23, 2024  
**Prepared for**: January 10, 2025 Workshop Test  
**Authority**: Seedbringer Council and Euystacio AI Collective
