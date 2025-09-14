# Mistral AI Chat Project

A Python-based chat application that leverages the power of Mistral AI API to provide intelligent and context-aware conversations.

## Features

*   **Interactive Chat**: Engage in conversations with the Mistral AI.
*   **GUI Display**: Displays the response in a user-friendly GUI window.
*   **Logging**: Logs all interactions to a markdown file.
*   **Easy to Run**: Simple setup and execution.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.x
*   `pipenv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd MistralAI
    ```

2.  **Install dependencies:**
    This project uses `pipenv` to manage dependencies. To install them, run:
    ```bash
    pipenv install
    ```

3.  **Set up your environment:**
    Create a `.env` file in the root directory and add your Mistral API key:
    ```
    MISTRAL_API_KEY='YOUR_API_KEY'
    ```

### Running the Application

To start the chat application, run the main script:

```bash
pipenv run python src/chat_main.py
```

## Testing

This project does not have a dedicated test suite yet.

## Usage

After starting the application, you can type your messages in the `input_prompt.md` file. The AI will respond to your prompts, and the response will be displayed in a new window.

## Project Structure

Here's an overview of the key files in this project:

*   `src/chat_main.py`: The main entry point for the chat application.
*   `src/chat_util_functions.py`: Contains helper functions and utilities used by the main application.
*   `Pipfile` & `Pipfile.lock`: Manage the project's Python dependencies.
*   `GEMINI.md`: This file - providing project documentation.
*   `input_prompt.md`: Can be used to store and test various input prompts.
*   `output_results.md`: Can be used to log or review the output from the AI.
*   `.gemini/`: Contains configuration files for the Gemini CLI.
