import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path to allow for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat_main import main

class TestChatMain(unittest.TestCase):

    @patch('os.getenv')
    def test_missing_api_key(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            main()

    @patch('chat_main.show_response')
    @patch('chat_main.markdown.markdown')
    @patch('chat_main.log_interaction')
    @patch('chat_main.get_prompt_from_md')
    @patch('chat_main.genai')
    @patch('os.getenv')
    def test_main_flow(self, mock_getenv, mock_genai, mock_get_prompt, mock_log, mock_markdown, mock_show_response):
        """
        Test the main flow of the application.
        """
        # Configure the mock for os.getenv
        def getenv_side_effect(key):
            if key == "GEMINI_API_KEY":
                return "test_api_key"
            return None
        mock_getenv.side_effect = getenv_side_effect

        # Mock the generative model and chat session
        mock_model = MagicMock()
        mock_chat_session = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat_session

        # Mock the response from the chat session
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_chat_session.send_message.return_value = mock_response

        mock_get_prompt.return_value = "Test prompt"

        # Run the main function
        main()

        # Assertions
        mock_genai.configure.assert_called_with(api_key="test_api_key")
        mock_model.start_chat.assert_called_once()
        mock_chat_session.send_message.assert_called_with("Test prompt")
        mock_log.assert_called_once()
        mock_markdown.assert_called_with("Test response")
        mock_show_response.assert_called_with("Gemini AI Response", mock_markdown.return_value, "Test response")

if __name__ == "__main__":
    unittest.main()