# API Testing Guide

## Starting the API Server

### Option 1: Run directly
```bash
python -m app.main
```

### Option 2: Run with uvicorn (more control)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## Available Endpoints

### 1. Health Check
```bash
GET http://localhost:8000/
GET http://localhost:8000/health
```

### 2. Plan Event
```bash
POST http://localhost:8000/api/plan-event
```

**Request Body:**
```json
{
  "prompt": "Community iftar in NYC for 100 people on a budget of 10 thousand dollars, indian food preferred",
  "result_count": 15,
  "radius": 20000
}
```

## Testing the API

### Method 1: Using the Test Script
```bash
# In terminal 1: Start the server
python -m app.main

# In terminal 2: Run the test script
python test_api.py
```

### Method 2: Using curl
```bash
# Health check
curl http://localhost:8000/health

# Plan an event
curl -X POST http://localhost:8000/api/plan-event \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Community iftar in New York City for 100 people on a budget of 10000 dollars, indian food preferred",
    "result_count": 10,
    "radius": 15000
  }'
```

### Method 3: Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/api/plan-event",
    json={
        "prompt": "Wedding in San Francisco for 200 people with a budget of 30000 dollars",
        "result_count": 10,
        "radius": 20000
    }
)

print(response.json())
```

### Method 4: Using the Swagger UI
1. Start the server: `python -m app.main`
2. Open browser: http://localhost:8000/docs
3. Click on the `/api/plan-event` endpoint
4. Click "Try it out"
5. Enter your request data
6. Click "Execute"

## Example Prompts

### Iftar Event
```
Community iftar in New York City for 100 people on a budget of 10 thousand dollars, indian food preferred
```

### Wedding
```
Wedding in San Francisco for 200 people with a budget of 30000 dollars, need Pakistani and Arab food, halal required
```

### Community Gathering
```
Community gathering in Chicago for 50 people, budget 5000 dollars, need Middle Eastern catering, wheelchair accessible venue required
```

### Eid Celebration
```
Eid celebration in Los Angeles for 300 people, budget 15000 dollars, Turkish and Mediterranean cuisine, need outdoor space
```

## Response Format

```json
{
  "venues": {
    "recommended_venues": [
      {
        "name": "Venue Name",
        "address": "Full Address",
        "rating": 4.5,
        "price_level": 2,
        "why_recommended": "Explanation...",
        "notes": ["Note 1", "Note 2"]
      }
    ],
    "general_notes": ["General note 1", "General note 2"]
  },
  "catering": [
    {
      "recommended_catering": [
        {
          "name": "Caterer Name",
          "address": "Full Address",
          "rating": 4.7,
          "price_level": 2,
          "why_recommended": "Explanation...",
          "dietary_support": ["halal", "vegetarian"],
          "notes": ["Note 1"]
        }
      ],
      "general_notes": ["General note 1"]
    }
  ],
  "status": "success"
}
```

## Troubleshooting

### Server won't start
- Check that `.env` file exists with required API keys
- Run `python -c "from app.config import validate_config; validate_config()"`

### Connection refused
- Make sure the server is running in another terminal
- Check that port 8000 is not in use: `lsof -i :8000`

### Slow responses
- First request is always slower (model loading)
- Subsequent requests should be faster
- Reduce `result_count` for faster responses

## Advanced Usage

### Custom Port
```bash
uvicorn app.main:app --port 5000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Auto-reload (Development)
```bash
uvicorn app.main:app --reload
```
