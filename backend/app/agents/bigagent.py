from huggingface_hub import InferenceClient
from app.config import HF_INFERENCE_KEY
import json
import re

class BigAgent:
    def __init__(self):
      self.client = InferenceClient(
          api_key=HF_INFERENCE_KEY
      )

      self.model = "Qwen/Qwen3-Next-80B-A3B-Instruct"

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

    def process_venue(self, prompt: str) -> dict:
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
