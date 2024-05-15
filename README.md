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
## Vision sample

visionCaption.py uses Azure Vision 4.0 REST API to create captions for objects found in a picture. It then sorts these captions by 'significance' - size of the object multiplied by recognition confidence + 1 (arbitrary way of increasing significance of confidence level). Below is the list it produced.

Some comments:

1. Brand extraction seems not supported in 4.0, requires 3.2 and does not seem very reliable.
2. Possible to train model with own brands
3. Do not use blob urls with SAS - you will get a misleading error message (wrong API key or API version)
4. There are two Vision services exposed in the market place: Custom Vision and Azure Vision. The former allows model training. Same API.

```
[Image 1](https://i.etsystatic.com/51286668/r/il/27eaed/6014488641/il_1588xN.6014488641_bybu.jpg)
3540664.4424562454 a white t-shirt with a logo on it
3323911.0958576202 a white shirt with a logo on it
1638713.3676481247 a white t-shirt with a logo on it
84935.92342960835 a close up of a logo
52640.99776518345 a wooden object with a black background
47312.44461965561 a close-up of a sign
22299.354930639267 a close up of a sign
21066.452381253242 a close up of a colorful square
9098.866596221924 a blue square with black lines
8100.673599243164 a close up of an orange square

[Image 2]:(https://mobileimages.lowes.com/productimages/cf75cdca-e41f-42f6-857f-aa49a5b10675/12161585.jpg)
1749111.6523742676 a can of paint with a white label
1163405.9780507088 a can of paint with a label
158812.61454582214 a close-up of a silver plate
81225.97669053078 a close up of a logo
65803.13216209412 a close up of a sign
46963.74707400799 a blue letter on a white surface
34378.030671179295 a blue shield with white text
32410.553058743477 a close up of a label
10311.295795440674 a blue sign with white letters
8493.588054478168 a letter on a white surface

[Image 3](https://cdnimg.webstaurantstore.com/images/products/large/758110/2572441.jpg)
656463.189125061 a screwdriver with yellow handle
507116.565787375 a screwdriver with a yellow handle

[Image 4](https://cdnimg.webstaurantstore.com/images/products/large/568760/2638325.jpg)
621655.7550430298 a blue machine with a fan
518628.0614397526 a blue fan with a black circle
99585.67106813192 a blue box with metal grate
93088.14066690207 a close-up of a vent
```

## questionss

1. Optimal maximumPageLength?
2. Handling search references in completion response