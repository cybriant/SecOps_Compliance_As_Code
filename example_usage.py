from google.oauth2 import service_account
from googleapiclient import _auth
from google.auth.transport.requests import Request
import requests
import json

# Example usage of Google SecOps API creds


# Set appropriate scope for the API to be used
SCOPES = ["https://www.googleapis.com/auth/malachite-ingestion"]


# Prior to running the script, make sure to have the service account json file stored and accessible
# Service account file looks like this:
# {
#     "type": "service_account",
#     "project_id": "",
#     "private_key_id": "",
#     "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
#     "client_email": "",
#     "client_id": "",
#     "auth_uri": "",
#     "token_uri": "",
#     "auth_provider_x509_cert_url": "",
#     "client_x509_cert_url": "",
#     "universe_domain": ""
# }
SERVICE_ACCOUNT_FILE = ".\\demo_cybriant_ingestion_api_creds.json"


# Create a credential using Google Developer Service Account Credential and Chronicle API Scope.
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)


# Build an HTTP client to make authorized OAuth requests.
http_client = _auth.authorized_http(credentials)


# Test authentication is successful
def test_authentication():
    try:
        # Fetch the token w object request
        request = Request()

        # Try to refresh creds w new token if the current one is expired
        credentials.refresh(request)

        # If there is no exception we have successfully authenticated with new token.
        print("Access Token obtained, auth successful.")
    except Exception as s:
        # If there was an error authenticating, let user know
        print(f"Authentication Failed: {s}")


test_authentication()