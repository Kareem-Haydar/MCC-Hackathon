from huggingface_hub import InferenceClient
from app.config import HF_INFERENCE_KEY
import json
import re

class SerializerAgent:
    def __init__(self):
        self.client = InferenceClient(
            api_key=HF_INFERENCE_KEY
        )

        self.model = "HuggingFaceTB/SmolLM3-3B"

    def _parse_response(self, response) -> dict:
        try:
            if response is None:
                raise ValueError("No response from LLM")

            cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
            match = re.search(r"```json\s*(\{.*?\})\s*```", cleaned, re.DOTALL)

            if not match:
                raise ValueError("No JSON block found in LLM response")

            json_str = match.group(1)

            return json.loads(json_str)

        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")

    def serialize_prompt(self, prompt: str) -> dict:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content":
                            "Serialize this prompt into JSON. Extract the following fields:\n"
                            "- location (string)\n"
                            "- event_type (string)\n"
                            "- budget (string)\n"
                            "- min_head_count (string)\n"
                            "- max_head_count (string)\n"
                            "- dietary_preferences (array of strings)\n"
                            "- other_requirements (array of strings)\n\n"
                            "Instructions for location:\n"
                            "- don't use abbreviations (e.g., 'NYC' instead of 'New York City')\n"
                            "Instructions for budget:\n"
                            "- just put the number, no commas or other symbols\n"
                            "Instructions for head_count:\n"
                            "- If the text mentions 'X attendees' or 'around X people', use X for both min_head_count and max_head_count.\n"
                            "- If the text mentions a single number of attendees, use that number for both min_head_count and max_head_count.\n"
                            "- If a range is given (e.g., 100-150 attendees), use the lower number as min_head_count and the higher as max_head_count.\n"
                            "Instructions for event_type:\n"
                            "- Choose the event type from the following list only:\n"
                            "  Conference, Seminar, Workshop, Lecture, Talk, Guest Speaker, Community Meeting, Town Hall, Celebration, Festival, Party, Wedding, Engagement, Religious Ceremony, Prayer Event, Ramadan Iftar, Eid Gathering, Charity, Fundraiser\n"
                            "- If the type is not explicitly mentioned, set event_type to 'unknown'\n"
                            "Instructions for other_requirements:\n"
                            "- Only include items in other_requirements if the user explicitly mentions them.\n"
                            "- Allowed requirements are: AV equipment, projector, microphone, sound system, accessible facilities, wheelchair access, indoor, outdoor, stage, podium, performance area, food, catering, dietary restrictions, parking, transport accessibility, decorations, setup requirements\n"
                            "- Do not infer anything from the prompt text; only include explicitly mentioned requirements\n"
                            "If information is missing, set the field to 'unknown'.\n\n"
                            "User text:\n" + prompt
                    }
                ],
            )

            return self._parse_response(completion.choices[0].message.content)

        except Exception as e:
            raise ValueError(f"Failed to serialize prompt: {e}")
