from dotenv import load_dotenv
import json

load_dotenv()

from app.agents import SerializerAgent

def __main__():
    serializer_agent = SerializerAgent()
    ret = serializer_agent.serialize_prompt("I want to go to New York City for a conference with 100-200 attendees, and some of them are alergic to peanuts. My budget is 15 thousand. I need an indoor area with good acoustics and a stage")

    print(json.dumps(ret))

if __name__ == "__main__":
    __main__()
