import os
import dotenv
import uuid
import requests
import tiktoken
import json

dotenv.load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings

SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")
INDEX_NAME=os.environ.get("INDEX_NAME")

rest_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes('{INDEX_NAME}')/docs/search.index?api-version=2023-11-01"

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION", "2021-08-04"),
    azure_endpoint = os.environ.get("OPENAI_ENDPOINT"),
    api_key= os.environ.get("OPENAI_API_KEY")
)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

dir = os.path.join(os.getcwd(), "data")
files = os.listdir(dir)
txt_files = [file for file in files if file.lower().endswith(".txt")]
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
docCount = 0
chunkCount = 0
for file in txt_files:
    documentsToLoad = list()
    with open(f"{dir}/{file}", encoding='utf-8') as f:
        inputDoc = f.read()
        chunks = text_splitter.create_documents([inputDoc])
        chunkVectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
        chunkNo = 0
        for chunk in chunks:
            outDoc = {
                "@search.action": "upload",
                "id": str(uuid.uuid4()),
                "uri": f"{dir}/{file}",
                "chunkNo": str(chunkNo),
                "content": chunk.page_content,
                "contentEmbedding": chunkVectors[chunkNo],
            }
            tokens = num_tokens_from_string(chunk.page_content, "gpt-3.5-turbo")
            print(f"{dir}/{file}-{chunkNo} - {len(chunk.page_content)} - {tokens}")
            documentsToLoad.append(outDoc)
            chunkNo += 1
        headers = {"api-key": SEARCH_API_KEY, "Content-Type": "application/json"}
        payload = { "value": documentsToLoad }
        #print(json.dumps(payload))
        response = requests.post(url=rest_url, headers=headers, json=payload)
        if response.status_code == 200:
            user_data = response.json()
            for resp in user_data["value"]:
                print(f"{resp["key"]} - {resp["statusCode"]} - {resp["status"]}")
            docCount += 1
            chunkCount += chunkNo
        else:
            print(f"Error loading data: {response.status_code} - {response.text}")
print(f"Documents: {docCount} - Chunks: {chunkCount}")

        




    
    