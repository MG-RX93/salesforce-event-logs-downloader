import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Globals for caching
_cached_token = None
_token_expiry = datetime.now()
_instance_url = None


def get_access_token() -> tuple:
    """Get current Salesforce access token, either from cache or request a new one."""
    global _instance_url
    access_token = get_cached_access_token()

    if access_token is None:
        access_token, instance_url, issued_at = request_new_access_token()
        cache_access_token(access_token, instance_url, issued_at)
        _instance_url = instance_url

    return access_token, _instance_url


def get_cached_access_token() -> str:
    """Get cached access token if still valid."""
    if _cached_token and not is_token_expired():
        return _cached_token
    return None


def is_token_expired() -> bool:
    """Check if the cached access token has expired."""
    global _token_expiry
    return datetime.now() < _token_expiry


def request_new_access_token() -> tuple:
    """Request a new access token from Salesforce."""
    auth_url = os.getenv("SF_AUTH_URL")
    client_id = os.getenv("SF_CONSUMER_KEY")
    client_secret = os.getenv("SF_CONSUMER_SECRET")
    username = os.getenv("SF_USERNAME")
    password = os.getenv("SF_PASSWORD")

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
    }

    response = requests.post(auth_url, data=data)
    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.text}")

    auth_response = response.json()
    validate_auth_response(auth_response)

    return (
        auth_response["access_token"],
        auth_response["instance_url"],
        auth_response["issued_at"],
    )


def validate_auth_response(response: dict):
    """Validate the authentication response from Salesforce."""
    required_keys = ["access_token", "instance_url", "issued_at"]
    if not all(key in response for key in required_keys):
        raise Exception("Authentication response is missing required keys.")


def cache_access_token(access_token: str, instance_url: str, issued_at: str):
    """Cache the new access token and set its expiry time."""
    global _cached_token, _token_expiry, _instance_url
    token_lifetime = int(os.getenv("SF_TOKEN_LIFETIME", "3600"))  # Default to 1 hour

    _cached_token = access_token
    _instance_url = instance_url
    issued_at_datetime = datetime.fromtimestamp(int(issued_at) / 1000)
    _token_expiry = issued_at_datetime + timedelta(seconds=token_lifetime)
