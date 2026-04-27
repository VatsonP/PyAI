# DeepSeek AI Chat Application

Welcome to the DeepSeek AI Chat Application!
This is a simple but practical desktop application that allows you to interact with DeepSeek language models through a clean, graphical user interface (GUI).

This project is designed to be a learning resource for people who are getting started with Python. It demonstrates a clean project structure, dependency management with `pyproject.toml`, API integration, GUI rendering with `tkinter`, Markdown formatting, and unit testing.

## Features

- **Direct DeepSeek AI Integration**: Connects to the DeepSeek API and sends prompts directly to a configured DeepSeek model.
- **File-Based Prompts**: Write prompts in `input_prompt.md` instead of typing long instructions in the terminal.
- **Graphical User Interface (GUI)**: Displays the final AI response in a readable desktop window.
- **Markdown Rendering**: Converts the returned text into formatted HTML so lists, headings, bold text, and code blocks remain readable.
- **Interaction Logging**: Appends each prompt, response, and timing record to `output_results.md`.
- **Clipboard Functionality**: Lets you copy the full response with one button click.
- **Modern Python Project Layout**: Uses a `src` layout, script entry points, and isolated tests.

## Getting Started: A Guide for Newcomers

This guide walks through the full setup process so you can run the project locally with minimal guesswork.

### Prerequisites

Before you begin, make sure you have the following:

1. **Python 3.12 or newer**
   Check your installed version:

   ```bash
   python --version
   ```

2. **A DeepSeek API Key**
   You need access to the DeepSeek API platform.

   General setup flow:
   - Create or sign in to your DeepSeek account.
   - Generate an API key for programmatic access.
   - Keep the key private and store it only in your local `.env` file.

### Installation & Setup

Follow these steps from a terminal opened in your development workspace.

#### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd DeepSeekAI
```

#### Step 2: Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python and from other projects.

```bash
python -m venv .venv
```

Activate it:

```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

When activation succeeds, your terminal prompt usually shows `(.venv)`.

#### Step 3: Install Dependencies

This project uses `pyproject.toml` for dependency management.

```bash
pip install -e .[dev]
```

This installs:
- the application itself in editable mode
- runtime dependencies such as `openai`, `tkhtmlview`, `markdown`, and `python-dotenv`
- development tools such as `pytest`

#### Step 4: Configure Your API Key

The application reads the DeepSeek API key from an environment file named `.env`.

Create or edit `.env` in the project root and add:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

Notes:
- Do not commit this file with a real key.
- Keep the key on a single line.
- The application loads this value using `python-dotenv`.

#### Step 5: Create Your First Prompt

The application reads the user prompt from `input_prompt.md`.

Example:

```markdown
Explain the concept of a Python virtual environment to a beginner. Use a simple analogy.
```

At this point the project is ready to run.

## Running the Application

With the virtual environment active, run:

```bash
deepseek-chat
```

This command exists because `pyproject.toml` defines the script entry point.

When the app runs, it will:

1. Read the content of `input_prompt.md`.
2. Load `DEEPSEEK_API_KEY` from `.env`.
3. Configure the DeepSeek client and create a model request.
4. Send the prompt to DeepSeek.
5. Convert the response from Markdown to HTML.
6. Save the prompt, response, and timing data to `output_results.md`.
7. Open a `tkinter` window that displays the response.

## Running the Tests

This project includes unit tests for both the orchestration logic and the utility functions.

If `pytest` is installed in your environment, run:

```bash
pytest
```

If `pytest` is not installed, you can still run the tests with the standard library:

```bash
python -m unittest discover tests -v
```

The tests are designed to mock external systems such as the GUI and API calls, so they can run without opening a real application window or making a network request.

## Project Structure Explained

Understanding the file layout makes the code easier to navigate.

```text
DeepSeekAI/
|-- .env                  # Local environment variables, including DEEPSEEK_API_KEY
|-- input_prompt.md       # Prompt text sent to the model
|-- output_results.md     # Saved prompt/response history and timing data
|-- pyproject.toml        # Project metadata, dependencies, and script entry points
|-- README.md             # Project documentation
|-- GEMINI.md             # Additional project notes carried from the original demo
|-- src/
|   `-- deepseek_chat_app/
|       |-- __init__.py
|       |-- __main__.py
|       |-- chat_main.py
|       `-- chat_util_functions.py
`-- tests/
    |-- test_chat_main.py
    `-- test_chat_util_functions.py
```

- **`pyproject.toml`**: Defines the package metadata, required Python version, dependencies, optional dev dependencies, and the `deepseek-chat` command.
- **`src/deepseek_chat_app/chat_main.py`**: Contains the high-level flow of the application, including API setup, prompt loading, response handling, logging, and GUI startup.
- **`src/deepseek_chat_app/chat_util_functions.py`**: Contains reusable helpers for prompt reading, interaction logging, clipboard handling, and response UI construction.
- **`tests/`**: Contains automated tests for both the main flow and the utility functions.

## How It Works: The Code Flow

When you run `deepseek-chat`, the application follows this sequence:

1. The `main()` function in `chat_main.py` starts the program.
2. `load_dotenv()` loads environment variables from `.env`.
3. The code reads `DEEPSEEK_API_KEY` and validates that it exists.
4. An `OpenAI` client is initialized with the DeepSeek base URL.
5. The request is sent to the `deepseek-chat` model through `client.chat.completions.create(...)`.
6. `get_prompt_from_md()` reads the content of `input_prompt.md`.
7. The returned text is extracted from `response.choices[0].message.content`.
8. The interaction is logged to `output_results.md` together with timestamps and total duration.
9. The response text is converted from Markdown to HTML.
10. `show_response_gui_window()` creates the main `tkinter` window.
11. `show_response()` builds the widgets that render the response and the action buttons.

## Notes About the Current DeepSeek Implementation

A few provider-specific details are worth knowing:

- The current model name in code is `deepseek-chat`.
- The project uses the `openai` Python client with a custom `base_url` pointing to DeepSeek's API.
- The application currently sends a single prompt per run and does not preserve multi-turn chat history between separate launches.
- The provider response handling assumes the OpenAI-compatible response shape exposed by DeepSeek.

## Troubleshooting

If the application does not run as expected, check these common issues:

- **`Please set the DEEPSEEK_API_KEY in the .env file`**
  The `.env` file is missing, empty, or does not contain `DEEPSEEK_API_KEY`.

- **`No module named pytest`**
  Install development dependencies with:

  ```bash
  pip install -e .[dev]
  ```

- **GUI window does not appear**
  Verify that your Python installation includes `tkinter` and that you are running in a desktop environment that supports GUI applications.

- **Prompt file not found**
  Make sure `input_prompt.md` exists in the project root.

## Summary

This project is a compact example of how to combine:

- environment-based API configuration
- file-based prompt input
- a desktop GUI
- Markdown rendering
- interaction logging
- automated unit testing

It is intentionally small, which makes it a good reference project for learning or for adapting to another LLM provider with a similar architecture.
