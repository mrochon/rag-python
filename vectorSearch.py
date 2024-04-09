import os
import dotenv
import uuid
import requests
import json

from langchain_openai import AzureOpenAIEmbeddings

dotenv.load_dotenv()

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION", "2021-08-04"),
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_API_KEY")
)

SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")
INDEX_NAME=os.environ.get("INDEX_NAME")
rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes('{INDEX_NAME}')/docs/search.post.search?api-version=2023-11-01"
headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}

#question = input("Q: ")
question = "Who is Robin Skynner?"

questionVector = embeddings.embed_query(question)
query = {
    "search": question,
    "count": True,
    "queryType": "semantic",
    "search": str(uuid.uuid4()),
    "searchFields": "content",
    "searchMode": "any",
    "sessionId": "1",
    "select": "id,uri,chunkNo,content",
    "skip": 0,
    "top": 3,
    "vectorQueries": [
        {
            "kind": "vector",
            "vector": questionVector,
            "fields": "contentEmbedding",
            "k": 5,
            "exhaustive": True
        }
    ],
    "vectorFilterMode": "preFilter",
    "semanticConfiguration": "semanticDocs"
}

response = requests.post(url=rest_url, headers=headers, json=query)
if response.status_code == 200:
    search_data = response.json()
    for resp in search_data["value"]:
        print(json.dumps(resp, indent=2))
else:
    print(f"Error loading data: {response.status_code} - {response.text}")

