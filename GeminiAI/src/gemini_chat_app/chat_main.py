"""Core application logic for the Gemini AI Chat Application.

This module serves as the main orchestrator for the application. It handles
loading configuration, initializing the API client, fetching the user prompt,
making the API call to Gemini, logging the interaction, and displaying the
response in a GUI window.
"""

import tkinter as tk
import os
import google.generativeai as genai
import markdown
from datetime import datetime
from dotenv import load_dotenv

from gemini_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, show_response

os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''


def show_response_gui_window(title, response_html, response_text):
    """Creates, configures, and runs the main tkinter GUI window.

    This function is responsible for the entire lifecycle of the GUI window.
    It creates the root window, sets its properties, populates it using the
    show_response utility function, and then starts the main event loop.

    :param title: The title for the main window.
    :type title: str
    :param response_html: The HTML content to be displayed.
    :type response_html: str
    :param response_text: The raw text content for the clipboard.
    :type response_text: str
    :raises SystemExit: Exits if any error occurs during UI rendering.

    :side-effects: This is a blocking call that enters the tkinter main event loop.
    """
    try:
        root = tk.Tk()
        root.geometry("1024x768")
        root.resizable(True, True)

        show_response(root, title, response_html, response_text)
        root.mainloop()
    except Exception as e:
        print(f"Error showing response: {e}")
        exit(1)


def main():
    """The main entry point for the Gemini Chat Application.

    This function orchestrates the entire application flow:
    1. Loads environment variables from a .env file.
    2. Retrieves and validates the Gemini API key.
    3. Initializes the Gemini API client.
    4. Reads a user prompt from a markdown file.
    5. Sends the prompt to the Gemini API and measures the response time.
    6. Logs the complete interaction (prompt, response, timing) to a file.
    7. Converts the response from markdown to HTML.
    8. Displays the HTML response in a graphical tkinter window.

    :raises ValueError: If the GEMINI_API_KEY environment variable is not set.
    :raises SystemExit: The application will exit if it encounters errors during
                        API initialization, file I/O, or UI rendering.

    :side-effects:
        - Reads from environment variables and files (`.env`, `input_prompt.md`).
        - Performs network requests to the Gemini API.
        - Writes to a log file (`output_results.md`).
        - Renders a GUI window.
    """
    print("Running chat_main.py's main function...")

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
            model_name="gemini-2.5-flash-lite",
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

    # Query the Gemini API, Set input prompt and get model response
    try:
        prompt_text = get_prompt_from_md()
        start_time = datetime.now()
        response = chat_session.send_message(prompt_text)
        end_time = datetime.now()
        duration = end_time - start_time
        response_text = response.text
        log_interaction(prompt_text, start_time,
                        end_time, duration, response_text)
    except Exception as e:
        print(f"Error sending message or processing response: {e}")
        exit(1)

    # Convert response text to Markdown-formatted HTML
    try:
        response_html = markdown.markdown(response_text)
    except Exception as e:
        print(f"Error converting response text to Markdown: {e}")
        exit(1)

    # Display the final response in its own GUI window
    show_response_gui_window(
        "Gemini AI Response", response_html, response_text)


if __name__ == "__main__":
    main()
