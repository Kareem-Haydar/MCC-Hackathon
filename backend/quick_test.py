#!/usr/bin/env python3
"""Quick API test - simpler version"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("="*60)
print("Quick API Test")
print("="*60)

# 1. Health check
print("\n1. Testing health endpoint...")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# 2. Test event planning
print("\n2. Testing event planning...")
print("   (This may take 30-60 seconds...)")

payload = {
    "prompt": "Community iftar in New York City for 50 people on a budget of 5000 dollars, prefer Pakistani food",
    "result_count": 5,
    "radius": 15000
}

response = requests.post(f"{BASE_URL}/api/plan-event", json=payload)

if response.status_code == 200:
    data = response.json()
    
    print(f"\n   ✅ Success!")
    print(f"\n   Venues recommended: {len(data['venues']['recommended_venues'])}")
    
    if data['venues']['recommended_venues']:
        venue = data['venues']['recommended_venues'][0]
        print(f"\n   Top Venue:")
        print(f"   - Name: {venue['name']}")
        print(f"   - Address: {venue['address']}")
        print(f"   - Rating: {venue['rating']}")
    
    print(f"\n   Catering groups: {len(data['catering'])}")
    
    if data['catering'] and data['catering'][0].get('recommended_catering'):
        caterer = data['catering'][0]['recommended_catering'][0]
        print(f"\n   Top Caterer:")
        print(f"   - Name: {caterer['name']}")
        print(f"   - Rating: {caterer['rating']}")
        print(f"   - Dietary Support: {', '.join(caterer['dietary_support'])}")
    
else:
    print(f"\n   ❌ Error: {response.status_code}")
    print(f"   {response.text}")

print("\n" + "="*60)
print("Test Complete!")
print("="*60)
print("\nNext steps:")
print("- Open http://localhost:8000/docs for interactive API documentation")
print("- Run 'python test_api.py' for comprehensive tests")
print("="*60)
