from googlemaps import Client
from app.config import GOOGLE_MAPS_API_KEY

class Map:
    def __init__(self):
        self.client = Client(key=GOOGLE_MAPS_API_KEY)

    def _map_place(self, place: dict) -> dict:
        place_id = place.get("place_id")

        details = {}
        if place_id:
            try:
                details_resp = self.client.place( # type: ignore
                    place_id=place_id,
                    fields=[
                        "formatted_phone_number",
                        "website",
                        "opening_hours"
                    ]
                )
                details = details_resp.get("result", {})
            except Exception:
                details = {}

        return {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "types": place.get("types", []),
            "rating": place.get("rating"),
            "price_level": place.get("price_level"),
            "vicinity": place.get("vicinity"),
            "phone_number": details.get("formatted_phone_number"),
            "website": details.get("website"),
            "opening_hours": details.get("opening_hours", {}).get("weekday_text")
        }

    def query_venue(self, location, venue_type, result_count=15, radius=20000):
        try:
            if result_count <= 0:
                raise ValueError("result_count must be a positive integer")

            geocode = self.client.geocode(location)[0] # type: ignore
            latlng = geocode["geometry"]["location"]

            response = self.client.places( # type: ignore
                query=venue_type,
                location=(latlng["lat"], latlng["lng"]),
                radius=radius
            )

            results = response.get("results", [])[:result_count]
            mapped_results = [self._map_place(place) for place in results]

            return mapped_results
        
        except Exception as e:
            print(f"Error querying Google Maps: {e}")
            return []

    def query_catering(self, location, cuisine, result_count=15, radius=20000):
        try:
            if result_count <= 0:
                raise ValueError("result_count must be a positive integer")

            geocode = self.client.geocode(location)[0] # type: ignore
            latlng = geocode["geometry"]["location"]

            response = self.client.places( # type: ignore
                query= "halal " + cuisine + " catering",
                location=(latlng["lat"], latlng["lng"]),
                radius=radius
            )

            results = response.get("results", [])[:result_count]
            mapped_results = [self._map_place(place) for place in results]

            return mapped_results
        
        except Exception as e:
            print(f"Error querying Google Maps: {e}")
            return []
