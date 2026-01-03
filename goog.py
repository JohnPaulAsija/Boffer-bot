import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def init_ai_client():
    # Retrieve the Gemini API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not found in .env file; set it in .env or the environment variables")
    print(f"Using GEMINI_API_KEY: {api_key}")
    
    # Global cache for File Search store
    _file_search_store_name = None

    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)

    # Get the absolute path of the current file
    current_file_path = os.path.realpath(__file__)

    # Get the directory containing the current file
    current_directory = os.path.dirname(current_file_path)

    # Load/validate the system instructions from system_instructions.txt
    _system_instruction_path = Path(current_directory) / "system_instructions.txt"
    if not _system_instruction_path.exists():
        raise FileNotFoundError(f"{_system_instruction_path} not found. Please create `system_instructions.txt` in the project root with the system instructions.")

    SYSTEM_INSTRUCTION = _system_instruction_path.read_text(encoding="utf-8")

    try:
       rules_file_refs = _ensure_uploaded_rules(current_directory=current_directory,client=client)
    except Exception as e:
        print(f"Failed to ensure uploaded rules: {e}")
        return f"Error preparing rules files: {e}"
    
    # Return the initialized client, system instructions, and uploaded file references
    return client, SYSTEM_INSTRUCTION, rules_file_refs

def _ensure_uploaded_rules(current_directory,client):
    # Upload rule files if not already uploaded, and return their references
    DagorhirRules = None
    HearthlightRules = None
    try:
        if DagorhirRules is None:
            uploaded = client.files.upload(file=os.path.join(current_directory, 'rules', 'DagorhirManualofArms.pdf'))
            DagorhirRules = uploaded
            # Some SDK versions expose the uploaded file's id as `id` or `file_id`, or may only provide a name.
            file_id = getattr(uploaded, 'id', None) or getattr(uploaded, 'file_id', None) or getattr(uploaded, 'name', None) or repr(uploaded)
            print(f"Uploaded DagorhirRules file: {file_id}")
        if HearthlightRules is None:
            uploaded = client.files.upload(file=os.path.join(current_directory, 'rules', 'HearthlightRulebook.pdf'))
            HearthlightRules = uploaded
            file_id = getattr(uploaded, 'id', None) or getattr(uploaded, 'file_id', None) or getattr(uploaded, 'name', None) or repr(uploaded)
            print(f"Uploaded HearthlightRules file: {file_id}")
    except Exception as e:
        # Surface upload errors so they are visible in logs and so callers can handle them.
        print(f"Error uploading rule files: {e}")
        raise
    return [DagorhirRules, HearthlightRules]



def generate_response(prompt, client, system_instructions, rules_file_refs):
    try:
        # Build a safe contents list: prompt plus any available uploaded file refs
        contents = [prompt]
        if rules_file_refs:
            contents.extend([r for r in rules_file_refs if r is not None]) # Add only non-None refs

        # Generate response from the model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instructions),
        )
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error generating response from model: {e}")
        return f"Error generating response: {e}"