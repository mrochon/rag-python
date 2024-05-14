import os
import dotenv
import requests
import json

dotenv.load_dotenv('.env', verbose=True, override=True)

SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY = os.environ.get("SEARCH_API_KEY")
INDEX_NAME = os.environ["INDEX_NAME"]

headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}

text = "This pipe is 10 in. long and 2"" in diameter. It is made of steel and is painted black."

text_params = {
        "text": text,
        "analyzer": "standard.lucene",
}
url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{INDEX_NAME}/analyze?api-version=2023-11-01" 

response = requests.post(url=url, json=text_params, headers={"Content-Type": "application/json", "api-key": SEARCH_API_KEY})
print(json.dumps(response.text, indent=2))
