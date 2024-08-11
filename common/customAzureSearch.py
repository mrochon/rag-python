import os
import json
import requests
from io import BytesIO
from typing import Any, Dict, List, Optional, Awaitable, Callable, Tuple, Type, Union
from collections import OrderedDict
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from operator import itemgetter
from typing import List
from azure.identity import DefaultAzureCredential

def get_search_results(query: str, indexes: list, token: str,
                       k: int = 5,
                       reranker_threshold: int = 1) -> List[dict]:
    """Performs multi-index hybrid search and returns ordered dictionary with the combined results"""
    
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {token}"}
    params = {'api-version': "2024-03-01-preview"}

    agg_search_results = dict()
    
    for index in indexes:
        search_payload = {
            "search": query,
            "select": "uri, chunk",
            "queryType": "semantic",
            "vectorQueries": [{"text": query, "fields": "chunkVector", "kind": "text", "k": k}],
            "semanticConfiguration": "semantic-configuration",
            "captions": "extractive",
            "answers": "extractive|count-3",
            "count":"true",
            "top": k    
        }

        resp = requests.post(f"https://{os.environ['SEARCH_SERVICE_NAME']}.search.windows.net/indexes/{index}/docs/search",
                         data=json.dumps(search_payload), headers=headers, params=params)

        search_results = resp.json()
        agg_search_results[index] = search_results
    
    content = dict()
    ordered_content = OrderedDict()
    
    id = 0
    for index,search_results in agg_search_results.items():
        for result in search_results['value']:
            if result['@search.rerankerScore'] > reranker_threshold: # Show results that are at least N% of the max possible score=4
                content[id]={
                                "uri": result['uri'], 
                                "chunk": result['chunk'],
                                "caption": result['@search.captions'][0]['text'],
                                "score": result['@search.rerankerScore'],
                                "index": index
                            }
                id += 1
                

    topk = k
        
    count = 0  # To keep track of the number of results added
    for id in sorted(content, key=lambda x: content[x]["score"], reverse=True):
        ordered_content[id] = content[id]
        count += 1
        if count >= topk:  # Stop after adding topK results
            break

    return ordered_content

class CustomAzureSearchRetriever(BaseRetriever):
    
    indexes: List
    topK : int
    reranker_threshold : int
    credential : DefaultAzureCredential
    
    
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        
        token_resp = self.credential.get_token("https://search.azure.com/.default")
        ordered_results = get_search_results(query, self.indexes, token_resp.token, k=self.topK, reranker_threshold=self.reranker_threshold, )
        
        top_docs = []
        for key,value in ordered_results.items():
            location = value["uri"] if value["uri"] is not None else ""
            top_docs.append(Document(page_content=value["chunk"], metadata={"source": location, "score":value["score"]}))

        return top_docs