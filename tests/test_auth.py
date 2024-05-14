import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src import (
    get_access_token,
    get_cached_access_token,
    is_token_expired,
    request_new_access_token,
    validate_auth_response,
)