import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Global cache for File Search store
_file_search_store_name = None

api_key_ = os.getenv("GEMINI_API_KEY")
if not api_key_:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file; set it in .env or the environment variables")
print(f"Using GEMINI_API_KEY: {api_key_}")

client = genai.Client(api_key=api_key_)

# Get the absolute path of the current file
current_file_path = os.path.realpath(__file__)
print(f"Absolute path of current file: {current_file_path}")

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Load/validate the system instructions at import time so startup errors are raised early
_system_instruction_path = Path(current_directory) / "system_instructions.txt"
if not _system_instruction_path.exists():
    raise FileNotFoundError(f"{_system_instruction_path} not found. Please create `system_instructions.txt` in the project root with the system instructions.")

SYSTEM_INSTRUCTION = _system_instruction_path.read_text(encoding="utf-8")

# Lazy-loaded uploaded files (avoid network calls at import time)
DagorhirRules = None
HearthlightRules = None

def _ensure_uploaded_rules():
    """Upload rules files to the client if they haven't been uploaded yet."""
    global DagorhirRules, HearthlightRules
    if DagorhirRules is None:
        DagorhirRules = client.files.upload(file=os.path.join(current_directory, 'rules', 'DagorhirManualofArms.pdf'))
    if HearthlightRules is None:
        HearthlightRules = client.files.upload(file=os.path.join(current_directory, 'rules', 'HearthlightRulebook.pdf'))

def generate_response(prompt):

    _ensure_uploaded_rules()

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=[prompt, DagorhirRules, HearthlightRules],
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION))
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"