from huggingface_hub import InferenceClient
from backend.config import get_hf_key
import json
import re

class BigAgent:
    """
    AI agent for evaluating and ranking venue and catering options.
    
    Uses a large language model (Qwen3-Next-80B) to analyze venue and catering
    options against event requirements, providing context-aware recommendations
    with detailed explanations and notes.
    
    Attributes:
        client (InferenceClient): HuggingFace inference client
        model (str): Name of the LLM model used for analysis
    """
    
    def __init__(self):
        """
        Initialize the BigAgent with HuggingFace client and model.
        """
        self.client = InferenceClient(
            api_key=get_hf_key()
        )

        self.model = "Qwen/Qwen3-Next-80B-A3B-Instruct"

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
            print(f"Attempted to parse: {json_str[:200] if 'json_str' in locals() else 'N/A'}") # type: ignore
            print(f"=== End Error ===")
            raise ValueError(f"Failed to parse JSON: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")

    def process_venue(self, prompt: str) -> dict:
        """
        Analyze and rank venue options for an event.
        
        Evaluates venue candidates against event requirements including
        capacity, event type suitability, rating, location, and other factors.
        Returns top 3-5 recommendations with detailed explanations.
        
        Args:
            prompt (str): JSON string containing event requirements and venue data.
                         Expected format: {"data": {...event_requirements...}, "venues": [...]}
        
        Returns:
            dict: Structured recommendations with format:
                  {
                    "recommended_venues": [
                      {
                        "name": str,
                        "address": str,
                        "rating": float,
                        "price_level": int,
                        "why_recommended": str,
                        "notes": [str]
                      }
                    ],
                    "general_notes": [str]
                  }
        
        Raises:
            ValueError: If LLM request fails or response cannot be parsed
        """
        try :
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": """
                            You are an AI event planning assistant for a local mosque or community center.

                            Your task is to evaluate and rank possible EVENT VENUES based on the event requirements and the venue data provided.

                            You will be given:
                            1. Event requirements (location, event type, headcount, budget, dietary preferences, other requirements)
                            2. A list of venue candidates sourced from Google Maps, each with structured fields

                            Your responsibilities:
                            - Compare venues against each other
                            - Rank the venues from most suitable to least suitable
                            - Select the TOP 3–5 venues only
                            - Do NOT invent facts that are not present in the input
                            - If information is missing or unclear, explicitly note that it needs confirmation

                            Evaluation criteria (use all that apply):
                            - Suitability for the event type
                            - Likely capacity based on venue type and context
                            - Rating and number of reviews
                            - Location relevance
                            - Price level if available
                            - Explicitly mentioned user requirements only

                            Important rules:
                            - Do NOT assume availability of AV equipment, stage, or accessibility unless stated
                            - If a venue is a community hall, mosque hall, or conference center, you may say "likely suitable" but must add a confirmation note
                            - Do NOT infer dietary details for venues unless explicitly mentioned
                            - If headcount suitability is unclear, flag it

                            Return ONLY valid JSON in the following format, with no additional text:

                            {
                              "recommended_venues": [
                                {
                                  "name": "string",
                                  "address": "string",
                                  "rating": number | null,
                                  "price_level": number | null,
                                  "why_recommended": "string",
                                  "notes": ["string"]
                                }
                              ],
                              "general_notes": ["string"]
                            }

                            Be concise, realistic, and conservative in your recommendations.

                            Data:

                            """ + prompt
                    }
                ]
            )

            return self._parse_response(completion.choices[0].message.content)

        except Exception as e:
            raise ValueError(f"Failed to process prompt: {e}")

    def process_catering(self, prompt: str) -> dict:
        """
        Analyze and rank catering options for an event.
        
        Evaluates catering candidates against event requirements including
        dietary restrictions (halal, vegetarian, etc.), cuisine type, rating,
        capacity, and pricing. Returns top 3-5 recommendations with detailed
        explanations and dietary support information.
        
        Args:
            prompt (str): JSON string containing event requirements and catering data.
                         Expected format: {\"data\": {...event_requirements...}, \"catering\": [...]}
        
        Returns:
            dict: Structured recommendations with format:
                  {
                    "recommended_catering": [
                      {
                        "name": str,
                        "address": str,
                        "rating": float,
                        "price_level": int,
                        "why_recommended": str,
                        "dietary_support": [str],
                        "notes": [str]
                      }
                    ],
                    "general_notes": [str]
                  }
        
        Raises:
            ValueError: If LLM request fails or response cannot be parsed
        """
        try :
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": """
                            You are an AI event planning assistant for a local mosque or community center.

                            Your task is to evaluate and rank possible CATERING OPTIONS based on the event requirements and the catering data provided.

                            You will be given:

                            1. Event requirements (location, event type, headcount, budget, dietary preferences, other requirements)
                            2. A list of catering candidates sourced from Google Maps, each with structured fields

                            Your responsibilities:

                            * Compare catering options against each other
                            * Rank the catering options from most suitable to least suitable
                            * Select the TOP 3–5 catering options only
                            * Do NOT invent menu items or services
                            * Treat dietary preferences as STRICT requirements

                            Dietary rules:

                            * If "halal" is listed, the caterer must explicitly appear halal-friendly or be flagged for confirmation
                            * If multiple dietary preferences exist (e.g., halal + dairy-free), always note that confirmation is required
                            * Never assume allergy handling or cross-contamination safety

                            Evaluation criteria:

                            * Alignment with dietary preferences
                            * Rating and number of reviews
                            * Catering-specific keywords or context
                            * Location relevance
                            * Price level if available

                            Important rules:

                            * Do NOT claim a caterer supports a dietary restriction unless explicitly stated or strongly implied by name/category
                            * Always include a confirmation note for dietary restrictions
                            * If headcount suitability or pricing is unclear, note it

                            Return ONLY valid JSON in the following format, with no additional text:

                            {
                                "recommended_catering": [
                                    {
                                    "name": "string",
                                    "address": "string",
                                    "rating": number | null,
                                    "price_level": number | null,
                                    "why_recommended": "string",
                                    "dietary_support": ["string"],
                                    "notes": ["string"]
                                    }
                                ],
                                "general_notes": ["string"]
                            }

                            Be cautious, transparent, and realistic.

                            Data:

                            """ + prompt
                    }
                ]
            )

            return self._parse_response(completion.choices[0].message.content)

        except Exception as e:
            raise ValueError(f"Failed to process prompt: {e}")
