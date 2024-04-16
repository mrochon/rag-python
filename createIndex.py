import sys
import os
import dotenv
import requests
import json

dotenv.load_dotenv()

INDEXER_NAME=os.environ.get("INDEXER_NAME")
TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")

token_params = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://search.azure.com/.default"
}
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" 
response = requests.post(url=TOKEN_URL, data=token_params, headers={"Content-Type": "application/x-www-form-urlencoded"})
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")
else:
    sys.exit(f"Error requesting token. Status code: {response.status_code}")
    
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

#headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}

def handleResponse(response):
    if response.status_code == 200 or response.status_code == 201:
        user_data = response.json()
        #print(user_data)
        print("Ok")
    else:
        sys.exit(f"Error fetching user data: {response.status_code} - {response.text}")
                 
def getPayload(objectName):
    file_path = os.path.join(os.getcwd(), f"debug/{objectName}.json")
    with open(file_path, "r") as file:
        payload= json.load(file)
    return payload

# Note: updating an index does not delete existing index data. Only way to delete the data is to delete the index
print("Creating index")
createIndex = getPayload('index')   
rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes?api-version=2024-03-01-preview"    
#print(json.dumps(createIndex, indent=2))
response = requests.post(url=rest_url, headers=headers, json=createIndex)
handleResponse(response)

print("Creating skillset")
createSkillset = getPayload('skillset')
rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/skillsets?api-version=2024-03-01-preview"    
response = requests.post(url=rest_url, headers=headers, json=createSkillset)
handleResponse(response)

print("Creating indexer")
indexer = getPayload('indexer')
rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexers?api-version=2024-03-01-preview"    
response = requests.post(url=rest_url, headers=headers, json=indexer)
handleResponse(response)



