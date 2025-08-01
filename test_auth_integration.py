#!/usr/bin/env python3
"""
Test integration for admin authentication and tutor nomination features.
Tests both API endpoints and overall system integration.
"""

import requests
import json
import sys
from time import sleep

# Test configuration
BASE_URL = "http://127.0.0.1:5001"
session = requests.Session()

def test_auth_status_no_auth():
    """Test authentication status endpoint without authentication"""
    print("Testing auth status without authentication...")
    response = session.get(f"{BASE_URL}/api/auth/status")
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] == False
    print("✓ Auth status correctly returns unauthenticated")

def test_admin_login_invalid():
    """Test login with invalid credentials"""
    print("Testing login with invalid credentials...")
    response = session.post(f"{BASE_URL}/api/auth/login", json={
        "username": "invalid_user",
        "password": "wrong_password"
    })
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    print("✓ Invalid login correctly rejected")

def test_admin_login_valid():
    """Test login with valid seed_bringer credentials"""
    print("Testing login with valid seed_bringer credentials...")
    response = session.post(f"{BASE_URL}/api/auth/login", json={
        "username": "seed_bringer",
        "password": "euystacio_genesis_2025"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["user"]["role"] == "seed_bringer"
    assert data["user"]["display_name"] == "Seed Bringer (bioarchitettura)"
    print("✓ Valid login successful")
    return response

def test_auth_status_with_auth():
    """Test authentication status after login"""
    print("Testing auth status with authentication...")
    response = session.get(f"{BASE_URL}/api/auth/status")
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] == True
    assert data["user"]["role"] == "seed_bringer"
    print("✓ Auth status correctly returns authenticated user")

def test_tutor_nomination_without_auth():
    """Test tutor nomination without authentication (should fail)"""
    print("Testing tutor nomination without authentication...")
    # Create a new session without auth
    no_auth_session = requests.Session()
    response = no_auth_session.post(f"{BASE_URL}/api/nominate_tutor", json={
        "name": "Unauthorized Test",
        "reason": "This should fail"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["authenticated"] == False
    print("✓ Tutor nomination correctly rejected without auth")

def test_tutor_nomination_with_auth():
    """Test tutor nomination with authentication"""
    print("Testing tutor nomination with authentication...")
    response = session.post(f"{BASE_URL}/api/nominate_tutor", json={
        "name": "Maria Santos",
        "reason": "Exceptional empathy and wisdom in guiding AI-human symbiosis",
        "spi_data": {
            "credentials": {
                "compassion_score": 0.9,
                "planetary_balance": 0.8,
                "listening_willingness": 0.85,
                "ai_alignment_score": 0.8
            }
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nomination_successful"] == True
    assert data["name"] == "Maria Santos"
    assert data["nominated_by"] == "Seed Bringer (bioarchitettura)"
    assert "tutor_fid" in data
    print("✓ Tutor nomination successful with auth")
    return data

def test_cofounder_login():
    """Test login with cofounder credentials"""
    print("Testing cofounder login...")
    response = session.post(f"{BASE_URL}/api/auth/login", json={
        "username": "cofounder_hannes",
        "password": "hannes_cofounder_2025"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["user"]["role"] == "cofounder"
    assert data["user"]["display_name"] == "Hannes Mitterer"
    print("✓ Cofounder login successful")

def test_cofounder_tutor_nomination():
    """Test tutor nomination as cofounder"""
    print("Testing tutor nomination as cofounder...")
    response = session.post(f"{BASE_URL}/api/nominate_tutor", json={
        "name": "Dr. Elena Rodriguez",
        "reason": "Leading expert in ethical AI development and human-computer interaction"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nomination_successful"] == True
    assert data["nominated_by"] == "Hannes Mitterer"
    print("✓ Cofounder tutor nomination successful")

def test_logout():
    """Test logout functionality"""
    print("Testing logout...")
    response = session.post(f"{BASE_URL}/api/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print("✓ Logout successful")

def test_auth_status_after_logout():
    """Test authentication status after logout"""
    print("Testing auth status after logout...")
    response = session.get(f"{BASE_URL}/api/auth/status")
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] == False
    print("✓ Auth status correctly returns unauthenticated after logout")

def test_tutors_api():
    """Test the tutors API to see nominated tutors"""
    print("Testing tutors API...")
    response = session.get(f"{BASE_URL}/api/tutors")
    assert response.status_code == 200
    data = response.json()
    assert "all_tutors" in data
    assert "active_circle" in data
    print(f"✓ Tutors API working - {len(data['all_tutors'])} tutors, {len(data['active_circle'])} active")

def run_tests():
    """Run all integration tests"""
    print("🌳 Starting Euystacio Admin Authentication & Tutor Nomination Integration Tests")
    print("=" * 80)
    
    try:
        # Test without authentication
        test_auth_status_no_auth()
        test_admin_login_invalid()
        test_tutor_nomination_without_auth()
        
        # Test with seed_bringer authentication
        test_admin_login_valid()
        test_auth_status_with_auth()
        test_tutor_nomination_with_auth()
        
        # Test cofounder authentication
        test_cofounder_login()
        test_cofounder_tutor_nomination()
        
        # Test logout
        test_logout()
        test_auth_status_after_logout()
        
        # Test other APIs
        test_tutors_api()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! The admin authentication and tutor nomination system is working correctly.")
        print("\nFeatures verified:")
        print("✓ Admin login/logout functionality")
        print("✓ Session-based authentication")
        print("✓ Role-based access control (seed_bringer & cofounder)")
        print("✓ Protected tutor nomination endpoints")
        print("✓ Proper authentication error handling")
        print("✓ Integration with existing tutor nomination system")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR: Flask app not running on http://127.0.0.1:5001")
        print("Please start the app with: python app.py")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)