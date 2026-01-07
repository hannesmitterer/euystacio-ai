"""
apollo_assistant.py
Apollo Assistant Framework for Euystacio AI

This module provides:
- User command interface for treasury inquiries
- Project longevity metrics queries
- Integration with Seedbringer Treasury system
- Natural language command processing

Aligned with NSR and OLF principles.
"""

import re
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

from core.treasury_manager import (
    TreasuryManager,
    TreasuryAssetType,
    TreasuryHealthStatus
)


class CommandCategory(Enum):
    """Categories of Apollo Assistant commands"""
    TREASURY = "TREASURY"
    LONGEVITY = "LONGEVITY"
    BALANCE = "BALANCE"
    HEALTH = "HEALTH"
    HELP = "HELP"
    UNKNOWN = "UNKNOWN"


@dataclass
class CommandResponse:
    """Response from Apollo Assistant command"""
    success: bool
    category: CommandCategory
    message: str
    data: Dict[str, Any]
    timestamp: str


class ApolloAssistant:
    """
    Apollo Assistant - User Interface for Treasury and Longevity Metrics
    
    Provides natural language command interface for querying treasury data,
    project sustainability, and longevity metrics.
    """
    
    def __init__(self, treasury_manager: TreasuryManager):
        """
        Initialize Apollo Assistant
        
        Args:
            treasury_manager: TreasuryManager instance for data queries
        """
        self.treasury_manager = treasury_manager
        self.command_patterns = self._initialize_command_patterns()
        
    def _initialize_command_patterns(self) -> Dict[CommandCategory, List[str]]:
        """Initialize regex patterns for command recognition"""
        return {
            CommandCategory.BALANCE: [
                r"(?:show|get|what(?:'s| is)?)\s+(?:the\s+)?(?:btc|bitcoin)\s+balance",
                r"(?:show|get|what(?:'s| is)?)\s+(?:the\s+)?(?:eth|ethereum)\s+balance",
                r"(?:show|get|what(?:'s| is)?)\s+(?:my|our|the|all)?\s*balances?",
                r"balance\s+(?:of\s+)?(?:btc|eth|bitcoin|ethereum)",
                r"^balances?$",
            ],
            CommandCategory.TREASURY: [
                r"(?:show|get|what(?:'s| is)?)\s+(?:the\s+)?treasury",
                r"treasury\s+(?:summary|status|overview|data)",
                r"(?:total\s+)?treasury\s+value",
            ],
            CommandCategory.LONGEVITY: [
                r"(?:how\s+)?long\s+(?:can|will)\s+(?:we|the project)\s+(?:last|survive)",
                r"(?:project\s+)?(?:longevity|sustainability|runway)",
                r"(?:when\s+)?(?:will|do)\s+(?:we|the treasury)\s+run\s+out",
                r"(?:how\s+many\s+)?(?:months|days)\s+(?:left|remaining)",
            ],
            CommandCategory.HEALTH: [
                r"(?:treasury\s+)?health\s*(?:status|check)?",
                r"(?:is\s+)?(?:the\s+)?treasury\s+(?:healthy|ok|fine)",
                r"financial\s+(?:health|status)",
            ],
            CommandCategory.HELP: [
                r"^help$",
                r"(?:what\s+)?commands",
                r"(?:how\s+)?(?:do\s+)?(?:i\s+)?use",
            ],
        }
    
    def process_command(self, command: str) -> CommandResponse:
        """
        Process a natural language command
        
        Args:
            command: User command string
            
        Returns:
            CommandResponse with result
        """
        from datetime import datetime, timezone
        
        command_lower = command.lower().strip()
        category = self._categorize_command(command_lower)
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Route to appropriate handler
        if category == CommandCategory.BALANCE:
            return self._handle_balance_query(command_lower, timestamp)
        elif category == CommandCategory.TREASURY:
            return self._handle_treasury_query(timestamp)
        elif category == CommandCategory.LONGEVITY:
            return self._handle_longevity_query(timestamp)
        elif category == CommandCategory.HEALTH:
            return self._handle_health_query(timestamp)
        elif category == CommandCategory.HELP:
            return self._handle_help_query(timestamp)
        else:
            return CommandResponse(
                success=False,
                category=CommandCategory.UNKNOWN,
                message="I didn't understand that command. Try 'help' for available commands.",
                data={},
                timestamp=timestamp
            )
    
    def _categorize_command(self, command: str) -> CommandCategory:
        """Categorize command using pattern matching"""
        for category, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return category
        return CommandCategory.UNKNOWN
    
    def _handle_balance_query(self, command: str, timestamp: str) -> CommandResponse:
        """Handle balance query commands"""
        # Determine which asset is being queried
        if re.search(r"btc|bitcoin", command):
            asset_type = TreasuryAssetType.BTC
        elif re.search(r"eth|ethereum", command):
            asset_type = TreasuryAssetType.ETH
        else:
            # Show all balances
            return self._handle_all_balances(timestamp)
        
        balance = self.treasury_manager.get_balance(asset_type)
        
        if not balance:
            return CommandResponse(
                success=False,
                category=CommandCategory.BALANCE,
                message=f"No {asset_type.value} balance data available.",
                data={"asset_type": asset_type.value},
                timestamp=timestamp
            )
        
        message = self._format_balance_message(balance)
        
        return CommandResponse(
            success=True,
            category=CommandCategory.BALANCE,
            message=message,
            data=balance.to_dict(),
            timestamp=timestamp
        )
    
    def _handle_all_balances(self, timestamp: str) -> CommandResponse:
        """Handle query for all balances"""
        balances = list(self.treasury_manager.balances.values())
        
        if not balances:
            return CommandResponse(
                success=False,
                category=CommandCategory.BALANCE,
                message="No balance data available.",
                data={},
                timestamp=timestamp
            )
        
        total_usd = self.treasury_manager.get_total_usd_value()
        
        message_lines = ["Current Treasury Balances:"]
        for balance in balances:
            message_lines.append(
                f"  • {balance.asset_type.value}: {balance.amount} "
                f"(${balance.usd_value:,.2f} USD)"
            )
        message_lines.append(f"\nTotal Value: ${total_usd:,.2f} USD")
        
        return CommandResponse(
            success=True,
            category=CommandCategory.BALANCE,
            message="\n".join(message_lines),
            data={
                "balances": [b.to_dict() for b in balances],
                "total_usd": str(total_usd)
            },
            timestamp=timestamp
        )
    
    def _handle_treasury_query(self, timestamp: str) -> CommandResponse:
        """Handle treasury summary query"""
        summary = self.treasury_manager.get_treasury_summary()
        
        message_lines = [
            "Treasury Summary:",
            f"  • Total Assets: {summary['total_assets']}",
            f"  • Total Value: ${Decimal(summary['total_usd_value']):,.2f} USD",
            f"  • Health Status: {summary['health_status']}",
            f"  • Runway: {summary['sustainability_runway']['runway_days']} days "
            f"({Decimal(summary['sustainability_runway']['runway_months']):.1f} months)"
        ]
        
        return CommandResponse(
            success=True,
            category=CommandCategory.TREASURY,
            message="\n".join(message_lines),
            data=summary,
            timestamp=timestamp
        )
    
    def _handle_longevity_query(self, timestamp: str) -> CommandResponse:
        """Handle project longevity/sustainability query"""
        runway = self.treasury_manager.calculate_sustainability_runway()
        
        message_lines = [
            "Project Longevity Metrics:",
            f"  • Treasury Balance: ${runway.total_treasury_usd:,.2f} USD",
            f"  • Monthly Burn Rate: ${runway.monthly_burn_rate_usd:,.2f} USD",
            f"  • Sustainability Runway: {runway.runway_days} days ({runway.runway_months:.1f} months)",
            f"  • Health Status: {runway.health_status.value}"
        ]
        
        if runway.projected_depletion_date:
            message_lines.append(
                f"  • Projected Depletion: {runway.projected_depletion_date[:10]}"
            )
        
        # Add health interpretation
        if runway.health_status == TreasuryHealthStatus.CRITICAL:
            message_lines.append(
                "\n⚠️ CRITICAL: Immediate action required to secure funding."
            )
        elif runway.health_status == TreasuryHealthStatus.WARNING:
            message_lines.append(
                "\n⚡ WARNING: Treasury runway below recommended threshold."
            )
        elif runway.health_status == TreasuryHealthStatus.MODERATE:
            message_lines.append(
                "\n✓ MODERATE: Treasury in acceptable range, monitor closely."
            )
        else:
            message_lines.append(
                "\n✓ HEALTHY: Treasury well-funded for sustainable operations."
            )
        
        return CommandResponse(
            success=True,
            category=CommandCategory.LONGEVITY,
            message="\n".join(message_lines),
            data=runway.to_dict(),
            timestamp=timestamp
        )
    
    def _handle_health_query(self, timestamp: str) -> CommandResponse:
        """Handle treasury health status query"""
        runway = self.treasury_manager.calculate_sustainability_runway()
        
        health_emoji = {
            TreasuryHealthStatus.HEALTHY: "✅",
            TreasuryHealthStatus.MODERATE: "⚡",
            TreasuryHealthStatus.WARNING: "⚠️",
            TreasuryHealthStatus.CRITICAL: "🚨"
        }
        
        emoji = health_emoji.get(runway.health_status, "❓")
        
        message = (
            f"{emoji} Treasury Health: {runway.health_status.value}\n"
            f"Runway: {runway.runway_days} days remaining"
        )
        
        return CommandResponse(
            success=True,
            category=CommandCategory.HEALTH,
            message=message,
            data={"health_status": runway.health_status.value, "runway_days": runway.runway_days},
            timestamp=timestamp
        )
    
    def _handle_help_query(self, timestamp: str) -> CommandResponse:
        """Handle help command"""
        help_text = """
Apollo Assistant - Available Commands:

💰 Balance Queries:
  • "show BTC balance" - View Bitcoin balance
  • "show ETH balance" - View Ethereum balance
  • "show balance" - View all asset balances

📊 Treasury Queries:
  • "show treasury" - View complete treasury summary
  • "treasury status" - View treasury overview

📈 Longevity Metrics:
  • "project longevity" - View sustainability runway
  • "how long can we last" - Project timeline
  • "sustainability runway" - Detailed metrics

💚 Health Status:
  • "treasury health" - View current health status
  • "health check" - Quick health assessment

❓ Help:
  • "help" - Show this message
  • "commands" - List available commands
"""
        
        return CommandResponse(
            success=True,
            category=CommandCategory.HELP,
            message=help_text.strip(),
            data={"available_categories": [cat.value for cat in CommandCategory]},
            timestamp=timestamp
        )
    
    def _format_balance_message(self, balance) -> str:
        """Format a balance into a readable message"""
        return (
            f"{balance.asset_type.value} Balance:\n"
            f"  • Amount: {balance.amount}\n"
            f"  • USD Value: ${balance.usd_value:,.2f}\n"
            f"  • Last Updated: {balance.last_updated[:19]}\n"
            f"  • Confirmations: {balance.confirmation_count}"
        )
    
    def get_command_suggestions(self) -> List[str]:
        """Get list of example commands"""
        return [
            "show BTC balance",
            "show ETH balance",
            "show treasury",
            "project longevity",
            "treasury health",
            "how long can we last",
            "help"
        ]
