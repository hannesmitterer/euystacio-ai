# Seedbringer Treasury System - Quick Start Guide

## Installation & Setup

### 1. Prerequisites

```bash
# Python 3.12+
python3 --version

# Install dependencies (already in requirements.txt)
# No additional dependencies needed - uses Python stdlib
```

### 2. Basic Usage

```python
from decimal import Decimal
from core.treasury_manager import TreasuryManager, TreasuryAssetType
from apollo_assistant import ApolloAssistant

# Initialize
manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
assistant = ApolloAssistant(manager)

# Update balances
manager.update_balance(
    TreasuryAssetType.BTC,
    Decimal("2.0"),
    Decimal("80000")
)

# Query via Apollo Assistant
response = assistant.process_command("show BTC balance")
print(response.message)
```

## Common Commands

### Balance Queries
```
show BTC balance
show ETH balance  
show balance
```

### Treasury Status
```
show treasury
treasury status
```

### Longevity Metrics
```
project longevity
how long can we last
sustainability runway
```

### Health Check
```
treasury health
health check
```

### Help
```
help
```

## Quick Examples

### Check Treasury Health

```python
response = assistant.process_command("treasury health")
print(response.message)
# Output: ✅ Treasury Health: HEALTHY
#         Runway: 480 days remaining
```

### Get Longevity Metrics

```python
response = assistant.process_command("project longevity")
print(response.message)
# Output: Project Longevity Metrics:
#   • Treasury Balance: $100,000.00 USD
#   • Monthly Burn Rate: $5,000.00 USD
#   • Sustainability Runway: 600 days (20.0 months)
#   • Health Status: HEALTHY
```

### View All Balances

```python
response = assistant.process_command("show balance")
print(response.message)
# Output: Current Treasury Balances:
#   • BTC: 2.0 ($80,000.00 USD)
#   • ETH: 10.0 ($20,000.00 USD)
#
# Total Value: $100,000.00 USD
```

## Testing

```bash
# Run all tests
python3 core/test_treasury.py
python3 test_apollo_assistant.py

# Expected output: All tests passing ✅
```

## Configuration

### Set Burn Rate

```python
manager = TreasuryManager(default_burn_rate_usd=Decimal("7500"))
```

### Custom Health Thresholds

```python
manager = TreasuryManager(
    health_thresholds={
        "critical": 20,   # 20 days
        "warning": 60,    # 60 days  
        "moderate": 120   # 120 days
    }
)
```

## Notifications Setup

### Discord

1. Create webhook in Discord server
2. Set environment variable:
```bash
export DISCORD_TREASURY_WEBHOOK="https://discord.com/api/webhooks/..."
```

### Telegram

1. Create bot via @BotFather
2. Get bot token and chat ID
3. Set environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

## IPFS Integration

```python
# Create snapshot
snapshot = manager.create_snapshot()

# Export for IPFS
json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)

# After uploading to IPFS, attach CID
manager.attach_ipfs_cid(snapshot.snapshot_id, "QmYourCID...")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No balance data" | Update balances first with `update_balance()` |
| Command not recognized | Check spelling, try `help` |
| Tests failing | Ensure Python 3.12+, check imports |

## Next Steps

1. ✅ Set up treasury with real balances
2. ✅ Configure burn rate based on actual expenses
3. 📋 Set up Discord/Telegram notifications
4. 📋 Integrate IPFS for snapshot storage
5. 📋 Schedule regular balance updates
6. 📋 Prepare for January 10 workshop test

## Resources

- **Full Documentation**: `docs/TREASURY_SYSTEM.md`
- **Tests**: `core/test_treasury.py`, `test_apollo_assistant.py`
- **Configuration**: `notification_propagation.yml`
- **Funding**: `.github/FUNDING.yml`

---

**Quick Help**: Type `help` in Apollo Assistant for available commands
