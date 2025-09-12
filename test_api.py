import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_home_endpoint():
    """Test the home endpoint"""
    print("Testing home endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_get_users():
    """Test getting list of mock users"""
    print("Testing get users endpoint...")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_login_success():
    """Test successful login"""
    print("Testing successful login...")
    login_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print("-" * 50)
    return result.get("token") if response.status_code == 200 else None

def test_login_failure():
    """Test failed login with wrong credentials"""
    print("Testing failed login...")
    login_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_protected_route_without_token():
    """Test accessing protected route without token"""
    print("Testing protected route without token...")
    response = requests.get(f"{BASE_URL}/protected")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_protected_route_with_token(token):
    """Test accessing protected route with valid token"""
    print("Testing protected route with valid token...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_logout(token):
    """Test logout endpoint"""
    print("Testing logout endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("FLASK API MOCK LOGIN TESTS")
    print("=" * 60)
    
    try:
        # Test public endpoints
        test_home_endpoint()
        test_get_users()
        
        # Test login functionality
        test_login_failure()
        token = test_login_success()
        
        if token:
            # Test protected routes
            test_protected_route_without_token()
            test_protected_route_with_token(token)
            test_logout(token)
        else:
            print("❌ Could not get token, skipping protected route tests")
        
        print("=" * 60)
        print("TESTS COMPLETED")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python app.py")

if __name__ == "__main__":
    run_all_tests()
