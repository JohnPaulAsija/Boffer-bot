import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# Retrieve the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY is None:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

if __name__ == "__main__":
    # Get the port from environment variable (default 8000)
    port = int(os.getenv("PORT", 8000))

    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
