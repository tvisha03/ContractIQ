import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Set this in your environment
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# You can change the model to any summarization-capable model available on OpenRouter
MODEL = "mistralai/mistral-7b-instruct"


def summarize_text(text: str, model: str = None) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable not set.")

    models_to_try = [model] if model else ["mistralai/mistral-7b-instruct", "meta-llama/llama-3-8b-instruct", "google/gemma-7b-it"]  # Add more as needed

    prompt = f"Summarize the following contract in plain English, focusing on key obligations, risks, and parties involved.\n\nContract:\n{text}"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    last_error = None
    for m in models_to_try:
        data = {
            "model": m,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"All summarization models failed. Last error: {last_error}")