import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime


# To help load src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import (
    get_access_token,
    get_cached_access_token,
    is_token_expired,
    request_new_access_token,
    validate_auth_response,
)


class TestSrcModule(unittest.TestCase):
    @patch("src.auth.datetime")
    def test_is_token_expired(self, mock_datetime):
        # Set up mock datetime
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        global _token_expiry
        _token_expiry = datetime(2023, 1, 1, 11, 0, 0)

        # Call function
        expired = is_token_expired()

        # Assert token is expired
        self.assertTrue(expired)


if __name__ == "__main__":
    unittest.main()
