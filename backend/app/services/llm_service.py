import os
import json
import traceback
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=api_key)

def generate_explanation(garbage_class):
    try:
        # Use the flash model for speed and efficiency
        model = genai.GenerativeModel(
            'gemini-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
        You are an expert on waste management and recycling.
        Provide a SHORT, CHILD-FRIENDLY explanation for the garbage type: {garbage_class}.
        
        The explanation should be simple, like:
        "This looks like plastic. Plastic can harm animals if thrown outside. It should be placed in the plastic recycling bin."
        
        DO NOT classify the object. The classification is already done (it is {garbage_class}).
        Your job is ONLY to explain it and give recycling tips.
        
        Return ONLY valid JSON in this format:
        {{
            "description": "Simple child-friendly explanation string",
            "tips": ["Simple tip 1", "Simple tip 2", "Simple tip 3"]
        }}
        """

        response = model.generate_content(prompt)
        
        # Parse the JSON response
        return json.loads(response.text)

    except Exception as e:
        traceback.print_exc()
        return {
            "description": "I couldn't generate an explanation right now.",
            "tips": [],
            "error_details": str(e)
        }
