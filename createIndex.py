import os
import dotenv
import requests
import json

dotenv.load_dotenv()

INDEX_NAME=os.environ.get("INDEX_NAME")
TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" 
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")
rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes?api-version=2023-11-01"

file_path = os.path.join(os.getcwd(), "data/createIndex.json")
with open(file_path, "r") as file:
    createIndex= json.load(file)
    createIndex["name"] = INDEX_NAME

# from requests_oauthlib import OAuth2Session
# oauth_session = OAuth2Session(client_id=CLIENT_ID)
# token = oauth_session.fetch_token(grant_type="client_credentials", client_secret=CLIENT_SECRET, token_url=TOKEN_URL, authorization_response=)

# request = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&scope=https://cognitiveservices.azure.com/.default"
# tokens = requests.post(url=TOKEN_URL, data=request, headers={"Content-Type": "application/x-www-form-urlencoded"})
# token = tokens.json().get("access_token")
# headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}

response = requests.post(url=rest_url, headers=headers, json=createIndex)

if response.status_code == 201:
    user_data = response.json()
    print(user_data)
else:
    print(f"Error fetching user data: {response.status_code} - {response.text}")

