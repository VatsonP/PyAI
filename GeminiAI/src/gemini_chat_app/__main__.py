"""Executable entry point for the gemini_chat_app package.

This module allows the package to be run directly from the command line
using `python -m gemini_chat_app`. It imports and calls the `main` function
from the `chat_main` module, effectively starting the application.
"""

from . import chat_main

if __name__ == "__main__":
    chat_main.main()
