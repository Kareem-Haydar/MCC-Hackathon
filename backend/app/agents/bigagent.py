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

  def process(self, prompt: str) -> str:
      completion = self.client.chat.completions.create(
          model=self.model,
          temperature=0.0,
          messages=[
              {
                  "role": "system",
                  "content": prompt
              }
          ]
      )

      return completion.choices[0].message["content"]