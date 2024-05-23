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
from pydantic import BaseModel, PositiveInt

class QueryConfig(BaseModel):
    index: str
    selectFields: List[str] = None
    searchFields: List[str] = None
    filter: str = None
    queryType: str = "semantic"
    vectorFieldName: str = None
    semanticConfigurationName: str = None
    topK: PositiveInt = 5
    reranker_threshold: int = 1

def get_search_results(query: str, configs: List[QueryConfig], token: str,
                       k: int = 5,
                       reranker_threshold: int = 1) -> List[dict]:
    """Performs multi-index hybrid search and returns ordered dictionary with the combined results"""
    
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {token}"}
    params = {'api-version': "2024-03-01-preview"}

    configIx = 0
    agg_search_results = dict()
    for config in configs:
        search_payload = {
            "search": query,
            "select": ",".join(config.selectFields) if config.selectFields else None,
            "searchFields": ",".join(config.searchFields) if config.searchFields else None,
            "filter": config.filter,
            "queryType": config.queryType,
            "semanticConfiguration": config.semanticConfigurationName,
            "captions": "extractive",
            "answers": "extractive|count-3",
            "count":"true",
            "top": k    
        }
        if config.vectorFieldName:
            search_payload["vectorQueries"] = [{"text": query, "fields": config.vectorFieldName, "kind": "text", "k": k}]
        resp = requests.post(f"https://{os.environ['SEARCH_SERVICE_NAME']}.search.windows.net/indexes/{config.index}/docs/search",
                         data=json.dumps(search_payload), headers=headers, params=params)
        if resp.status_code != 200:
            raise Exception(f"Search request failed with status code {json.loads(resp.text)['error']['message']}")
        search_results = resp.json()
        agg_search_results[configIx] = search_results
        configIx += 1

    content = dict()
    ordered_content = OrderedDict()
    id = 0
    for configIx,search_results in agg_search_results.items():
        for result in search_results['value']:
            if result['@search.rerankerScore'] > reranker_threshold: # Show results that are at least N% of the max possible score=4
                content[id]={
                                "caption": result['@search.captions'][0]['text'],
                                "score": result['@search.rerankerScore'],
                                "index": configs[configIx].index,
                            }
                for field in configs[configIx].selectFields:
                    content[id][field] = result[field]
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
    
    configs: List[QueryConfig]
    credential : DefaultAzureCredential
    
    
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        
        token_resp = self.credential.get_token("https://search.azure.com/.default")
        ordered_results = get_search_results(query, self.configs, token_resp.token)
        
        top_docs = []
        for key,value in ordered_results.items():
            location = value["uri"] if value["uri"] is not None else ""
            top_docs.append(Document(page_content=value["chunk"], metadata={"source": location, "score":value["score"]}))

        return top_docs