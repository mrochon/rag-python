# Document indexing

## Purpose

Create and populate Azure Search index with data from pdf files stored in blob storage. Provide simple chat interface to conduct q&a with OpenAI and Search to get answers to questions related to the stored documents.

## Operation

See [VSCode environment setup documentation](https://code.visualstudio.com/docs/python/environments) to prepare your propject.

1. Create a datasource in Azure Search to read your pdfs from a blob container
2. Register a confidential client app in Entra ID and give it Search Index Contributor permission
2. Setup your py environment with this repo, see [VSCode environment setup documentation](https://code.visualstudio.com/docs/python/environments).
4. Update *.env* file (see below) with your own settings
2. Execute createIndex.py to create an index, skillset and indexer
3. Run chatCompletions.py to enter questions and received answers from OpenAI
6. Use Azure portal Azure Search Index view to execute queries

The skillset chunks the pdf docs into pages, hides some PII data, vectorizes the text content and uploads chunk to secondary index (document goes to primary).

## Environment Setup

### Portal

Grant Search Service Contributor to a Service Principal and allow index to use RBAc for authorization (key is default).
Enable Semantic Ranker plan on the index.

### Variables

Following environment variables need to be created in the .env file:

```
DATA_SOURCE_NAME="<anem of an existing Azure Search Data Source>"
INDEX_NAME=<name of Azure Search Index>
INDEXER_NAME="<name of an indexer to create>"
SKILLSET_NAME="<name of a skillset to create>"
SEARCH_SERVICE_NAME="<name of Azure Search Service>"
OPENAI_ENDPOINT=https://<your ep>.openai.azure.com/
GTP_DEPLOYMENT="gtp-35-turbo-16k"
EMBEDDINGS_MODEL=<embedding deployment name>
OPENAI_API_KEY=...
SEARCH_API_KEY="<Search API key>"
AI_SERVICE_KEY="<API key for Azure Cognitive Service>"
TENANT_ID="<Entra tenant id>"
CLIENT_ID="<Confidential client id>"
CLIENT_SECRET="<Confidential client secret>"
```

### PIP Installs

See *requirements.txt*

```
pip install -r requirmeents.txt
```

### Terminal env

```python -m venv .venv```

### Install Tesseract for Confluence documenting reading**

If planning to read Confluence data:
[Error explanation](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i) and [this](https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror)

[Install .exe for Confluence data reading](https://github.com/UB-Mannheim/tesseract/wiki)
*Make sure to add this to PATH env variable*
```
C:\Users\mrochon\AppData\Local\Programs\Tesseract-OCR
```

```
pip install pytesseract Pillow
pip install pytesseract
```

## Code examples

| Source | Comments |
| --- | --- |
| [createIndex.py](https://github.com/mrochon/python/blob/main/createIndex.py) | Create new datasource, index, skillset and indexer | 
| [chatCompletions.py](https://github.com/mrochon/python/blob/main/chatCompletions.py) | Simple REST based chat completion | 
| [chatCompletionsStream.py](https://github.com/mrochon/python/blob/main/chatCompletionsStream.py) | REST based chat completion with response streaming | 
| ---other--- |  | 
| [confluenceDocReader.py](https://github.com/mrochon/python/blob/main/confluenceDocReader.py) | Reads data from Confluence |
| [chunkRecursive.py](https://github.com/mrochon/python/blob/main/chunkRecursive.py) | Break text into chunks using recursive chunking |
| [chunkText.py](https://github.com/mrochon/python/blob/main/chunkText.py) | Break text into chunks ([using semantic chunking](https://python.langchain.com/docs/modules/data_connection/document_transformers/semantic-chunker/)) |
| [vectorize.py](https://github.com/mrochon/python/blob/main/vectorize.py) | Create embedding vectors from text |
| [createIndex.py](https://github.com/mrochon/python/blob/main/createIndex.py) | Create Azure Search index [using REST call](https://learn.microsoft.com/en-us/rest/api/searchservice/indexes/create?view=rest-searchservice-2023-11-01&tabs=HTTP)|
| [loadSampleDocs.py](https://github.com/mrochon/python/blob/main/loadSampleDocs.py) | Load some docs to Azure Index (chunk, vectorize, upload) [using REST call](hhttps://learn.microsoft.com/en-us/rest/api/searchservice/documents/?view=rest-searchservice-2023-11-01&tabs=HTTP)|



## References:

1. [Krystian Safjan's Chunking strategies](https://safjan.com/from-fixed-size-to-nlp-chunking-a-deep-dive-into-text-chunking-techniques/#google_vignette)
2. [Carlo C. Chunking strategies](https://medium.com/aimonks/chunking-strategies-for-more-effective-rag-through-llm-63ae7b046b46)
3. [OpenAI REST API](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/stable/2024-02-01/inference.json)
4. [Py app sample](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/app/backend/app.py)

## Environment

Use local python environment (@command:python.createEnvironment).

Could be done as [Git Codespace except](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces) Tesserac requires own .exe, would need a new image.

```
py -m venv C:\Users\mrochon\source\repos\python 
```

## questionss

1. Optimal maximumPageLength?
2. Handling search references in completion response