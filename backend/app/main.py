from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv()

from app.config import GOOGLE_MAPS_API_KEY

from app.agents import SerializerAgent
from app.scraper import Map

def __main__():
    gmaps = Map()
    results = gmaps.query_venue(
        location="New York City",
        venue_type="coffee shop",
        result_count=5
    )

    first = results[0]

    print("✅ First result:")
    print(f"Name: {first.get('name')}")
    print(f"Address: {first.get('formatted_address')}")
    print(f"Rating: {first.get('rating')}")
    print(f"Total Reviews: {first.get('user_ratings_total')}")
    print(f"Place ID: {first.get('place_id')}")

if __name__ == "__main__":
    __main__()
