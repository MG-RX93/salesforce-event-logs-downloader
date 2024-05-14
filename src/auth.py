import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Globals for caching
_cached_token = None
_token_expiry = datetime.now()
_instance_url = None


def get_access_token() -> tuple:
    """
    Retrieves the current Salesforce access token, either from cache or by requesting a new one.

    Returns:
        tuple: A tuple containing the access token & Salesforce instance URL.
    """
    global _instance_url
    access_token = get_cached_access_token()

    if access_token is None:
        access_token, instance_url, issued_at = request_new_access_token()
        cache_access_token(access_token, instance_url, issued_at)
        _instance_url = instance_url

    return access_token, _instance_url


def get_cached_access_token() -> str:
    """
    Retrieves the cached access token if it is still valid.

    Returns:
        str: The cached access token, or None if the token has expired or is not cached.
    """
    if _cached_token and not is_token_expired():
        return _cached_token
    return None


def is_token_expired() -> bool:
    """
    Checks if the cached access token has expired.

    Returns:
        bool: True if the token has expired; False otherwise.
    """
    global _token_expiry
    return datetime.now() < _token_expiry


def request_new_access_token() -> tuple:
    """
    Requests a new access token from the Salesforce authentication endpoint.

    Returns:
        tuple: The new access token & instance URL.

    Raises:
        Exception: If the request fails or if the response from Salesforce is not as expected.
    """
    # Retrieve authentication credentials & endpoint from environment variables
    auth_url = os.getenv("SF_AUTH_URL")
    client_id = os.getenv("SF_CONSUMER_KEY")
    client_secret = os.getenv("SF_CONSUMER_SECRET")
    username = os.getenv("SF_USERNAME")
    password = os.getenv("SF_PASSWORD")

    # Prepare data payload for the authentication request
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
    }

    # Make the authentication request to Salesforce
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
    """
    Validates the authentication response from Salesforce.

    Parameters:
        response (dict): The JSON response received from the Salesforce authentication endpoint.

    Raises:
        Exception: If the response is missing required keys.
    """
    required_keys = ["access_token", "instance_url", "issued_at"]
    if not all(key in response for key in required_keys):
        raise Exception(
            "Authentication response from Salesforce is missing required keys."
        )


def cache_access_token(access_token: str, instance_url: str, issued_at: str):
    """
    Caches the new access token & calculates its expiry time.

    Parameters:
        access_token (str): The new access token.
        instance_url (str): The Salesforce instance URL.
        issued_at (str): The timestamp indicating when the token was issued.
    """
    global _cached_token, _token_expiry, _instance_url
    token_lifetime = int(
        os.getenv("SF_TOKEN_LIFETIME", "3600")
    )  # Default to 1 hour if not set

    _cached_token = access_token
    _instance_url = instance_url
    issued_at_datetime = datetime.fromtimestamp(int(issued_at) / 1000)
    _token_expiry = issued_at_datetime + timedelta(seconds=token_lifetime)
