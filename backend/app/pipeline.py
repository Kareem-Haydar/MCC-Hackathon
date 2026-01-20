from app.agents import SerializerAgent, BigAgent
from app.scraper import Map

import json

class PlannerPipeline:
    """
    Main orchestration pipeline for event planning.
    
    This class coordinates the entire event planning workflow by:
    1. Serializing natural language prompts into structured data
    2. Querying Google Maps for venues and catering options
    3. Using AI agents to analyze and recommend the best options
    
    Attributes:
        map (Map): Google Maps API client for location queries
        serializer (SerializerAgent): LLM agent for parsing natural language
        bigagent (BigAgent): LLM agent for evaluating and ranking options
    """
    
    def __init__(self):
        """
        Initialize the pipeline with all required components.
        """
        self.map = Map()
        self.serializer = SerializerAgent()
        self.bigagent = BigAgent()

    def plan(self, prompt, result_count=15, radius=20000):
        """
        Execute the complete event planning pipeline.
        
        Args:
            prompt (str): Natural language description of the event requirements.
                         Should include location, event type, headcount, budget, and preferences.
            result_count (int, optional): Number of results to fetch from Google Maps.
                                         Defaults to 15.
            radius (int, optional): Search radius in meters from the location.
                                   Defaults to 20000 (20km).
        
        Returns:
            tuple: A tuple containing:
                - venues (dict): Recommended venues with analysis
                - catering (list): Recommended catering options with analysis
        
        Raises:
            ValueError: If prompt serialization fails or required fields are missing
        
        Example:
            >>> pipeline = PlannerPipeline()
            >>> venues, catering = pipeline.plan(
            ...     "Community iftar in NYC for 100 people, budget $10,000",
            ...     result_count=10,
            ...     radius=15000
            ... )
        """
        try:
            json_data = self.serializer.serialize_prompt(prompt)

            if not json_data:
                raise ValueError("Failed to serialize prompt")
            
            print("\n================== Serialized Prompt Data ==================")
            print(json.dumps(json_data, indent=2))
            print("============================================================\n")
            
            cuisines = json_data.get("cuisines", [])
            catering = [self.map.query_catering(location=json_data["location"], cuisine=cuisine, result_count=result_count, radius=radius) for cuisine in cuisines]

            venues = self.map.query_venue(location=json_data["location"], venue_type=json_data["event_type"], result_count=result_count, radius=radius)

            print("================== Queried Venue Data ==================")
            print(json.dumps(venues, indent=2))
            print("============================================================\n")

            print("================== Queried Catering Data ==================")
            print(json.dumps(catering, indent=2))
            print("============================================================\n")
            big_agent_data = {
                "event_type": json_data["event_type"],
                "budget": json_data["budget"],
                "min_head_count": json_data["min_head_count"],
                "max_head_count": json_data["max_head_count"],
                "other_requirements": json_data["other_requirements"],
                "dietary_preferences": json_data["dietary_preferences"]
            }

            big_agent_venue_data = {
                "venues": venues,
                "data": big_agent_data
            }

            big_agent_venues_response = self.bigagent.process_venue(json.dumps(big_agent_venue_data))
            big_agent_catering_response = [self.bigagent.process_catering(json.dumps({"catering": catering_option, "data": big_agent_data})) for catering_option in catering]

            return big_agent_venues_response, big_agent_catering_response
        except Exception as e:
            raise ValueError(f"Pipeline planning failed: {e}")
