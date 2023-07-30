import requests
import json
import msal

# Load the configuration
config = {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "authority": "https://login.microsoftonline.com/your_tenant_id",
    "username": "your_username",
    "scope": ["https://graph.microsoft.com/.default"],
}

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"], client_credential=config["client_secret"]
)

# The pattern to acquire a token looks like this.
result = None

# First, the code looks up a token from the cache.
# Because we're looking for a token for the current user (not a client), not specifying a user here.
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    # If a token can't be found in the cache, the code invokes the "acquire_token_for_client" method
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    # Call a protected API with the access token
    headers = {
        'Authorization' : 'Bearer ' + result['access_token']
    }
    api_url = 'https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages'
    response = requests.get(url=api_url, headers=headers)
    if response.status_code == 200:
        email_data = json.loads(response.text)
        last_email = email_data['value'][0]
        print("Subject: ", last_email['subject'])
        print("Body: ", last_email['bodyPreview'])
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug
