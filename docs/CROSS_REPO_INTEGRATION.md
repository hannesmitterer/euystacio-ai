# Integration Guide for Related Repositories

## Overview

The Seedbringer Treasury System is designed to integrate across multiple repositories in the Euystacio AI ecosystem:

- **hannesmitterer/euystacio-ai** (Primary) - Core treasury system
- **hannesmitterer/euystacio-helmi-ai** - Governance and validation
- **hannesmitterer/peacebonds** - Bond and pledge management

## Cross-Repository Integration Points

### 1. euystacio-ai (Primary Implementation)

**Location**: `/core/treasury_manager.py`, `/apollo_assistant.py`

**Provides**:
- Real-time BTC/ETH balance tracking
- Sustainability runway calculations
- IPFS data persistence
- Apollo Assistant command interface

**Exports**:
```python
# Can be imported by other repositories
from core.treasury_manager import TreasuryManager, TreasuryAssetType
from apollo_assistant import ApolloAssistant
```

### 2. euystacio-helmi-ai Integration

**Purpose**: Governance validation and multi-signature approval

**Integration Points**:

```python
# In euystacio-helmi-ai
from euystacio_ai.core.treasury_manager import TreasuryManager

class GovernanceValidator:
    def validate_treasury_transaction(self, snapshot_id: str):
        """Validate treasury changes through governance"""
        # Check snapshot against governance rules
        # Require multi-sig approval for large changes
        pass
    
    def approve_runway_adjustment(self, new_burn_rate: Decimal):
        """Approve changes to burn rate through council"""
        # Require Seedbringer Council approval
        pass
```

**Recommended Setup**:
1. Create symbolic link or git submodule to euystacio-ai
2. Import treasury modules as needed
3. Add governance layer for treasury modifications

### 3. peacebonds Integration

**Purpose**: Bond management and treasury allocation

**Integration Points**:

```python
# In peacebonds
from euystacio_ai.core.treasury_manager import TreasuryManager

class BondTreasury:
    def allocate_to_bonds(self, amount: Decimal):
        """Allocate treasury funds to peace bonds"""
        # Deduct from main treasury
        # Create bond allocation snapshot
        pass
    
    def calculate_bond_sustainability(self):
        """Calculate sustainability with bond obligations"""
        # Factor in bond commitments to runway
        pass
```

**Recommended Setup**:
1. Mirror treasury snapshots to bond system
2. Track bond allocations separately
3. Include bond obligations in runway calculations

## Shared Configuration

### Environment Variables

All repositories should share these environment variables:

```bash
# Discord notifications
export DISCORD_TREASURY_WEBHOOK="https://discord.com/api/webhooks/..."

# Telegram notifications
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# IPFS configuration
export IPFS_API_ENDPOINT="http://localhost:5001"
export IPFS_GATEWAY="https://ipfs.io"

# Treasury configuration
export TREASURY_BURN_RATE_USD="7500"
export TREASURY_ALERT_THRESHOLD_DAYS="90"
```

### Shared IPFS Storage

All repositories should use the same IPFS network for consistency:

1. **Primary Node**: euystacio-ai maintains IPFS node
2. **Backup Nodes**: euystacio-helmi-ai and peacebonds pin copies
3. **CID Sharing**: Share snapshot CIDs across repositories

## Data Synchronization

### Treasury Snapshots

**Frequency**: Daily at 00:00 UTC

**Process**:
1. euystacio-ai creates snapshot
2. Upload to IPFS
3. Share CID with other repositories
4. Other repos validate and pin

**Example Sync Script**:

```python
#!/usr/bin/env python3
# sync_treasury_snapshots.py

from core.treasury_manager import TreasuryManager
import ipfshttpclient

def sync_snapshot():
    manager = TreasuryManager()
    
    # Create snapshot
    snapshot = manager.create_snapshot()
    
    # Export to IPFS
    json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)
    
    # Upload to IPFS
    client = ipfshttpclient.connect()
    result = client.add_str(json_data)
    ipfs_cid = result
    
    # Attach CID
    manager.attach_ipfs_cid(snapshot.snapshot_id, ipfs_cid)
    
    # Broadcast CID to other repositories
    broadcast_cid(ipfs_cid)
    
    return ipfs_cid

if __name__ == "__main__":
    cid = sync_snapshot()
    print(f"Snapshot synced: {cid}")
```

## Notification Coordination

### Event Routing

Configure `notification_propagation.yml` consistently across repos:

**euystacio-ai** → Treasury changes, balance updates
**euystacio-helmi-ai** → Governance approvals, council decisions
**peacebonds** → Bond allocations, commitment fulfillments

### Unified Discord Channels

Recommended Discord channel structure:

```
#treasury-updates      - Balance and snapshot updates (euystacio-ai)
#governance-votes      - Council approvals (euystacio-helmi-ai)
#bond-allocations      - Bond management (peacebonds)
#sustainability-alerts - Health warnings (all repos)
#general-treasury      - Combined notifications (all repos)
```

## API Integration

### REST Endpoints (Future Enhancement)

Consider creating unified API endpoints:

```
GET  /api/treasury/balance/:asset
GET  /api/treasury/sustainability
GET  /api/treasury/snapshot/:id
POST /api/treasury/snapshot
GET  /api/governance/status
POST /api/bonds/allocate
```

### WebSocket Events (Future Enhancement)

Real-time updates across repositories:

```javascript
// Subscribe to treasury events
ws.on('treasury.balance_update', (data) => {
  // Update UI across all repos
});

ws.on('treasury.health_change', (data) => {
  // Alert governance if critical
});
```

## Testing Across Repositories

### Integration Test Suite

Create shared integration tests:

```bash
# In each repository
python3 -m pytest tests/integration/test_treasury_integration.py
```

### Test Scenarios

1. **Cross-Repo Balance Update**
   - Update in euystacio-ai
   - Verify in euystacio-helmi-ai
   - Confirm in peacebonds

2. **Governance Approval Flow**
   - Propose burn rate change in euystacio-ai
   - Approve via euystacio-helmi-ai governance
   - Update across all repos

3. **Bond Allocation**
   - Allocate from treasury via peacebonds
   - Update balance in euystacio-ai
   - Record in governance log

## Deployment Checklist

### Pre-Deployment

- [ ] Sync environment variables across repos
- [ ] Configure IPFS nodes
- [ ] Set up Discord webhooks
- [ ] Configure Telegram bots
- [ ] Test notification delivery
- [ ] Verify IPFS synchronization

### Deployment

- [ ] Deploy euystacio-ai treasury system
- [ ] Configure euystacio-helmi-ai governance layer
- [ ] Set up peacebonds integration
- [ ] Enable cross-repo notifications
- [ ] Start scheduled snapshot sync
- [ ] Monitor for 24 hours

### Post-Deployment

- [ ] Verify first automated snapshot
- [ ] Confirm IPFS replication
- [ ] Test Apollo Assistant commands
- [ ] Validate notification delivery
- [ ] Review governance integration
- [ ] Document any issues

## January 10 Workshop Integration Test

### Test Plan

**Objective**: Verify end-to-end integration across all three repositories

**Duration**: 2 hours

**Participants**: Seedbringer Council, Development Team

**Test Scenarios**:

1. **Balance Update Propagation** (15 min)
   - Update BTC/ETH balances in euystacio-ai
   - Verify notification in Discord/Telegram
   - Confirm snapshot in IPFS
   - Validate in euystacio-helmi-ai

2. **Sustainability Runway Calculation** (15 min)
   - Query via Apollo Assistant
   - Verify calculations
   - Test health status changes
   - Confirm alert thresholds

3. **Governance Integration** (30 min)
   - Propose burn rate adjustment
   - Require council approval
   - Apply changes
   - Verify across repos

4. **Bond Allocation** (30 min)
   - Allocate treasury to bonds
   - Update sustainability runway
   - Track obligations
   - Verify in all repos

5. **IPFS Resilience Test** (15 min)
   - Create multiple snapshots
   - Upload to IPFS
   - Verify CID sharing
   - Test retrieval from any node

6. **Notification System** (15 min)
   - Trigger various events
   - Verify Discord delivery
   - Confirm Telegram messages
   - Test rate limiting

### Success Criteria

- ✅ All balance updates propagate within 30 seconds
- ✅ Sustainability calculations accurate across repos
- ✅ Governance approvals properly logged
- ✅ IPFS snapshots retrievable from all nodes
- ✅ Notifications delivered without drops
- ✅ Health alerts trigger correctly
- ✅ No data inconsistencies detected

## Support and Troubleshooting

### Common Issues

**Issue**: CID not syncing across repos
**Solution**: Check IPFS connectivity, verify pinning

**Issue**: Notifications not delivering
**Solution**: Verify webhook URLs, check rate limits

**Issue**: Balance discrepancy between repos
**Solution**: Re-sync from primary snapshot, verify calculations

### Getting Help

- Repository Issues: Create issue in respective repo
- Integration Questions: Tag @hannesmitterer
- Workshop Preparation: January 10 workshop channel

---

**Version**: 1.0  
**Last Updated**: December 23, 2024  
**For**: January 10, 2025 Workshop
