# Gemini AI Chat Project

A Python-based chat application that leverages the power of Google's Gemini API to provide intelligent and context-aware conversations.

## Features

*   **Interactive Chat:** Engage in conversations with the Gemini AI.
*   **Extensible:** Easily add new functions and capabilities.
*   **Session Management:** (Future feature) To maintain conversation history.
*   **Easy to Run:** Simple setup and execution.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.12+
*   `pipenv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd AI_Studio
    ```

2.  **Install dependencies:**
    This project uses `pipenv` to manage dependencies. To install them, run:
    ```bash
    pipenv install
    ```

3.  **Set up your environment:**
    Make sure you have your Gemini API key set up in your environment.
    ```bash
    export GOOGLE_API_KEY='YOUR_API_KEY'
    ```
    *(On Windows, use `set GOOGLE_API_KEY=YOUR_API_KEY`)*

### Running the Application

To start the chat application, run the main script:

```bash
pipenv run python chat_main.py
```

## Usage

After starting the application, you can type your messages in the console. The AI will respond to your prompts. You can modify the `input_prompt.md` to test different scenarios.

## Project Structure

Here's an overview of the key files in this project:

*   `chat_main.py`: The main entry point for the chat application.
*   `chat_util_functions.py`: Contains helper functions and utilities used by the main application.
*   `Pipfile` & `Pipfile.lock`: Manage the project's Python dependencies.
*   `GEMINI.md`: This file - providing project documentation.
*   `input_prompt.md`: Can be used to store and test various input prompts.
*   `output_results.md`: Can be used to log or review the output from the AI.
*   `.gemini/`: Contains configuration files for the Gemini CLI.
