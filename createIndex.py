import sys
import os
import dotenv
import requests
import json

generate_only = True

def handleResponse(response):
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
        print("Ok")
    else:
        sys.exit(f"Error calling Azure Search API: {response.status_code} - {response.text}")

def createObject(objectType, objectName):
    print(f"Generating {objectType}")
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
    with open(f"tmp/{objectType}.json", "w") as file:
        file.write(json.dumps(json.loads(payload), indent=2))
    if not generate_only:
        rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/{plural}('{objectName}')?allowIndexDowntime=True&api-version={API_VERSION}"   
        response = requests.put(url=rest_url, headers=headers, json=json.loads(payload))
        handleResponse(response)    

if generate_only:
    print("Generate only, no objects will be created")
else:
    print("Creating objects")
    
dotenv.load_dotenv('.env', verbose=True, override=True)

SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY = os.environ.get("SEARCH_API_KEY", None)
API_VERSION=os.environ.get("SEARCH_API_VERSION", "2024-07-01")

if not generate_only:
    if SEARCH_API_KEY:
        headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}        
    else:
        # Search Service Contributor role is required
        from azure.identity import DefaultAzureCredential
        token_provider = DefaultAzureCredential(exclude_interactive_browser_credential=True).get_token("https://search.azure.com/.default") 
        token = token_provider.token  
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

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

# Note: updating an index does not delete existing index data. Only way to delete the data is to delete the index

createObject('datasource', os.environ["DATA_SOURCE_NAME"])  
# createObject('synonymmap', os.environ["SYNONYM_MAP_NAME"])  
createObject('index', os.environ["INDEX_NAME"])   
createObject('skillset', os.environ["SKILLSET_NAME"])
createObject('indexer', os.environ["INDEXER_NAME"])

# For indexer schedule use ISO 8601 Durations, e.g. PT1H for 1 hour
# https://en.wikipedia.org/wiki/ISO_8601#Durations




