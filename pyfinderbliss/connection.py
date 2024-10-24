import requests
from .const import NEGOTIATE_URL

def negotiate_connection(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Length': '0',
        'User-Agent': 'Microsoft.AspNetCore.Http.Connections.Client/1.1.0-rtm-35687',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.post(NEGOTIATE_URL, headers=headers)
        response.raise_for_status()
        negotiate_data = response.json()
        connection_id = negotiate_data.get("connectionId")
        if connection_id:
            return connection_id
        else:
            print("Negotiation failed. No connection ID returned.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to negotiate WebSocket connection: {e}")
        return None
