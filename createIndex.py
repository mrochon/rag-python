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

variables = list()
file_path = os.path.join(os.getcwd(), ".env")
with open(file_path, "r") as file:
    for line in file:
        splitIndex = line.find("=")
        key = line[:splitIndex]
        value = line[splitIndex+1:]
        value = value.strip("\n\"")
        #key, value = line.strip().split("=")
        variables.append((key, value))

def handleResponse(response):
    if response.status_code == 200 or response.status_code == 201:
        user_data = response.json()
        #print(user_data)
        print("Ok")
    else:
        sys.exit(f"Error fetching user data: {response.status_code} - {response.text}")
                 
def createObject(objectName):
    print(f"Creating {objectName}")
    if objectName == "index":
        plural = "indexes"
    else:
        plural = f"{objectName}s"
    file_path = os.path.join(os.getcwd(), f"api-payload/{objectName}.json")
    with open(file_path, "r") as file:
        payload= file.read()
    #print(json.dumps(createIndex, indent=2))
    for key, value in variables:
        payload = payload.replace(key, value)   
    rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/{plural}?api-version=2024-03-01-preview"   
    response = requests.post(url=rest_url, headers=headers, json=json.loads(payload))
    handleResponse(response)    

# Note: updating an index does not delete existing index data. Only way to delete the data is to delete the index

createObject('index')   
createObject('skillset')
createObject('indexer')




