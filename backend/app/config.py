import os

HF_INFERENCE_KEY = os.environ.get("HF_INFERENCE_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

def validate_config():
    if not HF_INFERENCE_KEY:
        raise ValueError("HF_INFERENCE_KEY is not set in environment variables.")
    if not GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY is not set in environment variables.")