# 🕌 Mosque Event Planner API

An intelligent event planning system designed for mosque community centers, powered by AI and Google Maps. Automatically finds and recommends suitable venues and halal catering options based on natural language event descriptions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [How Interactive Documentation Works](#how-interactive-documentation-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Code Documentation](#code-documentation)
- [Examples](#examples)

---

## 🎯 Overview

The Mosque Event Planner API streamlines the event planning process by:

1. **Understanding** natural language event descriptions
2. **Searching** Google Maps for relevant venues and caterers
3. **Analyzing** options using AI to provide context-aware recommendations
4. **Prioritizing** halal dietary requirements for mosque communities

### Key Capabilities

- ✅ Natural language processing for event requirements
- ✅ Google Maps integration for venue and catering search
- ✅ AI-powered recommendation engine
- ✅ Automatic halal catering filtering
- ✅ Interactive API documentation (Swagger/OpenAPI)
- ✅ Comprehensive error handling

---

## ✨ Features

### 🤖 AI-Powered Analysis
- Uses state-of-the-art language models for understanding and recommendations
- Context-aware evaluation of venues and caterers
- Detailed explanations for each recommendation

### 🗺️ Google Maps Integration
- Real-time venue and catering search
- Enriched data with ratings, photos, contact info
- Configurable search radius and result count

### 🍽️ Dietary Compliance
- Automatic halal catering search
- Support for multiple cuisines
- Dietary preference tracking and validation

### 📊 Structured Output
- Standardized JSON responses
- Top 3-5 recommendations with explanations
- Notes about capacity, dietary support, and requirements

---

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI App   │  ← REST API Layer
└────────┬────────┘
         │
┌────────▼────────────┐
│ PlannerPipeline     │  ← Main Orchestrator
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│Serial│  │BigAgent│  ← AI Agents
│izer  │  │        │
└───┬──┘  └──┬─────┘
    │        │
    └───┬────┘
        │
   ┌────▼────┐
   │   Map   │  ← Google Maps Client
   └─────────┘
```

### Components

#### 1. **FastAPI Application** (`app/main.py`)
- REST API endpoints
- Request/response validation with Pydantic
- Interactive documentation generation
- Error handling and status codes

#### 2. **PlannerPipeline** (`app/pipeline.py`)
- Orchestrates the entire workflow
- Coordinates between serializer, maps, and analysis agents
- Handles errors and logging

#### 3. **SerializerAgent** (`app/agents/serializer.py`)
- Converts natural language to structured JSON
- Extracts: location, event type, budget, headcount, cuisines, etc.
- Uses SmolLM3-3B (lightweight, fast)

#### 4. **BigAgent** (`app/agents/bigagent.py`)
- Analyzes venues and catering options
- Ranks based on suitability, capacity, rating, etc.
- Uses Qwen3-Next-80B (powerful reasoning)

#### 5. **Map** (`app/scraper/mapsearch.py`)
- Google Maps API client
- Venue and catering search
- Data enrichment (phone, website, hours)

---

## 📖 How Interactive Documentation Works

FastAPI automatically generates **two types** of interactive documentation:

### 1. Swagger UI (http://localhost:8000/docs)

**How it works:**
- FastAPI uses your route decorators, Pydantic models, and docstrings to generate an **OpenAPI specification**
- Swagger UI renders this spec as an interactive web interface
- You can test API calls directly in the browser

**Key Features:**
- **"Try it out"** button: Execute real API requests
- **Request body editor**: Fill in JSON data with autocomplete
- **Response viewer**: See actual API responses
- **Schema browser**: Explore data models
- **Authentication support**: Test with API keys/tokens

**What makes it automatic:**
```python
@app.post("/api/plan-event", response_model=EventPlanResponse)
def plan_event(request: EventPlanRequest):
    """
    Plan an event with venue and catering recommendations
    
    - **prompt**: Natural language description of the event
    - **result_count**: Number of results to fetch (default: 15)
    - **radius**: Search radius in meters (default: 20000)
    """
```

FastAPI reads:
- The route path: `/api/plan-event`
- HTTP method: `POST`
- Request model: `EventPlanRequest` (with Pydantic validation)
- Response model: `EventPlanResponse`
- Docstring: Appears as endpoint description
- Type hints: Used for validation and documentation

### 2. ReDoc (http://localhost:8000/redoc)

Alternative documentation style:
- More readable for browsing
- Better for documentation sharing
- Three-panel layout (navigation, content, code samples)
- Generated from the same OpenAPI spec

### Behind the Scenes

```python
# Pydantic models define the schema
class EventPlanRequest(BaseModel):
    prompt: str
    result_count: Optional[int] = 15
    radius: Optional[int] = 20000
    
    class Config:
        json_schema_extra = {  # ← Shows up as example in docs!
            "example": {
                "prompt": "Community iftar in NYC...",
                "result_count": 15,
                "radius": 20000
            }
        }
```

**This generates:**
- JSON Schema for validation
- Example requests in the documentation
- Input validation with error messages
- Type conversion (string to int, etc.)

### Accessing Documentation

1. Start the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. Open your browser:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **OpenAPI JSON**: http://localhost:8000/openapi.json

3. Test an endpoint:
   - Click on `/api/plan-event`
   - Click "Try it out"
   - Edit the JSON request body
   - Click "Execute"
   - View the response below

---

## 🚀 Installation

### Prerequisites

- Python 3.9+
- Google Maps API key
- HuggingFace API key

### Steps

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Create a `.env` file in the `backend` directory:

```env
# HuggingFace API Key (for AI models)
HF_INFERENCE_KEY=your_huggingface_api_key_here

# Google Maps API Key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### Getting API Keys

#### HuggingFace API Key
1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "Read" access
3. Copy the token

#### Google Maps API Key
1. Go to https://console.cloud.google.com/
2. Enable "Places API" and "Geocoding API"
3. Create credentials (API Key)
4. Copy the API key

---

## 💻 Usage

### Start the Server

#### Option 1: Direct Python
```bash
python -m app.main
```

#### Option 2: Uvicorn (recommended)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

### Quick Test

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test event planning
curl -X POST http://localhost:8000/api/plan-event \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Community iftar in NYC for 100 people, budget $10,000",
    "result_count": 10,
    "radius": 15000
  }'
```

---

## 📚 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Root Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "online",
  "message": "Mosque Event Planner API is running",
  "version": "1.0.0"
}
```

#### 2. Detailed Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "api": "online",
    "serializer": "online",
    "maps": "online",
    "bigagent": "online"
  }
}
```

#### 3. Plan Event
```http
POST /api/plan-event
```

**Request Body:**
```json
{
  "prompt": "string (required)",
  "result_count": "integer (optional, default: 15)",
  "radius": "integer (optional, default: 20000)"
}
```

**Response:**
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
    "general_notes": ["General note"]
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
      "general_notes": ["General note"]
    }
  ],
  "status": "success"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input or prompt parsing failed
- `500 Internal Server Error`: Server error during processing

---

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Quick Test
```bash
python quick_test.py
```

### Manual Testing with Swagger UI
1. Open http://localhost:8000/docs
2. Click on `/api/plan-event`
3. Click "Try it out"
4. Edit the request body
5. Click "Execute"

---

## 📝 Code Documentation

All classes and public methods include comprehensive docstrings following Google style guide.

### Core Classes

#### `PlannerPipeline`
Main orchestration pipeline for event planning. Coordinates serialization, search, and analysis.

**Methods:**
- `plan(prompt, result_count, radius)`: Execute complete planning workflow

#### `SerializerAgent`
Converts natural language to structured JSON using SmolLM3-3B.

**Methods:**
- `serialize_prompt(prompt)`: Extract structured data from text

#### `BigAgent`
Analyzes and ranks options using Qwen3-Next-80B.

**Methods:**
- `process_venue(prompt)`: Rank venue options
- `process_catering(prompt)`: Rank catering options

#### `Map`
Google Maps API client for location queries.

**Methods:**
- `query_venue(location, venue_type, result_count, radius)`: Search venues
- `query_catering(location, cuisine, result_count, radius)`: Search caterers

### View Documentation

```python
# In Python REPL
from app.pipeline import PlannerPipeline
help(PlannerPipeline)
help(PlannerPipeline.plan)
```

---

## 💡 Examples

### Example 1: Community Iftar
```json
{
  "prompt": "Community iftar in New York City for 100 people on a budget of 10 thousand dollars, indian food preferred",
  "result_count": 10,
  "radius": 15000
}
```

### Example 2: Wedding
```json
{
  "prompt": "Wedding in San Francisco for 200 people with a budget of 30000 dollars, need Pakistani and Arab food, halal required",
  "result_count": 15,
  "radius": 25000
}
```

### Example 3: Eid Celebration
```json
{
  "prompt": "Eid celebration in Los Angeles for 300 people, budget 15000 dollars, Turkish and Mediterranean cuisine, need outdoor space",
  "result_count": 20,
  "radius": 30000
}
```

### Example 4: Educational Seminar
```json
{
  "prompt": "Islamic studies seminar in Chicago for 50 people, budget 5000 dollars, need AV equipment and wheelchair accessibility",
  "result_count": 8,
  "radius": 10000
}
```

---

## 🛠️ Development

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration & validation
│   ├── pipeline.py          # Main orchestrator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── serializer.py    # NLP agent
│   │   └── bigagent.py      # Analysis agent
│   └── scraper/
│       ├── __init__.py
│       └── mapsearch.py     # Google Maps client
├── test_api.py              # Comprehensive tests
├── quick_test.py            # Quick test script
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── API_TESTING.md          # Testing guide
└── README.md               # This file
```

### Adding New Features

1. **New Endpoint**: Add to `app/main.py`
2. **New Agent**: Create in `app/agents/`
3. **New Data Source**: Create in `app/scraper/`
4. **Update Pipeline**: Modify `app/pipeline.py`

---

## 🤝 Contributing

When contributing:
1. Add docstrings to all new classes and methods
2. Update this README with new features
3. Add tests for new functionality
4. Run the test suite before submitting

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

- **FastAPI**: Modern web framework for building APIs
- **HuggingFace**: AI model hosting and inference
- **Google Maps**: Location data and search
- **Qwen Team**: Large language model
- **SmolLM Team**: Lightweight language model

---

## 📞 Support

For questions or issues:
- Check the interactive documentation: http://localhost:8000/docs
- Review the API testing guide: [API_TESTING.md](API_TESTING.md)
- Check docstrings: `help(ClassName)`

---

**Built with ❤️ for the Muslim community**
