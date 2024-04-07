# My Py environment
Based on [https://docs.github.com/en/codespaces/...](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces)

## Setup
pip install python-dotenv
pip install openai
pip install langchain
pip install langchain-openai
pip install atlassian-python-api

https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror

https://github.com/UB-Mannheim/tesseract/wiki
C:\Users\mrochon\AppData\Local\Programs\Tesseract-OCR

pip install pytesseract Pillow
pip install pytesseract
Add tessarc PATh to PATH env variable

pip install num2words matplotlib plotly scipy scikit-learn pandas tiktoken

pip install python-dotenv
pip install lxml

## Index upload

### Create

https://learn.microsoft.com/en-us/rest/api/searchservice/indexes/create?view=rest-searchservice-2023-11-01&tabs=HTTP

### Upload

See https://learn.microsoft.com/en-us/rest/api/searchservice/documents/?view=rest-searchservice-2023-11-01&tabs=HTTP

## Curl

use curl --netrc-file .netrc http://example.com to keep secrets, .netrc format:

machine example.com
login daniel
password qwerty

curl -i -X POST host:port/post-file \
  -H "Content-Type: text/xml" \
  --data-binary "@path/to/file"
