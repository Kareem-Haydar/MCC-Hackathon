from googlemaps import Client
from app.config import GOOGLE_MAPS_API_KEY

class GMapsInstance:
    def __init__(self, api_key: str):
        self.client = Client(key=api_key)

    def query_place(self, location, venue_type):
        query_text = f"{venue_type} in {location}"
        results = self.client.places(query=query_text) # type: ignore

        
