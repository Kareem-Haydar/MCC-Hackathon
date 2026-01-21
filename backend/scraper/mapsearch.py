from googlemaps import Client
from backend.config import get_google_maps_key

class Map:
    """
    Google Maps API client for querying venues and catering options.
    
    Provides methods to search for event venues and catering services
    based on location, cuisine type, and other parameters. Enriches
    results with additional details like phone numbers and websites.
    
    Attributes:
        client (Client): Google Maps API client instance
    """
    
    def __init__(self):
        """
        Initialize the Map client with Google Maps API key.
        """
        self.client = Client(key=get_google_maps_key())

    def _map_place(self, place: dict) -> dict:
        """
        Transform Google Maps place data into standardized format.
        
        Enriches basic place data with additional details by making
        a follow-up API call for phone number, website, and hours.
        
        Args:
            place (dict): Raw place data from Google Maps API
        
        Returns:
            dict: Standardized place data with fields:
                  - name: Business name
                  - address: Full formatted address
                  - types: List of place types
                  - rating: Average rating (1-5)
                  - price_level: Price level (1-4)
                  - vicinity: Neighborhood/area
                  - phone_number: Formatted phone number
                  - website: Business website URL
                  - opening_hours: Weekly hours as list of strings
        """
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
        """
        Search for event venues near a location.
        
        Queries Google Maps for venues matching the event type within
        the specified radius of the location.
        
        Args:
            location (str): Location to search near (city name, address, etc.)
            venue_type (str): Type of venue to search for (e.g., "wedding", "conference")
            result_count (int, optional): Maximum number of results to return. Defaults to 15.
            radius (int, optional): Search radius in meters. Defaults to 20000.
        
        Returns:
            list: List of venue dictionaries with standardized place data
        
        Raises:
            ValueError: If result_count is not a positive integer
        
        Example:
            >>> maps = Map()
            >>> venues = maps.query_venue(
            ...     location="New York City",
            ...     venue_type="wedding venue",
            ...     result_count=10,
            ...     radius=15000
            ... )
        """
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
        """
        Search for halal catering options near a location.
        
        Queries Google Maps for halal catering services offering the specified
        cuisine type within the search radius. Automatically includes "halal"
        in the search query as this is designed for mosque events.
        
        Args:
            location (str): Location to search near (city name, address, etc.)
            cuisine (str): Type of cuisine (e.g., "Indian", "Pakistani", "Italian")
            result_count (int, optional): Maximum number of results to return. Defaults to 15.
            radius (int, optional): Search radius in meters. Defaults to 20000.
        
        Returns:
            list: List of caterer dictionaries with standardized place data
        
        Raises:
            ValueError: If result_count is not a positive integer
        
        Example:
            >>> maps = Map()
            >>> caterers = maps.query_catering(
            ...     location="San Francisco",
            ...     cuisine="Pakistani",
            ...     result_count=10
            ... )
        """
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
