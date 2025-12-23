"""
test_apollo_assistant.py
Test Suite for Apollo Assistant

Tests:
- Command parsing and categorization
- Balance queries
- Treasury queries
- Longevity metrics
- Health status queries
- Help system
"""

import sys
import os
from decimal import Decimal

# Ensure the parent directory is in the path for proper imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from apollo_assistant import ApolloAssistant, CommandCategory
from core.treasury_manager import TreasuryManager, TreasuryAssetType


class TestApolloAssistant:
    """Tests for Apollo Assistant"""
    
    def setup_treasury(self):
        """Set up a treasury manager with test data"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("5000"))
        
        # Add BTC balance
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("2.0"),
            Decimal("80000"),
            blockchain_address="bc1q...",
            confirmation_count=6
        )
        
        # Add ETH balance
        manager.update_balance(
            TreasuryAssetType.ETH,
            Decimal("10.0"),
            Decimal("20000"),
            blockchain_address="0x...",
            confirmation_count=12
        )
        
        return manager
    
    def test_initialization(self):
        """Test Apollo Assistant initialization"""
        manager = TreasuryManager()
        assistant = ApolloAssistant(manager)
        
        assert assistant.treasury_manager is manager
        assert len(assistant.command_patterns) > 0
        
        print("✅ test_initialization passed")
    
    def test_balance_query_btc(self):
        """Test BTC balance query"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("show BTC balance")
        
        assert response.success is True
        assert response.category == CommandCategory.BALANCE
        assert "BTC" in response.message
        assert "2.0" in response.message or "2" in response.message
        assert response.data["asset_type"] == "BTC"
        
        print("✅ test_balance_query_btc passed")
    
    def test_balance_query_eth(self):
        """Test ETH balance query"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("show ETH balance")
        
        assert response.success is True
        assert response.category == CommandCategory.BALANCE
        assert "ETH" in response.message
        assert response.data["asset_type"] == "ETH"
        
        print("✅ test_balance_query_eth passed")
    
    def test_balance_query_all(self):
        """Test query for all balances"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("show balance")
        
        assert response.success is True
        assert response.category == CommandCategory.BALANCE
        assert "BTC" in response.message
        assert "ETH" in response.message
        assert "Total Value" in response.message
        
        print("✅ test_balance_query_all passed")
    
    def test_balance_query_natural_language(self):
        """Test natural language balance queries"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        # Test variations
        commands = [
            "what's the bitcoin balance",
            "get ethereum balance",
            "what is our balance",
        ]
        
        for cmd in commands:
            response = assistant.process_command(cmd)
            assert response.success is True
            assert response.category == CommandCategory.BALANCE
        
        print("✅ test_balance_query_natural_language passed")
    
    def test_treasury_query(self):
        """Test treasury summary query"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("show treasury")
        
        assert response.success is True
        assert response.category == CommandCategory.TREASURY
        assert "Treasury Summary" in response.message
        assert "Total Value" in response.message
        assert "Health Status" in response.message
        
        print("✅ test_treasury_query passed")
    
    def test_longevity_query(self):
        """Test project longevity query"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("project longevity")
        
        assert response.success is True
        assert response.category == CommandCategory.LONGEVITY
        assert "Longevity Metrics" in response.message
        assert "Runway" in response.message or "runway" in response.message
        
        print("✅ test_longevity_query passed")
    
    def test_longevity_natural_language(self):
        """Test natural language longevity queries"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        commands = [
            "how long can we last",
            "sustainability runway",
            "when will we run out",
        ]
        
        for cmd in commands:
            response = assistant.process_command(cmd)
            assert response.success is True
            assert response.category == CommandCategory.LONGEVITY
        
        print("✅ test_longevity_natural_language passed")
    
    def test_health_query(self):
        """Test treasury health query"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("treasury health")
        
        assert response.success is True
        assert response.category == CommandCategory.HEALTH
        assert "Health" in response.message
        assert "Runway" in response.message
        
        print("✅ test_health_query passed")
    
    def test_health_query_variations(self):
        """Test health query variations"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        commands = [
            "health check",
            "is the treasury healthy",
            "financial health",
        ]
        
        for cmd in commands:
            response = assistant.process_command(cmd)
            assert response.success is True
            assert response.category == CommandCategory.HEALTH
        
        print("✅ test_health_query_variations passed")
    
    def test_help_command(self):
        """Test help command"""
        manager = TreasuryManager()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("help")
        
        assert response.success is True
        assert response.category == CommandCategory.HELP
        assert "Available Commands" in response.message
        assert "Balance Queries" in response.message
        
        print("✅ test_help_command passed")
    
    def test_unknown_command(self):
        """Test unknown command handling"""
        manager = TreasuryManager()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("do something random")
        
        assert response.success is False
        assert response.category == CommandCategory.UNKNOWN
        assert "didn't understand" in response.message.lower()
        
        print("✅ test_unknown_command passed")
    
    def test_empty_balance_query(self):
        """Test balance query with no data"""
        manager = TreasuryManager()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("show BTC balance")
        
        assert response.success is False
        assert "No BTC balance data available" in response.message
        
        print("✅ test_empty_balance_query passed")
    
    def test_command_suggestions(self):
        """Test getting command suggestions"""
        manager = TreasuryManager()
        assistant = ApolloAssistant(manager)
        
        suggestions = assistant.get_command_suggestions()
        
        assert len(suggestions) > 0
        assert "show BTC balance" in suggestions
        assert "help" in suggestions
        
        print("✅ test_command_suggestions passed")
    
    def test_response_includes_timestamp(self):
        """Test that all responses include timestamp"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        commands = [
            "show BTC balance",
            "treasury health",
            "project longevity",
            "help",
        ]
        
        for cmd in commands:
            response = assistant.process_command(cmd)
            assert response.timestamp is not None
            assert len(response.timestamp) > 0
        
        print("✅ test_response_includes_timestamp passed")
    
    def test_health_status_emojis(self):
        """Test health status includes appropriate indicators"""
        manager = TreasuryManager(default_burn_rate_usd=Decimal("1000"))
        
        # Create healthy treasury
        manager.update_balance(
            TreasuryAssetType.BTC,
            Decimal("10.0"),
            Decimal("400000")
        )
        
        assistant = ApolloAssistant(manager)
        response = assistant.process_command("treasury health")
        
        assert response.success is True
        # Should have a positive emoji for healthy status
        assert "✅" in response.message or "HEALTHY" in response.message
        
        print("✅ test_health_status_emojis passed")
    
    def test_case_insensitive_commands(self):
        """Test that commands are case-insensitive"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        commands = [
            "SHOW BTC BALANCE",
            "Show Treasury",
            "TrEaSuRy HeAlTh",
        ]
        
        for cmd in commands:
            response = assistant.process_command(cmd)
            assert response.success is True
        
        print("✅ test_case_insensitive_commands passed")
    
    def test_command_with_extra_whitespace(self):
        """Test commands with extra whitespace"""
        manager = self.setup_treasury()
        assistant = ApolloAssistant(manager)
        
        response = assistant.process_command("  show   BTC   balance  ")
        
        assert response.success is True
        assert response.category == CommandCategory.BALANCE
        
        print("✅ test_command_with_extra_whitespace passed")


def run_all_tests():
    """Run all Apollo Assistant tests"""
    print("\n" + "="*60)
    print("🧪 Running Apollo Assistant Test Suite")
    print("="*60 + "\n")
    
    test_suite = TestApolloAssistant()
    
    print("🤖 Apollo Assistant Tests:")
    print("-" * 40)
    
    tests = [
        test_suite.test_initialization,
        test_suite.test_balance_query_btc,
        test_suite.test_balance_query_eth,
        test_suite.test_balance_query_all,
        test_suite.test_balance_query_natural_language,
        test_suite.test_treasury_query,
        test_suite.test_longevity_query,
        test_suite.test_longevity_natural_language,
        test_suite.test_health_query,
        test_suite.test_health_query_variations,
        test_suite.test_help_command,
        test_suite.test_unknown_command,
        test_suite.test_empty_balance_query,
        test_suite.test_command_suggestions,
        test_suite.test_response_includes_timestamp,
        test_suite.test_health_status_emojis,
        test_suite.test_case_insensitive_commands,
        test_suite.test_command_with_extra_whitespace,
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
