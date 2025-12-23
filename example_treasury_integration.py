#!/usr/bin/env python3
"""
example_treasury_integration.py
Example demonstrating end-to-end Seedbringer Treasury System integration

This script shows:
- Setting up the treasury manager
- Updating balances
- Creating snapshots
- Using Apollo Assistant
- Preparing data for IPFS
- Simulating notification events

For January 10 workshop demonstration.
"""

from decimal import Decimal
from datetime import datetime, timezone
import json

from core.treasury_manager import (
    TreasuryManager,
    TreasuryAssetType,
    TreasuryHealthStatus
)
from apollo_assistant import ApolloAssistant


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demonstrate_treasury_setup():
    """Demonstrate basic treasury setup"""
    print_section("1. Treasury Manager Setup")
    
    # Initialize with custom settings
    manager = TreasuryManager(
        default_burn_rate_usd=Decimal("7500"),  # $7,500/month burn rate
        health_thresholds={
            "critical": 30,
            "warning": 90,
            "moderate": 180
        }
    )
    
    print("✅ Treasury Manager initialized")
    print(f"   • Default Burn Rate: $7,500 USD/month")
    print(f"   • Health Thresholds: Critical=30d, Warning=90d, Moderate=180d")
    
    return manager


def demonstrate_balance_updates(manager: TreasuryManager):
    """Demonstrate updating asset balances"""
    print_section("2. Updating Asset Balances")
    
    # Update BTC balance
    btc_balance = manager.update_balance(
        asset_type=TreasuryAssetType.BTC,
        amount=Decimal("3.5"),
        usd_value=Decimal("140000"),
        blockchain_address="bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        confirmation_count=6
    )
    
    print(f"✅ BTC Balance Updated:")
    print(f"   • Amount: {btc_balance.amount} BTC")
    print(f"   • USD Value: ${btc_balance.usd_value:,.2f}")
    print(f"   • Address: {btc_balance.blockchain_address}")
    print(f"   • Confirmations: {btc_balance.confirmation_count}")
    
    # Update ETH balance
    eth_balance = manager.update_balance(
        asset_type=TreasuryAssetType.ETH,
        amount=Decimal("75.0"),
        usd_value=Decimal("150000"),
        blockchain_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        confirmation_count=12
    )
    
    print(f"\n✅ ETH Balance Updated:")
    print(f"   • Amount: {eth_balance.amount} ETH")
    print(f"   • USD Value: ${eth_balance.usd_value:,.2f}")
    print(f"   • Address: {eth_balance.blockchain_address}")
    print(f"   • Confirmations: {eth_balance.confirmation_count}")
    
    total_value = manager.get_total_usd_value()
    print(f"\n💰 Total Treasury Value: ${total_value:,.2f} USD")


def demonstrate_sustainability_metrics(manager: TreasuryManager):
    """Demonstrate sustainability runway calculations"""
    print_section("3. Sustainability Runway Metrics")
    
    runway = manager.calculate_sustainability_runway()
    
    print(f"📊 Treasury Sustainability Analysis:")
    print(f"   • Total Treasury: ${runway.total_treasury_usd:,.2f} USD")
    print(f"   • Monthly Burn Rate: ${runway.monthly_burn_rate_usd:,.2f} USD")
    print(f"   • Runway: {runway.runway_days} days ({runway.runway_months:.1f} months)")
    print(f"   • Health Status: {runway.health_status.value}")
    
    if runway.projected_depletion_date:
        print(f"   • Projected Depletion: {runway.projected_depletion_date[:10]}")
    
    # Health status interpretation
    status_emoji = {
        TreasuryHealthStatus.HEALTHY: "✅",
        TreasuryHealthStatus.MODERATE: "⚡",
        TreasuryHealthStatus.WARNING: "⚠️",
        TreasuryHealthStatus.CRITICAL: "🚨"
    }
    
    emoji = status_emoji.get(runway.health_status, "❓")
    print(f"\n{emoji} Treasury is {runway.health_status.value}")


def demonstrate_snapshot_creation(manager: TreasuryManager):
    """Demonstrate snapshot creation and IPFS preparation"""
    print_section("4. Treasury Snapshot & IPFS Integration")
    
    # Create snapshot
    snapshot = manager.create_snapshot(
        metadata={
            "source": "workshop_demonstration",
            "created_by": "Seedbringer Council",
            "test_date": "2025-01-10",
            "notes": "Pre-workshop treasury snapshot"
        }
    )
    
    print(f"📸 Snapshot Created:")
    print(f"   • Snapshot ID: {snapshot.snapshot_id}")
    print(f"   • Timestamp: {snapshot.timestamp[:19]}")
    print(f"   • Total Assets: {len(snapshot.balances)}")
    print(f"   • Total Value: ${snapshot.total_usd_value:,.2f} USD")
    
    # Export for IPFS
    json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)
    
    print(f"\n💾 IPFS Export Prepared:")
    print(f"   • JSON Size: {len(json_data)} bytes")
    print(f"   • Ready for IPFS upload")
    
    # Simulate IPFS upload (PLACEHOLDER - in production, use real IPFS client)
    # Example with ipfshttpclient:
    # import ipfshttpclient
    # client = ipfshttpclient.connect()
    # result = client.add_str(json_data)
    # simulated_cid = result
    simulated_cid = "QmX7T9Zk3kV4hN8wYpL2mR5nQ6jP1xW9dS8cB7fE6gH5i"  # PLACEHOLDER CID
    success = manager.attach_ipfs_cid(snapshot.snapshot_id, simulated_cid)
    
    if success:
        print(f"\n🌐 IPFS CID Attached:")
        print(f"   • CID: {simulated_cid}")
        print(f"   • IPFS URL: https://ipfs.io/ipfs/{simulated_cid}")
    
    return snapshot


def demonstrate_apollo_assistant(manager: TreasuryManager):
    """Demonstrate Apollo Assistant command interface"""
    print_section("5. Apollo Assistant - Natural Language Queries")
    
    assistant = ApolloAssistant(manager)
    
    # Test various commands
    commands = [
        "show BTC balance",
        "show treasury",
        "project longevity",
        "treasury health"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n💬 Command {i}: \"{command}\"")
        print("-" * 70)
        
        response = assistant.process_command(command)
        
        if response.success:
            print(response.message)
        else:
            print(f"❌ Error: {response.message}")
        
        print()


def demonstrate_treasury_summary(manager: TreasuryManager):
    """Demonstrate complete treasury summary"""
    print_section("6. Complete Treasury Summary")
    
    summary = manager.get_treasury_summary()
    
    print("📋 Treasury Status Report")
    print(f"   Generated: {summary['timestamp'][:19]}")
    print()
    print(f"💰 Assets:")
    print(f"   • Total Assets: {summary['total_assets']}")
    print(f"   • Total Value: ${Decimal(summary['total_usd_value']):,.2f} USD")
    print()
    
    print(f"📊 Health & Sustainability:")
    runway = summary['sustainability_runway']
    print(f"   • Health Status: {summary['health_status']}")
    print(f"   • Runway: {runway['runway_days']} days")
    print(f"   • Monthly Burn: ${Decimal(runway['monthly_burn_rate_usd']):,.2f}")
    print()
    
    print(f"📸 Snapshots:")
    print(f"   • Total Snapshots: {summary['total_snapshots']}")


def simulate_notification_events():
    """Simulate notification events that would be triggered"""
    print_section("7. Notification System Events (Simulated)")
    
    events = [
        {
            "event": "balance_update",
            "asset": "BTC",
            "change_usd": 5000,
            "channels": ["discord.treasury_updates", "telegram.treasury_updates"]
        },
        {
            "event": "snapshot_created",
            "snapshot_id": "abc123...",
            "channels": ["discord.general"]
        },
        {
            "event": "health_status_change",
            "from": "MODERATE",
            "to": "HEALTHY",
            "channels": ["discord.sustainability_alerts", "telegram.alerts"]
        }
    ]
    
    print("📢 Notification Events (would be sent to Discord/Telegram):\n")
    
    for i, event in enumerate(events, 1):
        print(f"{i}. Event: {event['event']}")
        print(f"   Channels: {', '.join(event['channels'])}")
        if 'asset' in event:
            print(f"   Asset: {event['asset']}, Change: ${event['change_usd']:,.2f}")
        if 'from' in event:
            print(f"   Status Change: {event['from']} → {event['to']}")
        print()
    
    print("⚙️  To enable live notifications:")
    print("   1. Set up Discord webhook: export DISCORD_TREASURY_WEBHOOK='...'")
    print("   2. Set up Telegram bot: export TELEGRAM_BOT_TOKEN='...'")
    print("   3. Configure notification_propagation.yml")


def main():
    """Main demonstration script"""
    print("\n" + "="*70)
    print("  🌟 SEEDBRINGER TREASURY SYSTEM - FULL DEMONSTRATION 🌟")
    print("  Prepared for January 10, 2025 Workshop")
    print("="*70)
    
    # 1. Setup
    manager = demonstrate_treasury_setup()
    
    # 2. Update balances
    demonstrate_balance_updates(manager)
    
    # 3. Calculate sustainability
    demonstrate_sustainability_metrics(manager)
    
    # 4. Create snapshot
    demonstrate_snapshot_creation(manager)
    
    # 5. Apollo Assistant
    demonstrate_apollo_assistant(manager)
    
    # 6. Summary
    demonstrate_treasury_summary(manager)
    
    # 7. Notifications
    simulate_notification_events()
    
    # Final message
    print_section("✅ Demonstration Complete")
    print("All components of the Seedbringer Treasury System are operational!")
    print()
    print("Next Steps:")
    print("  1. Configure live blockchain addresses")
    print("  2. Set up real-time price feeds")
    print("  3. Enable Discord/Telegram notifications")
    print("  4. Deploy IPFS node for snapshot storage")
    print("  5. Schedule automated balance updates")
    print("  6. Conduct January 10 workshop test")
    print()
    print("Documentation:")
    print("  • Full Guide: docs/TREASURY_SYSTEM.md")
    print("  • Quick Start: docs/TREASURY_QUICKSTART.md")
    print("  • Tests: core/test_treasury.py, test_apollo_assistant.py")
    print()
    print("Aligned with NSR and OLF principles ✨")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
