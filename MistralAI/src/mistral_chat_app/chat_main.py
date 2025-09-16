import os
from mistralai import Mistral
import markdown
from datetime import datetime
from dotenv import load_dotenv


# Import functions from the separate file
from mistral_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, show_response


def main():
    # Your entire application logic from chat_main.py goes here.
    # For example:
    # prompt = get_prompt_from_md('prompt_template.md')
    # ...and so on.
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

    # Show response in GUI window
    try:
        show_response("Mistral AI Response", response_html, response_text)
    except Exception as e:
        print(f"Error showing response: {e}")
        exit(1)


if __name__ == "__main__":
    main()
