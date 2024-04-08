# Document indexing
Use local python environment (@command:python.createEnvironment).

Could be done as [Git Codespace except](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces) Tesserac requires own .exe, would need a new image.

## Environment Setup

```
pip install python-dotenv
pip install openai
pip install langchain
pip install langchain-openai
pip install atlassian-python-api
pip install uuid
```

Install Tesseract:

[Error explanation](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i)
and [this](https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror)

[Install app](https://github.com/UB-Mannheim/tesseract/wiki)
Make sure to add this to PATH env variable
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
| tbd | Upload documents to [Azure Search using REST](https://learn.microsoft.com/en-us/rest/api/searchservice/documents/?view=rest-searchservice-2023-11-01&tabs=HTTP) | 

