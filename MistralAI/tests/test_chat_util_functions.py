import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tkinter as tk

from mistral_chat_app.chat_util_functions import get_prompt_from_md, log_interaction, copy_to_clipboard, show_response


class TestChatUtilFunctions(unittest.TestCase):

    def test_get_prompt_from_md_success(self):
        # Mock the open function to simulate file reading
        m = mock_open(read_data="Test prompt")
        with patch("builtins.open", m):
            prompt = get_prompt_from_md("test_prompt.md")
            self.assertEqual(prompt, "Test prompt")

    def test_get_prompt_from_md_file_not_found(self):
        # Mock the open function to raise FileNotFoundError
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit):
                get_prompt_from_md("non_existent_file.md")

    @patch('builtins.open', new_callable=mock_open)
    def test_log_interaction(self, mock_open_file):
        # Mock the datetime objects
        start_time = MagicMock()
        end_time = MagicMock()
        duration = MagicMock()

        # Call the function to be tested
        log_interaction("Test prompt", start_time, end_time,
                        duration, "Test response", "test_log.md")

        # Assert that the file was opened in append mode and the content was written correctly
        mock_open_file.assert_called_with("test_log.md", "a", encoding="utf-8")
        mock_open_file().write.assert_called()

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

    @patch('mistral_chat_app.chat_util_functions.HTMLLabel')
    def test_show_response(self, mock_HTMLLabel):
        # Create a real Tk instance to serve as the root window
        root = tk.Tk()

        # Call the function to be tested
        with patch('tkinter.Tk', return_value=root):
            with patch.object(root, 'mainloop'):
                show_response("Test Title", "<h1>Test</h1>", "Test response")

        # Assert that the tkinter window was created and configured correctly
        self.assertEqual(root.title(), "Test Title")
        mock_HTMLLabel.assert_called_once()
        root.destroy()


if __name__ == '__main__':
    unittest.main()
