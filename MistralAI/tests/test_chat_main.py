import unittest
from unittest.mock import patch, MagicMock
import os

from mistral_chat_app.chat_main import main


class TestChatMain(unittest.TestCase):

    @patch('mistral_chat_app.chat_main.load_dotenv')
    @patch('mistral_chat_app.chat_main.os.getenv')
    def test_missing_api_key(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            main()

    @patch('mistral_chat_app.chat_main.get_prompt_from_md')
    @patch('mistral_chat_app.chat_main.Mistral')
    @patch('mistral_chat_app.chat_main.show_response')
    @patch('mistral_chat_app.chat_main.log_interaction')
    @patch('mistral_chat_app.chat_main.load_dotenv')
    @patch('mistral_chat_app.chat_main.os.getenv')
    def test_main_success(self, mock_getenv, mock_load_dotenv, mock_log_interaction, mock_show_response, mock_mistral, mock_get_prompt_from_md):
        # Mock the return values of the patched functions
        mock_getenv.return_value = "test_key"
        mock_get_prompt_from_md.return_value = "Test prompt"
        mock_mistral.return_value.chat.complete.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )

        # Call the main function
        main()

        # Assert that the functions were called with the expected arguments
        mock_load_dotenv.assert_called_once()
        mock_get_prompt_from_md.assert_called_once()
        mock_mistral.assert_called_once_with(
            api_key="test_key",
        )
        mock_mistral.return_value.chat.complete.assert_called_once()
        mock_show_response.assert_called_once()
        mock_log_interaction.assert_called_once()


if __name__ == '__main__':
    unittest.main()
