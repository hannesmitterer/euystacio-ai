"""
treasury_manager.py
Seedbringer Treasury Management System for Euystacio AI

This module provides:
- Real-time BTC/ETH balance querying
- Sustainability Runway calculation
- Treasury health monitoring
- IPFS data integration for long-term resilience

Aligned with NSR (Natural State Recognition) and OLF (Organic Living Framework) principles.
Prepared for January 10 workshop test.
"""

import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal


class TreasuryAssetType(Enum):
    """Types of treasury assets"""
    BTC = "BTC"
    ETH = "ETH"
    STABLE = "STABLE"
    OTHER = "OTHER"


class TreasuryHealthStatus(Enum):
    """Overall health status of treasury"""
    HEALTHY = "HEALTHY"
    MODERATE = "MODERATE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class AssetBalance:
    """Represents balance of a specific asset"""
    asset_type: TreasuryAssetType
    amount: Decimal
    usd_value: Decimal
    last_updated: str
    blockchain_address: Optional[str] = None
    confirmation_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_type": self.asset_type.value,
            "amount": str(self.amount),
            "usd_value": str(self.usd_value),
            "last_updated": self.last_updated,
            "blockchain_address": self.blockchain_address,
            "confirmation_count": self.confirmation_count
        }


@dataclass
class SustainabilityRunway:
    """Calculates and tracks project sustainability runway"""
    total_treasury_usd: Decimal
    monthly_burn_rate_usd: Decimal
    runway_months: Decimal
    runway_days: int
    health_status: TreasuryHealthStatus
    projected_depletion_date: Optional[str]
    last_calculated: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_treasury_usd": str(self.total_treasury_usd),
            "monthly_burn_rate_usd": str(self.monthly_burn_rate_usd),
            "runway_months": str(self.runway_months),
            "runway_days": self.runway_days,
            "health_status": self.health_status.value,
            "projected_depletion_date": self.projected_depletion_date,
            "last_calculated": self.last_calculated
        }


@dataclass
class TreasurySnapshot:
    """Complete treasury state snapshot"""
    snapshot_id: str
    timestamp: str
    balances: List[AssetBalance]
    total_usd_value: Decimal
    sustainability_runway: SustainabilityRunway
    ipfs_cid: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp,
            "balances": [b.to_dict() for b in self.balances],
            "total_usd_value": str(self.total_usd_value),
            "sustainability_runway": self.sustainability_runway.to_dict(),
            "ipfs_cid": self.ipfs_cid,
            "metadata": self.metadata
        }


class TreasuryManager:
    """
    Main Treasury Management System
    
    Provides real-time treasury data, sustainability calculations,
    and IPFS integration for data resilience.
    """
    
    def __init__(
        self,
        default_burn_rate_usd: Decimal = Decimal("5000"),
        health_thresholds: Optional[Dict[str, int]] = None
    ):
        """
        Initialize Treasury Manager
        
        Args:
            default_burn_rate_usd: Default monthly burn rate in USD
            health_thresholds: Dict mapping health status to runway days
                              e.g., {"critical": 30, "warning": 90, "moderate": 180}
        """
        self.default_burn_rate_usd = default_burn_rate_usd
        self.health_thresholds = health_thresholds or {
            "critical": 30,
            "warning": 90,
            "moderate": 180
        }
        self.balances: Dict[TreasuryAssetType, AssetBalance] = {}
        self.snapshots: List[TreasurySnapshot] = []
        
    def update_balance(
        self,
        asset_type: TreasuryAssetType,
        amount: Decimal,
        usd_value: Decimal,
        blockchain_address: Optional[str] = None,
        confirmation_count: int = 6
    ) -> AssetBalance:
        """
        Update balance for a specific asset
        
        Args:
            asset_type: Type of asset (BTC, ETH, etc.)
            amount: Amount of the asset
            usd_value: Current USD value of the total amount
            blockchain_address: Optional blockchain address
            confirmation_count: Number of confirmations
            
        Returns:
            Updated AssetBalance object
        """
        balance = AssetBalance(
            asset_type=asset_type,
            amount=amount,
            usd_value=usd_value,
            last_updated=datetime.now(timezone.utc).isoformat(),
            blockchain_address=blockchain_address,
            confirmation_count=confirmation_count
        )
        
        self.balances[asset_type] = balance
        return balance
    
    def get_balance(self, asset_type: TreasuryAssetType) -> Optional[AssetBalance]:
        """Get current balance for a specific asset"""
        return self.balances.get(asset_type)
    
    def get_total_usd_value(self) -> Decimal:
        """Calculate total USD value of all assets"""
        return sum(
            balance.usd_value for balance in self.balances.values()
        )
    
    def calculate_sustainability_runway(
        self,
        monthly_burn_rate_usd: Optional[Decimal] = None
    ) -> SustainabilityRunway:
        """
        Calculate project sustainability runway
        
        Args:
            monthly_burn_rate_usd: Optional custom burn rate, uses default if None
            
        Returns:
            SustainabilityRunway object with calculated metrics
        """
        burn_rate = monthly_burn_rate_usd or self.default_burn_rate_usd
        total_treasury = self.get_total_usd_value()
        
        # Calculate runway
        if burn_rate > 0:
            runway_months = total_treasury / burn_rate
            runway_days = int(runway_months * 30)  # Approximate
        else:
            runway_months = Decimal("999")  # Effectively infinite
            runway_days = 999999
        
        # Determine health status
        if runway_days <= self.health_thresholds["critical"]:
            health_status = TreasuryHealthStatus.CRITICAL
        elif runway_days <= self.health_thresholds["warning"]:
            health_status = TreasuryHealthStatus.WARNING
        elif runway_days <= self.health_thresholds["moderate"]:
            health_status = TreasuryHealthStatus.MODERATE
        else:
            health_status = TreasuryHealthStatus.HEALTHY
        
        # Calculate projected depletion date
        if runway_days < 999999:
            depletion_date = datetime.now(timezone.utc) + timedelta(days=runway_days)
            projected_depletion = depletion_date.isoformat()
        else:
            projected_depletion = None
        
        return SustainabilityRunway(
            total_treasury_usd=total_treasury,
            monthly_burn_rate_usd=burn_rate,
            runway_months=runway_months,
            runway_days=runway_days,
            health_status=health_status,
            projected_depletion_date=projected_depletion,
            last_calculated=datetime.now(timezone.utc).isoformat()
        )
    
    def create_snapshot(
        self,
        monthly_burn_rate_usd: Optional[Decimal] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TreasurySnapshot:
        """
        Create a complete treasury snapshot
        
        Args:
            monthly_burn_rate_usd: Optional custom burn rate
            metadata: Optional metadata to attach to snapshot
            
        Returns:
            TreasurySnapshot object
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Generate snapshot ID
        snapshot_data = f"{timestamp}:{len(self.balances)}:{self.get_total_usd_value()}"
        snapshot_id = hashlib.sha256(snapshot_data.encode()).hexdigest()[:16]
        
        # Calculate sustainability
        runway = self.calculate_sustainability_runway(monthly_burn_rate_usd)
        
        # Create snapshot
        snapshot = TreasurySnapshot(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            balances=list(self.balances.values()),
            total_usd_value=self.get_total_usd_value(),
            sustainability_runway=runway,
            metadata=metadata or {}
        )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_latest_snapshot(self) -> Optional[TreasurySnapshot]:
        """Get the most recent treasury snapshot"""
        return self.snapshots[-1] if self.snapshots else None
    
    def attach_ipfs_cid(self, snapshot_id: str, ipfs_cid: str) -> bool:
        """
        Attach IPFS CID to a snapshot for long-term resilience
        
        Args:
            snapshot_id: ID of the snapshot
            ipfs_cid: IPFS Content Identifier
            
        Returns:
            True if successful, False otherwise
        """
        for snapshot in self.snapshots:
            if snapshot.snapshot_id == snapshot_id:
                snapshot.ipfs_cid = ipfs_cid
                return True
        return False
    
    def export_snapshot_for_ipfs(self, snapshot_id: str) -> Optional[str]:
        """
        Export snapshot as JSON for IPFS storage
        
        Args:
            snapshot_id: ID of the snapshot to export
            
        Returns:
            JSON string of snapshot data, or None if not found
        """
        for snapshot in self.snapshots:
            if snapshot.snapshot_id == snapshot_id:
                return json.dumps(snapshot.to_dict(), indent=2)
        return None
    
    def get_treasury_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current treasury state
        
        Returns:
            Dictionary with summary information
        """
        runway = self.calculate_sustainability_runway()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_assets": len(self.balances),
            "total_usd_value": str(self.get_total_usd_value()),
            "balances": {
                asset_type.value: balance.to_dict()
                for asset_type, balance in self.balances.items()
            },
            "sustainability_runway": runway.to_dict(),
            "health_status": runway.health_status.value,
            "total_snapshots": len(self.snapshots)
        }
