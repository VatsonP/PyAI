import os
import google.generativeai as genai
import markdown
from datetime import datetime
from dotenv import load_dotenv


# Import functions from the separate file
from chat_util_functions import get_prompt_from_md, log_interaction, show_response

# Load environment variables from the .env file (if present)
load_dotenv()

# Retrieve the API key from the .env file
api_key_txt = os.getenv("GEMINI_API_KEY")

# Check for empty API key
if not api_key_txt:
    raise ValueError("Please set the GEMINI_API_KEY in the .env file")

# Configure and set API key
try:
    genai.configure(api_key=api_key_txt)

    generation_config = {
        "temperature": 0.75,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
except Exception as e:
    print(f"Error configuring and setting API key: {e}")  # Error message
    exit(1)

# Create model and client initialization
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
except Exception as e:
    print(f"Error initializing model: {e}")  # Error message
    exit(1)

# Start chat session
try:
    chat_session = model.start_chat(
        history=[
        ]
    )
except Exception as e:
    print(f"Error starting chat session: {e}")  # Error message
    exit(1)


# Set input prompt and get model response
try:
    prompt_text = get_prompt_from_md()
    start_time = datetime.now()
    response = chat_session.send_message(prompt_text)
    end_time = datetime.now()
    duration = end_time - start_time
    response_text = response.text
    log_interaction(prompt_text, start_time, end_time, duration, response_text)
except AttributeError:
    print("Error getting response text")
    exit(1)

# Converting response text to Markdown
try:
    response_html = markdown.markdown(response_text)
except Exception as e:
    print(f"Error converting response text to Markdown: {e}")
    exit(1)

# Show response in GUI window
try:
    show_response("Gemini AI Response", response_html, response_text)
except Exception as e:
    print(f"Error showing response: {e}")
    exit(1)
