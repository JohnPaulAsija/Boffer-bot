import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Global cache for File Search store
_file_search_store_name = None

api_key_=os.getenv("GEMINI_API_KEY")
if api_key_ is None:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)
print(f"Using GEMINI_API_KEY: {api_key_}")

client = genai.Client(api_key=api_key_)
# Get the absolute path of the current file
current_file_path = os.path.realpath(__file__)
print(f"Absolute path of current file: {current_file_path}")

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)



DagorhirRules = client.files.upload(file=current_directory+'/rules/DagorhirManualofArms.pdf'),
HearthlightRules = client.files.upload(file=current_directory+'/rules/HearthlightRulebook.pdf'),


def generate_response(prompt):

    system_instruction = (
        "You are a helpful Discord bot assistant. Provide concise and clear responses. "
        "Your purpose is to answer questions strictly related to Dagorhir and Hearthlight rules and guidelines. "
        "Do not answer unrelated questions. If you do not know the answer, respond with 'I don't know.' "
        "When answering, cite relevant information from the available rules documents. when referencing a rules document include the section and sub section." \
        "perfer short answers with an option for more detail if needed."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=[prompt,DagorhirRules,HearthlightRules],
            config=types.GenerateContentConfig(system_instruction=system_instruction))
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"