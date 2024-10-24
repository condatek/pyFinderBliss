import requests
from .const import BASE_URL, LOGIN_ENDPOINT, CLIENT_ID, SCOPE, GRANT_TYPE

def login(user, password):
    """Authenticate with the Finder BLISS API and retrieve access tokens."""
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    payload = {
        'client_id': CLIENT_ID,
        'grant_type': GRANT_TYPE,
        'scope': SCOPE,
        'username': user,
        'password': password,
    }

    try:
        response = requests.post(login_url, data=payload)
        response.raise_for_status()  # Raise an error for bad responses
        token = response.json().get('access_token')
        return token
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return None
