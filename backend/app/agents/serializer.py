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
                        "content": f"""
                            Serialize this prompt into JSON. Extract the following fields:
                            - location (string)
                            - event_type (string)
                            - budget (string)
                            - min_head_count (string)
                            - max_head_count (string)
                            - cuisines (array of strings)
                            - dietary_preferences (array of strings)
                            - other_requirements (array of strings)

                            Instructions for location:
                            - don't use abbreviations (e.g., 'NYC' instead of 'New York City')

                            Instructions for budget:
                            - just put the number, no commas or other symbols

                            Instructions for cuisines:
                            - only include cuisines that are explicitly mentioned in the prompt, if none is mentioned, default to "American"

                            Instructions for head_count:
                            - If the text mentions 'X attendees' or 'around X people', use X for both min_head_count and max_head_count.
                            - If the text mentions a single number of attendees, use that number for both min_head_count and max_head_count.
                            - If a range is given (e.g., 100-150 attendees), use the lower number as min_head_count and the higher as max_head_count.

                            Instructions for event_type:
                            - Choose the event type from the following list only:
                              Conference, Seminar, Workshop, Lecture, Talk, Guest Speaker, Community Meeting, Town Hall, Celebration, Festival, Party, Wedding, Engagement, Religious Ceremony, Prayer Event, Ramadan Iftar, Eid Gathering, Charity, Fundraiser
                            - If the type is not explicitly mentioned, set event_type to 'unknown'

                            Instructions for other_requirements:
                            - Only include items in other_requirements if the user explicitly mentions them.
                            - Allowed requirements are: AV equipment, projector, microphone, sound system, accessible facilities, wheelchair access, indoor, outdoor, stage, podium, performance area, food, catering, dietary restrictions, parking, transport accessibility, decorations, setup requirements
                            - Do not infer anything from the prompt text; only include explicitly mentioned requirements

                            If information is missing, set the field to 'unknown'.

                            User text:
                            {prompt}"""
                    }
                ],
            )

            return self._parse_response(completion.choices[0].message.content)

        except Exception as e:
            raise ValueError(f"Failed to serialize prompt: {e}")
