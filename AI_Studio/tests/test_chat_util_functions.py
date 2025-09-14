
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

# Add the parent directory to the Python path to allow for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat_util_functions import get_prompt_from_md, log_interaction

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

if __name__ == "__main__":
    unittest.main()
