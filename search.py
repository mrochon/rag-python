import sys
import os
import dotenv
import requests
import json
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

dotenv.load_dotenv('.env', verbose=True, override=True)

from common.customAzureSearch import CustomAzureSearchRetriever
from azure.identity import DefaultAzureCredential

cred = DefaultAzureCredential()
retriever = CustomAzureSearchRetriever(indexes=[os.environ['INDEX_NAME']], credential=cred, topK=5, reranker_threshold=1)
chain = (
    {
        "context": itemgetter("question") | retriever, # Passes the question to the retriever and the results are assign to context
        "question": itemgetter("question")
    }
    | StrOutputParser() 
)
chain.invoke({"question": "Which fillaments does Longer recommend?"})
# for chunk in chain.stream({"question": "What is the population of Denmark?"}):
#     print(chunk, end="", flush=True)