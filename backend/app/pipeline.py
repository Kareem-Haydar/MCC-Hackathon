from app.agents import SerializerAgent, BigAgent
from app.scraper import Map

import json

class PlannerPipeline:
    def __init__(self):
        self.map = Map()
        self.serializer = SerializerAgent()
        self.bigagent = BigAgent()

    def plan(self, prompt, result_count=15, radius=20000):
        json_data = self.serializer.serialize_prompt(prompt)
        venues = self.map.query_venue(location=json_data["location"], venue_type=json_data["event_type"], result_count=result_count, radius=radius)
        catering = self.map.query_catering(json_data["location"], json_data["event_type"], result_count=result_count, radius=radius)

        big_agent_venues_response = self.bigagent.process_venue(json.dumps(venues))
        big_agent_catering_response = self.bigagent.process_catering(json.dumps(catering))

        return big_agent_venues_response, big_agent_catering_response
