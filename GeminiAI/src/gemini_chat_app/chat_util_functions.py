import tkinter as tk
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel
from datetime import datetime

# -- Util functions definitions --


def get_prompt_from_md(filename="input_prompt.md"):
    """Reads prompt text from a specified markdown file.

    This function attempts to open and read the content of a file. It is
    designed to fetch the user prompt for the Mistral model from an external
    file to keep the prompt separate from the application logic.

    :param filename: The path to the markdown file containing the prompt.
    :type filename: str
    :returns: The content of the file as a string.
    :rtype: str
    :raises SystemExit: If the file cannot be found or another reading error occurs.
    
    :side-effects: Prints an error message to stdout and exits the application on failure.
    """    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Prompt file {filename} not found")
        exit(1)
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        exit(1)


def log_interaction(prompt, start_time, end_time, duration, response,
                    filename="output_results.md"):
    """Logs the details of a user-model interaction to a markdown file.

    Appends a formatted record of the prompt, response, and timing information
    to the specified log file. If the file does not exist, it will be created.
    The logged information includes timestamps, duration, the user prompt,
    and the model's response.

    :param prompt: The user prompt sent to the model.
    :type prompt: str
    :param start_time: The timestamp when the API call was initiated.
    :type start_time: datetime.datetime
    :param end_time: The timestamp when the API call completed.
    :type end_time: datetime.datetime
    :param duration: The time difference between start and end time.
    :type duration: datetime.timedelta
    :param response: The content of the model's response.
    :type response: str
    :param filename: The path to the markdown log file. Defaults to "output_results.md".
    :type filename: str
    :raises SystemExit: If there is an error writing to the file.

    :side-effects: Writes to the filesystem. Prints an error and exits on failure.
    """
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(
                f"\n### Interaction at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"- **User Prompt**:  \n{prompt}\n\n")
            f.write(
                f"- **Start Time**: `{start_time.strftime('%Y-%m-%d %H:%M:%S')}`\n")
            f.write(
                f"- **End Time**: `{end_time.strftime('%Y-%m-%d %H:%M:%S')}`\n")
            f.write(f"- **Duration**: `{str(duration)}`\n")
            f.write("\n")
            f.write(f"- **Model Response**:  \n{response}\n\n")
            f.write("---\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
        exit(1)


def copy_to_clipboard(window, response_text):
    """Copies the provided response text to the system clipboard.

    This function interacts with the tkinter window to access the system's
    clipboard, clearing any previous content and appending the new text.

    :param window: The tkinter root window object.
    :type window: tkinter.Tk
    :param response_text: The text to be copied to the clipboard.
    :type response_text: str
    :returns: None
    
    :side-effects: Modifies the system clipboard. Prints a confirmation to stdout.
    """
    if window and response_text:
        window.clipboard_clear()
        window.clipboard_append(response_text)
        window.update()
        print("Copied to clipboard!")


def show_response(title_text, response_html, response_text):
    """Creates and displays a GUI window to show the model's response.

    This function builds a tkinter window containing the HTML-formatted response,
    a copy-to-clipboard button, and a close button. It handles the entire
    lifecycle of the GUI window, including entering the main event loop.

    :param title_text: The title for the response window.
    :type title_text: str
    :param response_html: The model's response formatted as an HTML string.
    :type response_html: str
    :param response_text: The raw text version of the model's response (for clipboard).
    :type response_text: str
    :returns: None
    """    
    window = tk.Tk()
    window.title(title_text)  # Updated title
    window.geometry("1024x768")
    window.resizable(True, True)

    response_frame = tk.Frame(window)
    response_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scroll_frame = scrolledtext.ScrolledText(
        response_frame, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
    scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    html_label = HTMLLabel(
        scroll_frame, html=response_html, width=600, height=300)
    html_label.pack(fill=tk.BOTH, expand=True)

    scroll_frame.bind(
        "<Control-c>", lambda event: window.clipboard_append(scroll_frame.get("1.0", "end-1c")))
    scroll_frame.bind(
        "<Control-v>", lambda event: scroll_frame.insert("insert", window.clipboard_get()))

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    copy_button = tk.Button(
        button_frame,
        text="Copy to Clipboard",
        command=lambda: copy_to_clipboard(window, response_text),
        font=("Arial", 12)
    )
    copy_button.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(button_frame,
                             text="Close",
                             command=window.destroy,
                             font=("Arial", 12))
    close_button.pack(side=tk.LEFT, padx=10)

    window.mainloop()
