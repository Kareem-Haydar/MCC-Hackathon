from googlemaps import Client
from app.config import GOOGLE_MAPS_API_KEY

class GMapsInstance:
    def __init__(self):
        self.client = Client(key=GOOGLE_MAPS_API_KEY)

    def query_place(self, location, venue_type, result_count):
        try:
            if result_count <= 0:
                raise ValueError("result_count must be a positive integer")

            geocode = self.client.geocode(location)[0] # type: ignore
            latlng = geocode["geometry"]["location"]

            response = self.client.places( # type: ignore
                query=venue_type,
                location=(latlng["lat"], latlng["lng"]),
                radius=20000
            )

            results = response.get("results", [])[:result_count]
            return results
        
        except Exception as e:
            print(f"Error querying Google Maps: {e}")
            return []