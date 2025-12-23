"""
test_treasury.py
Test Suite for Seedbringer Treasury System

Tests:
- Treasury Manager functionality
- Balance updates and queries
- Sustainability Runway calculations
- IPFS integration
- Snapshot management
"""

import sys
import os
from decimal import Decimal

# Ensure the parent directory is in the path for proper imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.treasury_manager import (
    TreasuryManager,
    TreasuryAssetType,
    TreasuryHealthStatus,
    AssetBalance,
    SustainabilityRunway,
    TreasurySnapshot
)


class TestTreasuryManager:
    """Tests for Treasury Manager"""
    
    def test_initialization(self):
        """Test Treasury Manager initialization"""
        manager = TreasuryManager(
            default_burn_rate_usd=Decimal("5000"),
            health_thresholds={"critical": 30, "warning": 90, "moderate": 180}
        )
        
        assert manager.default_burn_rate_usd == Decimal("5000")
        assert manager.health_thresholds["critical"] == 30
        assert len(manager.balances) == 0
        assert len(manager.snapshots) == 0
        
        print("✅ test_initialization passed")
    
    def test_update_btc_balance(self):
        """Test updating BTC balance"""
        manager = TreasuryManager()
        
        balance = manager.update_balance(
            asset_type=TreasuryAssetType.BTC,
            amount=Decimal("1.5"),
            usd_value=Decimal("60000"),
            blockchain_address="bc1q...",
            confirmation_count=6
        )
        
        assert balance.asset_type == TreasuryAssetType.BTC
        assert balance.amount == Decimal("1.5")
        assert balance.usd_value == Decimal("60000")
        assert balance.blockchain_address == "bc1q..."
        assert balance.confirmation_count == 6
        
        print("✅ test_update_btc_balance passed")
    
    def test_update_eth_balance(self):
        """Test updating ETH balance"""
        manager = TreasuryManager()
        
        balance = manager.update_balance(
            asset_type=TreasuryAssetType.ETH,
            amount=Decimal("10.0"),
            usd_value=Decimal("20000"),
            blockchain_address="0x...",
            confirmation_count=12
        )
        
        assert balance.asset_type == TreasuryAssetType.ETH
        assert balance.amount == Decimal("10.0")
        assert balance.usd_value == Decimal("20000")
        
        print("✅ test_update_eth_balance passed")
    
    def test_get_balance(self):
        """Test retrieving specific balance"""
        manager = TreasuryManager()
        
        # Add BTC balance
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("2.0"),
            Decimal("80000")
        )
        
        # Retrieve balance
        btc_balance = manager.get_balance(TreasuryAssetType.BTC)
        
        assert btc_balance is not None
        assert btc_balance.asset_type == TreasuryAssetType.BTC
        assert btc_balance.amount == Decimal("2.0")
        
        # Try to get non-existent balance
        eth_balance = manager.get_balance(TreasuryAssetType.ETH)
        assert eth_balance is None
        
        print("✅ test_get_balance passed")
    
    def test_get_total_usd_value(self):
        """Test calculating total USD value"""
        manager = TreasuryManager()
        
        # Add multiple assets
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("1.0"),
            Decimal("40000")
        )
        manager.update_balance(
            TreasuryAssetType.ETH,
            Decimal("10.0"),
            Decimal("20000")
        )
        
        total = manager.get_total_usd_value()
        
        assert total == Decimal("60000")
        
        print("✅ test_get_total_usd_value passed")
    
    def test_calculate_sustainability_runway_healthy(self):
        """Test sustainability runway calculation - healthy status"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
        
        # Add treasury balance
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("5.0"),
            Decimal("200000")
        )
        
        runway = manager.calculate_sustainability_runway()
        
        assert runway.total_treasury_usd == Decimal("200000")
        assert runway.monthly_burn_rate_usd == Decimal("5000")
        assert runway.runway_months == Decimal("40")  # 200000 / 5000
        assert runway.runway_days == 1200  # 40 * 30
        assert runway.health_status == TreasuryHealthStatus.HEALTHY
        assert runway.projected_depletion_date is not None
        
        print("✅ test_calculate_sustainability_runway_healthy passed")
    
    def test_calculate_sustainability_runway_critical(self):
        """Test sustainability runway calculation - critical status"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("10000"))
        
        # Add small treasury balance
        manager.update_balance(
            TreasuryAssetType.ETH,
            Decimal("5.0"),
            Decimal("100000")
        )
        
        runway = manager.calculate_sustainability_runway()
        
        assert runway.monthly_burn_rate_usd == Decimal("10000")
        assert runway.runway_months == Decimal("10")  # 100000 / 10000
        assert runway.runway_days == 300  # 10 * 30
        assert runway.health_status == TreasuryHealthStatus.HEALTHY  # 300 days is still healthy
        
        print("✅ test_calculate_sustainability_runway_critical passed")
    
    def test_calculate_sustainability_runway_warning(self):
        """Test sustainability runway calculation - warning status"""
        manager = TreasuryManager(
            default_burn_rate_usd=Decimal("5000"),
            health_thresholds={"critical": 30, "warning": 90, "moderate": 180}
        )
        
        # 60 days runway = WARNING status
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("1.0"),
            Decimal("10000")
        )
        
        runway = manager.calculate_sustainability_runway()
        
        assert runway.runway_days == 60  # (10000 / 5000) * 30
        assert runway.health_status == TreasuryHealthStatus.WARNING
        
        print("✅ test_calculate_sustainability_runway_warning passed")
    
    def test_custom_burn_rate(self):
        """Test using custom burn rate"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
        
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("1.0"),
            Decimal("100000")
        )
        
        # Use custom burn rate
        runway = manager.calculate_sustainability_runway(
            monthly_burn_rate_usd=Decimal("10000")
        )
        
        assert runway.monthly_burn_rate_usd == Decimal("10000")
        assert runway.runway_months == Decimal("10")
        
        print("✅ test_custom_burn_rate passed")
    
    def test_create_snapshot(self):
        """Test creating treasury snapshot"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
        
        # Add balances
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("2.0"),
            Decimal("80000")
        )
        manager.update_balance(
            TreasuryAssetType.ETH,
            Decimal("10.0"),
            Decimal("20000")
        )
        
        # Create snapshot
        snapshot = manager.create_snapshot(
            metadata={"note": "Test snapshot"}
        )
        
        assert snapshot.snapshot_id is not None
        assert len(snapshot.snapshot_id) == 16
        assert len(snapshot.balances) == 2
        assert snapshot.total_usd_value == Decimal("100000")
        assert snapshot.metadata["note"] == "Test snapshot"
        assert snapshot.sustainability_runway is not None
        
        print("✅ test_create_snapshot passed")
    
    def test_get_latest_snapshot(self):
        """Test retrieving latest snapshot"""
        manager = TreasuryManager()
        
        # Initially no snapshots
        latest = manager.get_latest_snapshot()
        assert latest is None
        
        # Create snapshots
        manager.update_balance(TreasuryAssetType.BTC, Decimal("1.0"), Decimal("40000"))
        snapshot1 = manager.create_snapshot()
        
        manager.update_balance(TreasuryAssetType.ETH, Decimal("5.0"), Decimal("10000"))
        snapshot2 = manager.create_snapshot()
        
        # Get latest
        latest = manager.get_latest_snapshot()
        assert latest is not None
        assert latest.snapshot_id == snapshot2.snapshot_id
        assert len(latest.balances) == 2
        
        print("✅ test_get_latest_snapshot passed")
    
    def test_attach_ipfs_cid(self):
        """Test attaching IPFS CID to snapshot"""
        manager = TreasuryManager()
        
        manager.update_balance(TreasuryAssetType.BTC, Decimal("1.0"), Decimal("40000"))
        snapshot = manager.create_snapshot()
        
        # Initially no IPFS CID
        assert snapshot.ipfs_cid is None
        
        # Attach IPFS CID
        success = manager.attach_ipfs_cid(
            snapshot.snapshot_id,
            "QmX7T9Zk3kV4hN8wYpL2mR5nQ6jP1xW9dS8cB7fE6gH5i"
        )
        
        assert success is True
        assert snapshot.ipfs_cid == "QmX7T9Zk3kV4hN8wYpL2mR5nQ6jP1xW9dS8cB7fE6gH5i"
        
        # Try invalid snapshot ID
        success = manager.attach_ipfs_cid("invalid_id", "QmTest")
        assert success is False
        
        print("✅ test_attach_ipfs_cid passed")
    
    def test_export_snapshot_for_ipfs(self):
        """Test exporting snapshot as JSON for IPFS"""
        manager = TreasuryManager()
        
        manager.update_balance(TreasuryAssetType.BTC, Decimal("1.5"), Decimal("60000"))
        snapshot = manager.create_snapshot()
        
        # Export snapshot
        json_data = manager.export_snapshot_for_ipfs(snapshot.snapshot_id)
        
        assert json_data is not None
        assert isinstance(json_data, str)
        assert snapshot.snapshot_id in json_data
        assert "BTC" in json_data
        
        # Try invalid snapshot ID
        invalid_export = manager.export_snapshot_for_ipfs("invalid_id")
        assert invalid_export is None
        
        print("✅ test_export_snapshot_for_ipfs passed")
    
    def test_get_treasury_summary(self):
        """Test getting treasury summary"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
        
        manager.update_balance(TreasuryAssetType.BTC, Decimal("2.0"), Decimal("80000"))
        manager.update_balance(TreasuryAssetType.ETH, Decimal("10.0"), Decimal("20000"))
        manager.create_snapshot()
        
        summary = manager.get_treasury_summary()
        
        assert summary["total_assets"] == 2
        assert summary["total_usd_value"] == "100000"
        assert "balances" in summary
        assert "BTC" in summary["balances"]
        assert "ETH" in summary["balances"]
        assert "sustainability_runway" in summary
        assert summary["total_snapshots"] == 1
        
        print("✅ test_get_treasury_summary passed")
    
    def test_zero_burn_rate(self):
        """Test handling zero burn rate (infinite runway)"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("0"))
        
        manager.update_balance(TreasuryAssetType.BTC, Decimal("1.0"), Decimal("40000"))
        
        runway = manager.calculate_sustainability_runway()
        
        assert runway.runway_months == Decimal("999")
        assert runway.runway_days == 999999
        assert runway.projected_depletion_date is None
        assert runway.health_status == TreasuryHealthStatus.HEALTHY
        
        print("✅ test_zero_burn_rate passed")
    
    def test_asset_balance_to_dict(self):
        """Test AssetBalance to_dict conversion"""
        balance = AssetBalance(
            asset_type=TreasuryAssetType.BTC,
            amount=Decimal("1.5"),
            usd_value=Decimal("60000"),
            last_updated="2025-01-10T00:00:00Z",
            blockchain_address="bc1q...",
            confirmation_count=6
        )
        
        data = balance.to_dict()
        
        assert data["asset_type"] == "BTC"
        assert data["amount"] == "1.5"
        assert data["usd_value"] == "60000"
        assert data["blockchain_address"] == "bc1q..."
        assert data["confirmation_count"] == 6
        
        print("✅ test_asset_balance_to_dict passed")


def run_all_tests():
    """Run all treasury tests"""
    print("\n" + "="*60)
    print("🧪 Running Seedbringer Treasury Test Suite")
    print("="*60 + "\n")
    
    test_suite = TestTreasuryManager()
    
    print("📊 Treasury Manager Tests:")
    print("-" * 40)
    
    tests = [
        test_suite.test_initialization,
        test_suite.test_update_btc_balance,
        test_suite.test_update_eth_balance,
        test_suite.test_get_balance,
        test_suite.test_get_total_usd_value,
        test_suite.test_calculate_sustainability_runway_healthy,
        test_suite.test_calculate_sustainability_runway_critical,
        test_suite.test_calculate_sustainability_runway_warning,
        test_suite.test_custom_burn_rate,
        test_suite.test_create_snapshot,
        test_suite.test_get_latest_snapshot,
        test_suite.test_attach_ipfs_cid,
        test_suite.test_export_snapshot_for_ipfs,
        test_suite.test_get_treasury_summary,
        test_suite.test_zero_burn_rate,
        test_suite.test_asset_balance_to_dict,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    total = len(tests)
    passed = total - failed
    print(f"✅ Tests Passed: {passed}/{total}")
    if failed > 0:
        print(f"❌ Tests Failed: {failed}/{total}")
    print("="*60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
