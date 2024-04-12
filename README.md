# Document indexing
Use local python environment (@command:python.createEnvironment).

Could be done as [Git Codespace except](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces) Tesserac requires own .exe, would need a new image.

## Environment Setup

### Variables

Exaple:

```
INDEX_NAME=<name of Azure Search Index>
OPENAI_API_VERSION="2023-05-15"
OPENAI_ENDPOINT=https://<your ep>.openai.azure.com/
GTP_DEPLOYMENT="gtp-35-turbo-16k"
OPENAI_API_KEY=...
EMBEDDINGS_MODEL=<embedding deployment name>
CONF_USER_NAME="<Confluence user name>"
CONF_API_KEY=<pwd>>
TENANT_ID="<Entra tenant id>"
CLIENT_ID="<Confidential client id>"
CLIENT_SECRET="<Confidential client secret>"
SEARCH_SERVICE_NAME="<Search service name>"
SEARCH_API_KEY="<Search API key>"
```
### PIP Installs

```
pip install python-dotenv
pip install openai
pip install langchain
pip install langchain-openai
pip install atlassian-python-api
pip install uuid
```

**Install Tesseract for Confluence documenting reading**

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

Is this needed?
pip install num2words matplotlib plotly scipy scikit-learn pandas tiktoken

```
pip install python-dotenv
pip install lxml
```

For REST and OAuth2
```
pip install request
pip install requests_oauthlib
```

For text chunking
```
pip install langchain_experimental
pip install langchain-text-splitters
```

## Entra Id

1. Register an application to work with Search: apId and secret
2. In Search, use IAM to assign Index Contributor role to the above application

## Code examples

| Source | Comments |
| --- | --- |
| [readDocs.py](https://github.com/mrochon/python/blob/main/readDocs.py) | Reads data from Confluence |
| [chunkText.py](https://github.com/mrochon/python/blob/main/chunkText.py) | Break text into chunks ([using semantic chunking](https://python.langchain.com/docs/modules/data_connection/document_transformers/semantic-chunker/)) |
| [vectorize.py](https://github.com/mrochon/python/blob/main/vectorize.py) | Create embedding vectors from text |
| [createIndex.py](https://github.com/mrochon/python/blob/main/createIndex.py) | Create Azure Search index [using REST call](https://learn.microsoft.com/en-us/rest/api/searchservice/indexes/create?view=rest-searchservice-2023-11-01&tabs=HTTP)|
| [loadSampleDocs.py](https://github.com/mrochon/python/blob/main/loadSampleDocs.py) | Load some docs to Azure Index (chunk, vectorize, upload) [using REST call](hhttps://learn.microsoft.com/en-us/rest/api/searchservice/documents/?view=rest-searchservice-2023-11-01&tabs=HTTP)|
| [chatCompletion.py](https://github.com/mrochon/python/blob/main/chatCompletion.py) | Simple REST based chat completion | 


## References:

1. [Krystian Safjan's Chunking strategies](https://safjan.com/from-fixed-size-to-nlp-chunking-a-deep-dive-into-text-chunking-techniques/#google_vignette)
2. [Carlo C. Chunking strategies](https://medium.com/aimonks/chunking-strategies-for-more-effective-rag-through-llm-63ae7b046b46)
3. [OpenAI REST API](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/stable/2024-02-01/inference.json)