import unittest
from unittest.mock import patch, MagicMock
import os

from gemini_chat_app.chat_main import main

class TestChatMain(unittest.TestCase):

    @patch('gemini_chat_app.chat_main.load_dotenv')
    @patch('gemini_chat_app.chat_main.os.getenv')
    def test_missing_api_key(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            main()

    @patch('gemini_chat_app.chat_main.show_response')
    @patch('gemini_chat_app.chat_main.markdown.markdown')
    @patch('gemini_chat_app.chat_main.log_interaction')
    @patch('gemini_chat_app.chat_main.get_prompt_from_md')
    @patch('gemini_chat_app.chat_main.genai')
    @patch('gemini_chat_app.chat_main.os.getenv')
    def test_main_flow(self, mock_getenv, mock_genai, mock_get_prompt, mock_log, mock_markdown, mock_show_response):
        """
        Test the main flow of the application.
        """
        # Configure mocks
        mock_getenv.return_value = "test_api_key"
        mock_get_prompt.return_value = "Test prompt"

        # Mock the generative model and chat session
        mock_model = MagicMock()
        mock_chat_session = MagicMock()

        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat_session
        mock_chat_session.send_message.return_value = mock_response

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