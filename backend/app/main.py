from dotenv import load_dotenv
import json

load_dotenv()

from app.config import GOOGLE_MAPS_API_KEY

from app.agents import SerializerAgent
from app.scraper import GMapsInstance

def __main__():
    gmaps = GMapsInstance()
    results = gmaps.query_place(
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
