import argparse
from .auth import login
from .api import negotiate_connection, open_websocket

def get_arguments():
    """Get parsed arguments from the command line."""
    parser = argparse.ArgumentParser(description="pyFinderBliss: Command Line Utility")
    parser.add_argument("-u", "--user", required=True, help="User for Finder BLISS account")
    parser.add_argument("-p", "--password", required=True, help="Password for Finder BLISS account")
    return vars(parser.parse_args())

def main():
    """Main entry point for the CLI."""
    args = get_arguments()

    user = args.get('user')
    password = args.get('password')

    # Perform login to get access token
    access_token = login(user, password)
    if access_token:
        print("Login successful!")
        print(f"Access Token: {access_token}")
        # Negotiate connection using the access token
        connection_id = negotiate_connection(access_token)
        if connection_id:
            print("Connection ID obtained:", connection_id)
             # Open WebSocket connection to fetch data
            server_payload = open_websocket(access_token, connection_id)
            
        else:
            print("Failed to obtain connection ID.")
    else:
        print("Login failed. Check your credentials.")

if __name__ == "__main__":
    main()
