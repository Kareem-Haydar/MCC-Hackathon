#!/usr/bin/env python3
"""
Test script for the Event Planner API
Run the API server first: python -m app.main
Then run this script: python test_api.py
"""

import requests
import json
from time import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_plan_event_simple():
    """Test event planning with a simple request"""
    print("\n" + "="*60)
    print("Testing Event Planning - Simple Iftar")
    print("="*60)
    
    payload = {
        "prompt": "Community iftar in New York City for 100 people on a budget of 10 thousand dollars, indian food preferred",
        "result_count": 5,
        "radius": 15000
    }
    
    print(f"\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    start_time = time()
    response = requests.post(f"{BASE_URL}/api/plan-event", json=payload)
    elapsed = time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Time: {elapsed:.2f} seconds")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nVenues Found: {len(data.get('venues', {}).get('recommended_venues', []))}")
        print(f"Catering Options: {len(data.get('catering', []))}")
        
        print("\n--- Recommended Venues ---")
        for venue in data.get('venues', {}).get('recommended_venues', [])[:3]:
            print(f"\n  • {venue['name']}")
            print(f"    Address: {venue['address']}")
            print(f"    Rating: {venue['rating']}")
            print(f"    Why: {venue['why_recommended'][:100]}...")
        
        print("\n--- Recommended Catering ---")
        for catering_group in data.get('catering', [])[:2]:
            for caterer in catering_group.get('recommended_catering', [])[:2]:
                print(f"\n  • {caterer['name']}")
                print(f"    Address: {caterer['address']}")
                print(f"    Rating: {caterer['rating']}")
                print(f"    Dietary: {', '.join(caterer.get('dietary_support', []))}")
        
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_plan_event_wedding():
    """Test event planning with a wedding request"""
    print("\n" + "="*60)
    print("Testing Event Planning - Wedding")
    print("="*60)
    
    payload = {
        "prompt": "Wedding in San Francisco for 200 people with a budget of 30000 dollars, need Pakistani and Arab food, halal required",
        "result_count": 8,
        "radius": 25000
    }
    
    print(f"\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    start_time = time()
    response = requests.post(f"{BASE_URL}/api/plan-event", json=payload)
    elapsed = time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Time: {elapsed:.2f} seconds")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nVenues Found: {len(data.get('venues', {}).get('recommended_venues', []))}")
        print(f"Catering Options: {len(data.get('catering', []))}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_invalid_request():
    """Test with invalid request"""
    print("\n" + "="*60)
    print("Testing Invalid Request")
    print("="*60)
    
    payload = {
        "prompt": "",  # Empty prompt
        "result_count": 5
    }
    
    response = requests.post(f"{BASE_URL}/api/plan-event", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    return response.status_code >= 400

def main():
    print("\n" + "="*60)
    print("Event Planner API Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    
    # Check if server is running
    try:
        requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: API server is not running!")
        print("Start the server first with: python -m app.main")
        return
    
    results = {
        "Health Check": test_health_check(),
        "Simple Event (Iftar)": test_plan_event_simple(),
        "Wedding Event": test_plan_event_wedding(),
        "Invalid Request": test_invalid_request()
    }
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n")

if __name__ == "__main__":
    main()
