#!/usr/bin/env python3
"""Test runner for all tests."""
import sys
import os
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set test environment
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

def run_basic_tests():
    """Run basic functionality tests."""
    print("=" * 60)
    print("Running Basic Functionality Tests")
    print("=" * 60)
    
    from decimal import Decimal
    from src.economics.core.house_edge import HouseEdgeCalculator
    from src.economics.core.commission_calculator import CommissionCalculator
    from src.economics.core.bonus_calculator import BonusCalculator
    from src.economics.limits.bet_limits import BetLimits
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: House edge calculation
    try:
        calc = HouseEdgeCalculator(Decimal('0.01'))
        result = calc.calculate_expected_multiplier(Decimal('2.0'))
        assert result == Decimal('1.98'), f'Expected 1.98, got {result}'
        print('✓ Test 1: House edge calculation')
        tests_passed += 1
    except Exception as e:
        print(f'✗ Test 1 failed: {e}')
        tests_failed += 1
    
    # Test 2: Commission calculation
    try:
        comm_calc = CommissionCalculator()
        commission = comm_calc.calculate_withdrawal_commission(Decimal('100.0'), 'TON')
        assert commission >= Decimal('0.1'), f'Commission too low: {commission}'
        print('✓ Test 2: Commission calculation')
        tests_passed += 1
    except Exception as e:
        print(f'✗ Test 2 failed: {e}')
        tests_failed += 1
    
    # Test 3: Bonus calculation
    try:
        bonus_calc = BonusCalculator()
        bonus = bonus_calc.calculate_first_deposit_bonus(Decimal('10.0'), 'TON')
        assert bonus == Decimal('1.0'), f'Expected 1.0, got {bonus}'
        print('✓ Test 3: Bonus calculation')
        tests_passed += 1
    except Exception as e:
        print(f'✗ Test 3 failed: {e}')
        tests_failed += 1
    
    # Test 4: Bet limits validation
    try:
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal('0.01'), 'TON')
        assert is_valid, f'Validation failed: {error}'
        print('✓ Test 4: Bet limits validation')
        tests_passed += 1
    except Exception as e:
        print(f'✗ Test 4 failed: {e}')
        tests_failed += 1
    
    print(f"\nBasic Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed


def run_database_tests():
    """Run database integration tests."""
    print("\n" + "=" * 60)
    print("Running Database Integration Tests")
    print("=" * 60)
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.database.connection import Base
    from src.database.repositories.user_repo import UserRepository
    from src.economics.bonuses import BonusManager
    from src.economics.referrals import ReferralManager
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        # Create test database
        engine = create_engine('sqlite:///./test_integration.db')
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Test 1: User creation
        try:
            user_repo = UserRepository(db)
            user = user_repo.create(
                telegram_user_id=999999999,
                username='testuser',
            )
            assert user.id is not None
            print('✓ Test 1: User creation')
            tests_passed += 1
        except Exception as e:
            print(f'✗ Test 1 failed: {e}')
            tests_failed += 1
        
        # Test 2: Bonus manager
        try:
            bonus_manager = BonusManager(db)
            bonuses = bonus_manager.get_available_bonuses(user.id, 'TON')
            assert isinstance(bonuses, dict)
            print('✓ Test 2: Bonus manager')
            tests_passed += 1
        except Exception as e:
            print(f'✗ Test 2 failed: {e}')
            tests_failed += 1
        
        # Test 3: Referral manager
        try:
            referral_manager = ReferralManager(db)
            code = referral_manager.create_referral_code(user.id)
            assert code is not None
            assert len(code) == 8
            print('✓ Test 3: Referral manager')
            tests_passed += 1
        except Exception as e:
            print(f'✗ Test 3 failed: {e}')
            tests_failed += 1
        
        db.close()
        
        # Clean up
        if os.path.exists('./test_integration.db'):
            os.remove('./test_integration.db')
        
    except Exception as e:
        print(f'✗ Database setup failed: {e}')
        tests_failed += 1
    
    print(f"\nDatabase Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed


def run_economics_tests():
    """Run economics module tests."""
    print("\n" + "=" * 60)
    print("Running Economics Module Tests")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test imports
    modules_to_test = [
        ('HouseEdgeCalculator', 'src.economics.core.house_edge'),
        ('CommissionCalculator', 'src.economics.core.commission_calculator'),
        ('BonusCalculator', 'src.economics.core.bonus_calculator'),
        ('PayoutCalculator', 'src.economics.core.payout_calculator'),
        ('ProfitTracker', 'src.economics.core.profit_tracker'),
        ('BonusManager', 'src.economics.bonuses'),
        ('ReferralManager', 'src.economics.referrals'),
        ('BetLimits', 'src.economics.limits'),
        ('MultiplierDistribution', 'src.economics.game'),
    ]
    
    for module_name, module_path in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[module_name])
            cls = getattr(module, module_name)
            assert cls is not None
            print(f'✓ {module_name} imports successfully')
            tests_passed += 1
        except Exception as e:
            print(f'✗ {module_name} import failed: {e}')
            tests_failed += 1
    
    print(f"\nEconomics Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CRASH GAME - TEST SUITE")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    # Run test suites
    passed, failed = run_basic_tests()
    total_passed += passed
    total_failed += failed
    
    passed, failed = run_database_tests()
    total_passed += passed
    total_failed += failed
    
    passed, failed = run_economics_tests()
    total_passed += passed
    total_failed += failed
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests Passed: {total_passed}")
    print(f"Total Tests Failed: {total_failed}")
    print(f"Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%")
    print("=" * 60)
    
    if total_failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total_failed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
