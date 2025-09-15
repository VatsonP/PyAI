import tkinter as tk
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel
from datetime import datetime


# -- Util functions definitions --

def get_prompt_from_md(filename="input_prompt.md"):
    # Prompt reading function
    """Read prompt text from markdown file."""
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
    # Prompt and model output logging function
    """Log interaction details to markdown file."""
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
    # Copy response to clipboard
    if window and response_text:
        window.clipboard_clear()
        window.clipboard_append(response_text)
        window.update()
        print("Copied to clipboard!")


def show_response(title_text, response_html, response_text):
    # Create GUI window
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
