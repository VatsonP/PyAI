import unittest
from unittest.mock import patch, MagicMock

from gemini_chat_app.chat_main import main


class TestChatMain(unittest.TestCase):

    @patch('gemini_chat_app.chat_main.load_dotenv')
    @patch('gemini_chat_app.chat_main.os.getenv')
    def test_missing_api_key(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            main()

    @patch('gemini_chat_app.chat_main.get_prompt_from_md')
    @patch('gemini_chat_app.chat_main.genai')
    @patch('gemini_chat_app.chat_main.show_response')
    @patch('gemini_chat_app.chat_main.log_interaction')
    @patch('gemini_chat_app.chat_main.tk.Tk')
    @patch('gemini_chat_app.chat_main.load_dotenv')
    @patch('gemini_chat_app.chat_main.os.getenv')
    def test_main_success(self, mock_getenv, mock_load_dotenv, mock_tk, mock_log_interaction, mock_show_response, mock_genai, mock_get_prompt_from_md):
        mock_getenv.return_value = "test_api_key"
        mock_get_prompt_from_md.return_value = "Test prompt"

        mock_model = MagicMock()
        mock_chat_session = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test response"

        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat_session
        mock_chat_session.send_message.return_value = mock_response

        main()

        mock_load_dotenv.assert_called_once()
        mock_genai.configure.assert_called_with(api_key="test_api_key")
        mock_genai.GenerativeModel.assert_called_once()
        mock_model.start_chat.assert_called_once()
        mock_chat_session.send_message.assert_called_with("Test prompt")
        mock_show_response.assert_called_once()
        mock_log_interaction.assert_called_once()

if __name__ == "__main__":
    unittest.main()
