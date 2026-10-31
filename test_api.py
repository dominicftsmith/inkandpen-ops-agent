import os
import sys
import warnings
from dotenv import load_dotenv

# Suppress AFC advice warnings
warnings.filterwarnings("ignore")

# Load environment credentials
load_dotenv(os.path.join("submission", ".env"))
load_dotenv()

from google import genai
from google.genai import errors

print(f"[*] Python executable: {sys.executable}")
print("[*] Connecting to Gemini API...")

client = genai.Client()

# Test models: prioritize gemini-3.8-flash, with gemini-2.0-flash as a fallback check
models_to_test = ["gemini-3.8-flash", "gemini-2.0-flash"]

for model_id in models_to_test:
    print(f"\n[>] Sending test ping to '{model_id}'...")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Say 'API connection verified!' in 5 words or less."
        )
        print(f"[+] SUCCESS from {model_id}: {(response.text or '').strip()}")
        break
    except errors.ServerError as e:
        print(f"[-] 503 Server Congestion on {model_id}: {e.message}")
    except errors.APIError as e:
        print(f"[-] API Error on {model_id} (Code {e.code}): {e.message}")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")