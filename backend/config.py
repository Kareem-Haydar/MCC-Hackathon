import os

def get_hf_key():
    return os.getenv("HF_INFERENCE_KEY")

def get_google_maps_key():
    return os.getenv("GOOGLE_MAPS_API_KEY")

def validate_config():
    hf_key = os.getenv("HF_INFERENCE_KEY")
    maps_key = os.getenv("GOOGLE_MAPS_API_KEY")

    missing = []
    if not hf_key:
        missing.append("HF_INFERENCE_KEY")
    if not maps_key:
        missing.append("GOOGLE_MAPS_API_KEY")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
