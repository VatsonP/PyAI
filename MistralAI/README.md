
# Mistral AI Chat Application

Welcome to the Mistral AI Chat Application!
This is a simple but powerful desktop application that allows you to interact with Mistral AI's state-of-the-art language models through a clean, graphical user interface (GUI).

This project is designed to be a simple learning resource for those new to Python. It demonstrates modern Python development practices, including project structure, dependency management, testing, and handling APIs.

## Features

-   **Direct Mistral AI Integration**: Connects directly to the Mistral API to get high-quality responses.
-   **File-Based Prompts**: Write your complex, multi-line prompts in a simple Markdown file (`input_prompt.md`). No need to type them into a tiny terminal window!
-   **Graphical User Interface (GUI)**: Displays the AI's response in a clean, readable window built with Python's native `tkinter` library.
-   **Markdown Rendering**: The AI's response is rendered as formatted Markdown, preserving lists, bold text, code blocks, and more.
-   **Interaction Logging**: Automatically saves a history of your prompts, the AI's responses, and performance metrics to a log file (`output_results.md`).
-   **Clipboard Functionality**: Easily copy the AI's full response to your clipboard with a single button click.
-   **Modern Python Project**: Built using `pyproject.toml` for packaging and dependency management, a `src` layout for clean code separation, and a full suite of unit tests.

## Getting Started: A Guide for Newcomers

This guide will walk you through every step needed to get this application running on your machine.

### Prerequisites

Before you begin, you will need a few things:

1.  **Python 3.12 or newer**: This project uses modern Python features. You can check your version by opening a terminal and running:
    ```bash
    python --version
    ```
2.  **A Mistral AI API Key**: You need an account with Mistral AI to get an API key.
    -   Go to the [Mistral AI Platform](https://console.mistral.ai/).
    -   Sign up or log in.
    -   Navigate to the "API Keys" section and create a new secret key.
    -   **Important**: Copy this key immediately and save it somewhere safe. You will not be able to see it again.

### Installation & Setup

Follow these steps carefully in your terminal.

#### Step 1: Clone the Repository

First, download the project code to your computer using Git.

```bash
git clone <your-repository-url>
cd MistralAI
```

#### Step 2: Create a Virtual Environment

A "virtual environment" is a private, isolated workspace for a Python project. It's a critical best practice that prevents package conflicts between different projects. We'll use Python's built-in `venv` module.

```bash
# Create the virtual environment in a folder named '.venv'
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

You'll know it's working because your terminal prompt will change to show `(.venv)` at the beginning.

#### Step 3: Install Dependencies

This project uses a `pyproject.toml` file to manage all required packages. The `-e .[dev]` part installs the project in "editable" mode and includes the "development" packages (like `pytest` for testing).

```bash
pip install -e .[dev]
```

#### Step 4: Configure Your API Key

You must provide your secret API key to the application. We do this securely using an environment variable file.

1.  Find the file named `.env` in the project directory.
2.  Open it in a text editor.
3.  You will see a line like this: `MISTRAL_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
4.  Replace `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` with the actual API key you got from the Mistral AI website.
5.  Save and close the file. The `python-dotenv` package we installed will automatically load this key for our application.

#### Step 5: Create Your First Prompt

The application reads your question or instruction from a file named `input_prompt.md`.

1.  Create a file named `input_prompt.md` in the root of the `MistralAI` directory.
2.  Open it and write anything you want to ask the AI. For example:

    ```markdown
    Explain the concept of a Python virtual environment to a beginner. Use a simple analogy.
    ```

You are now fully set up!

## Running the Application

With your virtual environment still active, run the following command in your terminal:

```bash
mistral-chat
```

This command works because it was defined as a `script` in our `pyproject.toml` file. It will:
1.  Read the content of `input_prompt.md`.
2.  Send it to the Mistral AI API.
3.  Open a GUI window on your screen with the formatted response.
4.  Append the results of the interaction to `output_results.md`.

## Running the Tests

This project comes with a suite of unit tests to ensure everything works correctly. Tests are crucial for maintaining code quality and preventing bugs.

To run the tests, make sure your virtual environment is active and then run:

```bash
pytest
```

You should see a report indicating that all tests have passed. Our tests are configured to run "headlessly," meaning they won't open any actual GUI windows during testing.

## Project Structure Explained

Understanding the layout of the files is key to understanding the project.

```
MistralAI/
|
|-- .env                     # <-- Your secret API key lives here. (DO NOT SHARE!)
|-- input_prompt.md          # <-- You write your AI prompts in this file.
|-- output_results.md        # <-- The application logs all interactions here.
|-- pyproject.toml           # <-- The heart of the project: config, dependencies, etc.
|
|-- src/                     # <-- All of our main application code is here.
|   `-- mistral_chat_app/
|       |-- __init__.py      # Makes this directory a Python "package".
|       |-- __main__.py      # Allows running the package as a script.
|       |-- chat_main.py     # The main logic: API calls, orchestration.
|       `-- chat_util_functions.py # Helper functions for GUI, logging, etc.
|
`-- tests/                   # <-- All of our tests live here.
    |-- test_chat_main.py
    `-- test_chat_util_functions.py
```

-   **`pyproject.toml`**: This is the modern standard for configuring Python projects. It tells Python what your project is called, what other packages it needs to run (`dependencies`), and defines convenient commands (`scripts`).
-   **`src/` layout**: Placing all application code inside a `src` directory is a best practice that cleanly separates the code you write from project configuration files.
-   **Separation of Concerns**: Notice how `chat_main.py` handles the high-level logic (the "what"), while `chat_util_functions.py` handles the low-level details (the "how"). This makes the code much easier to read, test, and maintain.

## How It Works: The Code Flow

When you run `mistral-chat`:

1.  The `main()` function in `chat_main.py` is called.
2.  `load_dotenv()` reads your `MISTRAL_API_KEY` from the `.env` file.
3.  The Mistral API client is initialized with your key.
4.  `get_prompt_from_md()` (from `chat_util_functions.py`) reads your `input_prompt.md` file.
5.  The prompt is sent to the Mistral `chat.complete` API endpoint.
6.  The response text is extracted and converted from Markdown to HTML.
7.  `log_interaction()` (from `chat_util_functions.py`) writes a complete record to `output_results.md`.
8.  Finally, `show_response_gui_window()` is called. This function creates the main `tkinter` window and then uses `show_response()` (from `chat_util_functions.py`) to populate it with the HTML content and buttons.
9.  The application waits for you to close the window.

---
