# This acts as the main entry point for the 'deepseek_chat_app' package.
# It imports the `main` function from the `chat_main` module and runs it.

from . import chat_main

if __name__ == "__main__":
    chat_main.main()