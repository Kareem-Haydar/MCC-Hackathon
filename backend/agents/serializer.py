from huggingface_hub import InferenceClient
from backend.config import get_hf_key
import json
import re

class SerializerAgent:
    """
    AI agent for converting natural language event descriptions into structured JSON.
    
    Uses a lightweight language model (SmolLM3-3B) to extract structured information
    from natural language prompts, including location, event type, budget, headcount,
    cuisines, dietary preferences, and other requirements.
    
    Attributes:
        client (InferenceClient): HuggingFace inference client
        model (str): Name of the LLM model used for serialization
    """
    
    def __init__(self):
        """
        Initialize the SerializerAgent with HuggingFace client and model.
        """
        self.client = InferenceClient(
            api_key=get_hf_key()
        )

        self.model = "HuggingFaceTB/SmolLM3-3B"

    def _parse_response(self, response) -> dict:
        """
        Parse JSON from LLM response, handling various formats.
        
        Attempts to extract JSON from markdown code blocks or raw text,
        while removing thinking tags and other noise from the response.
        
        Args:
            response (str): Raw response text from the LLM
        
        Returns:
            dict: Parsed JSON data
        
        Raises:
            ValueError: If JSON cannot be found or parsed
        """
        try:
            if response is None:
                raise ValueError("No response from LLM")

            # Remove thinking tags
            cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
            
            # Try to find JSON in markdown code blocks first
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
            
            if match:
                json_str = match.group(1)
            else:
                # Try to find raw JSON object
                match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    # Print response for debugging
                    print(f"\n=== LLM Response (first 500 chars) ===")
                    print(response[:500])
                    print(f"\n=== End Response ===")
                    raise ValueError("No JSON found in LLM response")

            return json.loads(json_str)

        except json.JSONDecodeError as e:
            print(f"\n=== JSON Parse Error ===")
            print(f"Error: {e}")
            print(f"Attempted to parse: {json_str[:200] if 'json_str' in locals() else 'N/A'}") #type: ignore
            print(f"=== End Error ===")
            raise ValueError(f"Failed to parse JSON: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")

    def serialize_prompt(self, prompt: str) -> dict:
        """
        Convert natural language event description to structured JSON.
        
        Extracts key information from a natural language prompt including:
        - location: Event location (city/venue)
        - event_type: Type of event (Iftar, Wedding, Conference, etc.)
        - budget: Budget amount as a number
        - min_head_count/max_head_count: Expected number of attendees
        - cuisines: List of preferred food types
        - dietary_preferences: List of dietary restrictions
        - other_requirements: List of additional requirements (AV, parking, etc.)
        
        Args:
            prompt (str): Natural language description of the event.
                         Example: "Community iftar in NYC for 100 people, budget $10,000"
        
        Returns:
            dict: Structured event data with all extracted fields
        
        Raises:
            ValueError: If LLM request fails or response cannot be parsed
        
        Example:
            >>> agent = SerializerAgent()
            >>> data = agent.serialize_prompt(
            ...     "Wedding in San Francisco for 200 people, budget $30,000"
            ... )
            >>> print(data['location'])
            'San Francisco'
        """
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
                              Conference, Seminar, Workshop, Lecture, Talk, Guest Speaker, Community Meeting, Town Hall, Celebration, Festival, Party, Wedding, Engagement, Religious Ceremony, Prayer Event, Iftar, Eid Gathering, Charity, Fundraiser
                            - Use context clues to infer the event type if it's not explicitly mentioned.
                            - If words like iftar or ramadan are mentioned, classify as Iftar.

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
