import sys
import os
import dotenv
import requests
import json

dotenv.load_dotenv('.env', verbose=True, override=True)


INDEXER_NAME=os.environ.get("INDEXER_NAME")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY = os.environ.get("SEARCH_API_KEY")
API_VERSION=os.environ["API_VERSION"]

if TENANT_ID and CLIENT_ID and CLIENT_SECRET:
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
else:
    headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}

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
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
        print("Ok")
    else:
        sys.exit(f"Error calling Azure Search API: {response.status_code} - {response.text}")

def createObject(objectType, objectName):
    print(f"Creating {objectType}")
    if objectType == "index":
        plural = "indexes"
    else:
        plural = f"{objectType}s"
    file_path = os.path.join(os.getcwd(), f"api-payload/{objectType}.json")
    with open(file_path, "r") as file:
        payload= file.read()
    #print(json.dumps(createIndex, indent=2))
    for key, value in variables:
        payload = payload.replace(key, value)  
    # preview API supports vectorization
    rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/{plural}('{objectName}')?allowIndexDowntime=True&api-version={API_VERSION}"   
    response = requests.put(url=rest_url, headers=headers, json=json.loads(payload))
    handleResponse(response)    

# Note: updating an index does not delete existing index data. Only way to delete the data is to delete the index

createObject('datasource', os.environ["DATA_SOURCE_NAME"])  
createObject('synonymmap', os.environ["SYNONYM_MAP_NAME"])  
createObject('index', os.environ["INDEX_NAME"])   
createObject('skillset', os.environ["SKILLSET_NAME"])
createObject('indexer', os.environ["INDEXER_NAME"])

# For indexer schedule use ISO 8601 Durations, e.g. PT1H for 1 hour
# https://en.wikipedia.org/wiki/ISO_8601#Durations




