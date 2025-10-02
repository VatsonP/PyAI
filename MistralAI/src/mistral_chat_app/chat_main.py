import tkinter as tk
import os
from mistralai import Mistral
import markdown
from datetime import datetime
from dotenv import load_dotenv

# Import functions from the separate file
from mistral_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, show_response


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
    """The main entry point for the Mistral Chat Application.

    This function orchestrates the entire application flow:
    1. Loads environment variables from a .env file.
    2. Retrieves and validates the Mistral API key.
    3. Initializes the Mistral API client.
    4. Reads a user prompt from a markdown file.
    5. Sends the prompt to the Mistral API and measures the response time.
    6. Logs the complete interaction (prompt, response, timing) to a file.
    7. Converts the response from markdown to HTML.
    8. Displays the HTML response in a graphical tkinter window.

    :raises ValueError: If the MISTRAL_API_KEY environment variable is not set.
    :raises SystemExit: The application will exit if it encounters errors during
                        API initialization, file I/O, or UI rendering.

    :side-effects:
        - Reads from environment variables and files (`.env`, `input_prompt.md`).
        - Performs network requests to the Mistral API.
        - Writes to a log file (`output_results.md`).
        - Renders a GUI window.
    """
    print("Running chat_main.py's main function...")

    # Load environment variables from the .env file (if present)
    load_dotenv()

    # Retrieve the API key from the .env file
    api_key_txt = os.getenv("MISTRAL_API_KEY")

    # Check for empty API key
    if not api_key_txt:
        raise ValueError("Please set the MISTRAL_API_KEY in the .env file")

    # Define the Mistral model and initialize the client
    model = "mistral-large-latest"
    try:
        client = Mistral(api_key=api_key_txt)
    except Exception as e:
        print(f"Error initializing Mistral client: {e}")
        exit(1)

    # Query the Mistral API, Set input prompt and get model response
    try:
        prompt_text = get_prompt_from_md()
        start_time = datetime.now()

        response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                },
            ]
        )
        end_time = datetime.now()
        duration = end_time - start_time
        # Use the appropriate method or attribute to get the response text
        # Assuming the response object has a `choices` attribute and a structure like:
        try:
            # type: ignore
            response_text = response.choices[0].message.content
        except AttributeError:
            print("Error accessing response text")
            exit(1)

        log_interaction(prompt_text, start_time,
                        end_time, duration, response_text)
    except Exception as e:
        print(f"Error querying Mistral API: {e}")
        exit(1)

    # Convert response text to Markdown-formatted HTML
    try:
        response_html = markdown.markdown(response_text)  # type: ignore
    except Exception as e:
        print(f"Error converting response text to Markdown: {e}")
        exit(1)

    # Display the final response in its own GUI window
    show_response_gui_window(
        "Mistral AI Response", response_html, response_text)


if __name__ == "__main__":
    main()
