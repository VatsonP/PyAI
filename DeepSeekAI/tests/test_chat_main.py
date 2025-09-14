import unittest
from unittest.mock import patch, MagicMock
import os

# It is necessary to add the src directory to the path to be able to import the modules
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from chat_main import main

class TestChatMain(unittest.TestCase):

    @patch('chat_main.get_prompt_from_md')
    @patch('chat_main.OpenAI')
    @patch('chat_main.show_response')
    @patch('chat_main.log_interaction')
    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    def test_main_success(self, mock_log_interaction, mock_show_response, mock_openai, mock_get_prompt_from_md):
        # Mock the return values of the patched functions
        mock_get_prompt_from_md.return_value = "Test prompt"
        mock_openai.return_value.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )

        # Call the main function
        main()

        # Assert that the functions were called with the expected arguments
        mock_get_prompt_from_md.assert_called_once()
        mock_openai.assert_called_once_with(
            api_key="test_key",
            base_url="https://api.deepseek.com/v1",
        )
        mock_openai.return_value.chat.completions.create.assert_called_once()
        mock_show_response.assert_called_once()
        mock_log_interaction.assert_called_once()

if __name__ == '__main__':
    unittest.main()
