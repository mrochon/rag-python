import sys
import os
import dotenv
import requests
import json

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from IPython.display import display, HTML, Markdown

dotenv.load_dotenv()

OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
GTP_DEPLOYMENT = os.environ.get("GTP_DEPLOYMENT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INDEX_NAME=os.environ.get("INDEX_NAME")
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")

agg_search_results = dict()
k = 1
QUESTION = "Which filaments does Longer recommend?"
search_payload = {
    "search": QUESTION, # Text query
    "select": "uri, chunk",
    "queryType": "semantic",
    "vectorQueries": [{"text": QUESTION, "fields": "chunkVector", "kind": "text", "k": k}], # Vector query
    "semanticConfiguration": "manuals-semantic-configuration",
    "captions": "extractive",
    "answers": "extractive",
    "count":"true",
    "top": k
}
headers = {"api-key": os.environ['QUERY_KEY'], "Content-Type": "application/json"}
params = {'api-version': "2024-03-01-Preview"}
r = requests.post(f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{INDEX_NAME}/docs/search",
                    data=json.dumps(search_payload), headers=headers, params=params)
if not r.ok:
    sys.exit(f"Error calling Azure Search API: {r.status_code} - {r.text}")
search_results = r.json()
print("Index:", INDEX_NAME, "Results Found: {}, Results Returned: {}".format(search_results['@odata.count'], len(search_results['value'])))
filtered_results = [result for result in search_results['value'] if result['@search.rerankerScore'] > 2.0]
if len(filtered_results) == 0:
    sys.exit("No data")
# for doc in filtered_results:
#     print(doc['uri'], doc['chunk'])

COMPLETION_TOKENS = 4000
llm = AzureChatOpenAI(deployment_name=os.environ["GTP_DEPLOYMENT"], 
                      azure_endpoint = OPENAI_ENDPOINT,
                      temperature=0.8,
                      max_tokens=COMPLETION_TOKENS)
#template = """Answer the question thoroughly, based **ONLY** on the following context:
template = """Answer questions about Longer 3D printers using the following context:
{context}

If the context is not enough, you can ask for more information.

Question: {question}
"""
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm | output_parser
#filtered_results = "Longer recommends using its own filaments to prevent damage to nozzles and ensure the best print quality. Longer filaments are available in a variety of colors and materials, including PLA, ABS, and PETG. Longer also offers a range of specialty filaments, such as wood, metal, and flexible filaments. Longer filaments are designed to work seamlessly with Longer 3D printers, ensuring optimal performance and reliability. Longer filaments are available in both 1.75mm and 2.85mm diameters, making them compatible with a wide range of 3D printers on the market."
try:
    answer = chain.invoke({"question": QUESTION, "context": filtered_results})
    print(answer)
except Exception as e:
    sys.exit(f"Error calling Azure OpenAI API: {e}")




