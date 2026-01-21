from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

from backend.config import get_hf_key, validate_config
from backend.pipeline import PlannerPipeline
from backend.config import *

# Validate config on startup
validate_config()

# Initialize FastAPI app
app = FastAPI(
    title="Mosque Event Planner API",
    description="API for planning mosque community events with venue and catering recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(get_hf_key())
print(get_google_maps_key())

# Initialize pipeline
planner = PlannerPipeline()

# Request models
class EventPlanRequest(BaseModel):
    prompt: str
    result_count: Optional[int] = 15
    radius: Optional[int] = 20000
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Community iftar in NYC for 100 people on a budget of 10 thousand dollars, indian food preferred",
                "result_count": 15,
                "radius": 20000
            }
        }

# Response models
class EventPlanResponse(BaseModel):
    venues: dict
    catering: list
    status: str = "success"

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Mosque Event Planner API is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "serializer": "online",
            "maps": "online",
            "bigagent": "online"
        }
    }

@app.post("/api/plan-event", response_model=EventPlanResponse)
def plan_event(request: EventPlanRequest):
    """
    Plan an event with venue and catering recommendations
    
    - **prompt**: Natural language description of the event
    - **result_count**: Number of results to fetch from Google Maps (default: 15)
    - **radius**: Search radius in meters (default: 20000)
    """
    try:
        venue_res, catering_res = planner.plan(
            prompt=request.prompt,
            result_count=request.result_count or 15,
            radius=request.radius or 20000
        )
        
        return EventPlanResponse(
            venues=venue_res,
            catering=catering_res,
            status="success"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# For testing locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
