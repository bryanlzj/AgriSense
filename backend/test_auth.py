"""
Test script for authentication endpoints.

This script tests the complete authentication flow:
1. Register a new user
2. Login to get JWT token
3. Use token to access protected endpoint

Usage:
    python test_auth.py

Note: Requires the FastAPI server to be running on http://localhost:8000
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_authentication_flow():
    """Test the complete authentication flow."""
    print("=" * 60)
    print("Testing Authentication Flow")
    print("=" * 60)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testfarmer",
        "password": "TestPassword123!",
        "full_name": "Test Farmer",
        "phone_number": "+1234567890",
        "farm_location": "Test Farm, Test Region"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Registration successful!")
            print(f"User ID: {user_data['id']}")
            print(f"Username: {user_data['username']}")
            print(f"Full Name: {user_data['full_name']}")
        elif response.status_code == 400:
            print(f"⚠️  User already exists (this is expected if running multiple times)")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.json()}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running on http://localhost:8000?")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "username": "testfarmer",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"✅ Login successful!")
            print(f"Token Type: {token_data['token_type']}")
            print(f"Access Token: {access_token[:50]}...")
        else:
            print(f"❌ Login failed: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Get current user (protected endpoint)
    print("\n3. Testing Protected Endpoint (Get Current User)...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Successfully accessed protected endpoint!")
            print(f"User ID: {user_data['id']}")
            print(f"Username: {user_data['username']}")
            print(f"Full Name: {user_data['full_name']}")
            print(f"Phone: {user_data['phone_number']}")
            print(f"Farm Location: {user_data['farm_location']}")
            print(f"Created At: {user_data['created_at']}")
        else:
            print(f"❌ Failed to access protected endpoint: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 4: Test invalid token
    print("\n4. Testing Invalid Token...")
    invalid_headers = {
        "Authorization": "Bearer invalid_token_here"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=invalid_headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"✅ Invalid token correctly rejected!")
            print(f"Error: {response.json()}")
        else:
            print(f"⚠️  Unexpected response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ All Authentication Tests Completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_authentication_flow()
