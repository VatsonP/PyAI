
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch, MagicMock
import tkinter as tk
import os
 

from gemini_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, copy_to_clipboard, show_response


class TestChatUtilFunctions(unittest.TestCase):

    def test_get_prompt_from_md(self):
        """
        Test that get_prompt_from_md reads from a file correctly.
        """
        mock_content = "Test prompt"
        m = mock_open(read_data=mock_content)
        with patch("builtins.open", m):
            result = get_prompt_from_md("test_prompt.md")
            self.assertEqual(result, mock_content)

    def test_log_interaction(self):
        """
        Test that log_interaction writes to a file correctly.
        """
        prompt = "Test prompt"
        start_time = datetime(2023, 1, 1, 12, 0, 0)
        end_time = datetime(2023, 1, 1, 12, 0, 5)
        duration = end_time - start_time
        response = "Test response"
        m = mock_open()
        with patch("builtins.open", m):
            log_interaction(prompt, start_time, end_time, duration, response, "test_log.md")
            m().write.assert_called()

    @patch('tkinter.Tk')
    def test_copy_to_clipboard(self, mock_tk):
        # Mock the tkinter window and its methods
        mock_window = MagicMock()
        mock_tk.return_value = mock_window

        # Call the function to be tested
        copy_to_clipboard(mock_window, "Test response")

        # Assert that the clipboard functions were called
        mock_window.clipboard_clear.assert_called_once()
        mock_window.clipboard_append.assert_called_once_with("Test response")
        mock_window.update.assert_called_once()

    @patch('gemini_chat_app.chat_util_functions.HTMLLabel')
    def test_show_response(self, mock_HTMLLabel):
        # Create a real Tk instance to serve as the root window
        root = tk.Tk()

        # Call the function to be tested
        with patch('tkinter.Tk', return_value=root):
            with patch.object(root, 'mainloop'):
                show_response("Test Title", "<h1>Test</h1>", "Test response")

            self.assertEqual(root.title(), "Test Title")
            mock_HTMLLabel.assert_called_once()
            root.destroy()

if __name__ == "__main__":
    unittest.main()
