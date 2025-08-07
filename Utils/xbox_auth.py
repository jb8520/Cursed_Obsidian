import json
import os

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.api.client import XboxLiveClient


def save_tokens(manager):
    with open("tokens.json", "w") as f:
        json.dump(manager.oauth, f, indent=4)
    print("Tokens saved to tokens.json")

def main():
    client_id = os.getenv("XBOX_CLIENT_ID") or input("Enter your Client ID: ")
    redirect_uri = os.getenv("XBOX_REDIRECT_URI") or input("Enter your Redirect URI (e.g. https://localhost): ")

    manager = AuthenticationManager(client_id, redirect_uri)

    auth_url = manager.get_authorization_url()
    print("Go to the following URL and sign in:")
    print(auth_url)

    auth_code = input("Paste the URL you were redirected to here:\n")

    manager.request_tokens(auth_code)
    save_tokens(manager)

    # Test the token
    client = XboxLiveClient(manager)
    profile = client.profile.get_profile()
    print(f"Logged in as: {profile.profile_users[0].settings[0].value}")

if __name__ == "__main__":
    main()
