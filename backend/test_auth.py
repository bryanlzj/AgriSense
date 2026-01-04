"""
Quick test script for authentication endpoints.
Run after starting the server with: python run.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_auth_flow():
    """Test complete authentication flow."""
    
    print("=" * 60)
    print("TESTING AUTHENTICATION ENDPOINTS")
    print("=" * 60)
    
    # Test 1: Register new user
    print("\n1. Testing Registration...")
    register_data = {
        "username": "test_farmer",
        "password": "testpass123",
        "full_name": "Test Farmer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
        else:
            print("   ⚠️  Registration failed or user already exists")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing Login...")
    login_data = {
        "username": "test_farmer",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,  # OAuth2PasswordRequestForm expects form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("   ✅ Login successful!")
            print(f"   Token (first 50 chars): {token[:50]}...")
        else:
            print("   ❌ Login failed")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Get current user
    print("\n3. Testing Get Current User...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("   ✅ Get current user successful!")
        else:
            print("   ❌ Get current user failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 4: Invalid token
    print("\n4. Testing Invalid Token...")
    headers = {
        "Authorization": "Bearer invalid_token_here"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("   ✅ Invalid token correctly rejected!")
        else:
            print("   ⚠️  Expected 401 status")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the server is running: python run.py")
    print("Press Enter to start tests...")
    input()
    test_auth_flow()
