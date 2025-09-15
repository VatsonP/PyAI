import os
from openai import OpenAI  # Changed import
import markdown
from datetime import datetime
from dotenv import load_dotenv

# Import functions from the separate file
from deepseek_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, show_response


def main():
    # Load environment variables from the .env file (if present)
    load_dotenv()

    # Retrieve the API key from the .env file
    api_key_txt = os.getenv("DEEPSEEK_API_KEY")

    # Check for empty API key
    if not api_key_txt:
        raise ValueError("Please set the DEEPSEEK_API_KEY in the .env file")

    # Set the DEEPSEEK_API_KEY as an environment variable (example key: "12345abcde")
    os.environ["DEEPSEEK_API_KEY"] = api_key_txt

    # Changed model and client initialization
    model = "deepseek-chat"
    try:
        client = OpenAI(
            api_key=api_key_txt,
            base_url="https://api.deepseek.com/v1",  # DeepSeek API endpoint
        )
    except Exception as e:
        print(f"Error initializing DeepSeek client: {e}")  # Updated message
        exit(1)

    # Query the DeepSeek API, Set input prompt and get model response
    try:
        prompt_text = get_prompt_from_md()
        start_time = datetime.now()

        response = client.chat.completions.create(
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
            # Response structure is similar to OpenAI's
            response_text = response.choices[0].message.content
        except AttributeError:
            print("Error accessing response text")
            exit(1)

        log_interaction(prompt_text, start_time,
                        end_time, duration, response_text)
    except Exception as e:
        print(f"Error querying DeepSeek API: {e}")
        exit(1)

    # Rest of the code remains the same
    try:
        response_html = markdown.markdown(response_text)
    except Exception as e:
        print(f"Error converting response text to Markdown: {e}")
        exit(1)

    # Show response in GUI window
    try:
        show_response("DEEPSEEK AI Response", response_html, response_text)
    except Exception as e:
        print(f"Error showing response: {e}")
        exit(1)


if __name__ == "__main__":
    main()
