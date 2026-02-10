import os
import sys

# Ensure the current directory is in sys.path
sys.path.append(os.getcwd())

from app.services.llm_service import generate_explanation

# Check for API key
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY is not set in the environment.")
    print("Attempting to load from .env...")
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: Please set GEMINI_API_KEY in your .env file or environment variables.")
        sys.exit(1)

print("Testing Gemini integration...")
garbage_class = "plastic bottle"
print(f"Input Class: {garbage_class}")

try:
    result = generate_explanation(garbage_class)
    print("\n--- Result ---")
    print(result)
    
    if "description" in result and "tips" in result:
        print("\nSUCCESS: Received valid JSON response.")
    else:
        print("\nFAILURE: Response structure is incorrect.")

except Exception as e:
    print(f"\nERROR: Failed to generate explanation. {e}")
