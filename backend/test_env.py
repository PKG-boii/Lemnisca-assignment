# backend/test_env.py

import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment")

url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())