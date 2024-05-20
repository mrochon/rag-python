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
    params = {'api-version': os.environ['SEARCH_API_VERSION']}

    agg_search_results = dict()
    
    for index in indexes:
        search_payload = {
            "search": query,
            "select": "id, title, chunk, name, location",
            "queryType": "semantic",
            "vectorQueries": [{"text": query, "fields": "chunkVector", "kind": "text", "k": k}],
            "semanticConfiguration": "my-semantic-config",
            "captions": "extractive",
            "answers": "extractive",
            "count":"true",
            "top": k    
        }

        resp = requests.post(f"https://{os.environ['SEARCH_SERVICE_NAME']}.search.windows.net/indexes/{index}/docs/search",
                         data=json.dumps(search_payload), headers=headers, params=params)

        search_results = resp.json()
        agg_search_results[index] = search_results
    
    content = dict()
    ordered_content = OrderedDict()
    
    for index,search_results in agg_search_results.items():
        for result in search_results['value']:
            if result['@search.rerankerScore'] > reranker_threshold: # Show results that are at least N% of the max possible score=4
                content[result['id']]={
                                        "title": result['title'], 
                                        "name": result['name'], 
                                        "chunk": result['chunk'],
                                        "location": result['location'],
                                        "caption": result['@search.captions'][0]['text'],
                                        "score": result['@search.rerankerScore'],
                                        "index": index
                                    }
                

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
        #token_resp = {'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJodHRwczovL3NlYXJjaC5henVyZS5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9jMzY0NWUwOS1kNjAyLTRlMjUtOTUwYy01ODUwZTM4M2Q2ZjIvIiwiaWF0IjoxNzE2MTc0NzExLCJuYmYiOjE3MTYxNzQ3MTEsImV4cCI6MTcxNjE3ODYxMSwiYWlvIjoiRTJOZ1lQRFMzbnV3NjhjWDhRK3liVkl2ODE4dUF3QT0iLCJhcHBpZCI6IjlkOGYzZWFiLWFkMDUtNDg0ZC05Y2VjLWFhZDUyYTkzOTJkNCIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2MzNjQ1ZTA5LWQ2MDItNGUyNS05NTBjLTU4NTBlMzgzZDZmMi8iLCJpZHR5cCI6ImFwcCIsIm9pZCI6ImZlNzdjYzM1LTg4YjQtNGQ3ZS05YjNiLTI0ODIzZDIwNGEwNyIsInJoIjoiMC5BWDBBQ1Y1a3d3TFdKVTZWREZoUTQ0UFc4b0NqRFloZW1KaEJnYm5nV3h6Rk1WaWNBQUEuIiwic3ViIjoiZmU3N2NjMzUtODhiNC00ZDdlLTliM2ItMjQ4MjNkMjA0YTA3IiwidGlkIjoiYzM2NDVlMDktZDYwMi00ZTI1LTk1MGMtNTg1MGUzODNkNmYyIiwidXRpIjoiYVVMNjRaRWpSME9WMzc5M2M3MHlBQSIsInZlciI6IjEuMCJ9.Om2nxL6DyZW3czY-Yuk-kUcqrBVPFkdAnZv5sJeoEqVSPnP_hOawxrc9FPUKY98UjjLFmq2xO9gEoAfMgcnx0TRW-GEyj2QEGBxjYH0rr8vzZHNN2no3I027VpGYjIwO2AchHxl8f8lCQJc4yt3zaT97ynicSP2GcIyqHLihluV4S_EcOaYfpcvgQhQVlDNuLHlA9EGAOJpwFu5AmKknbGMHoEh-cvKF3xipn5zm8FxPx_AZNcSSVXQOb-ndDIbadOYwtiFzW_atRCUbJ-3yjxfCd08F1pwqKlwDVx01NLCylb5G8Lqam2FGQyjyMrjBuFUR6if3SZnU26l8DVI-jw'}
        ordered_results = get_search_results(query, self.indexes, token_resp.token, k=self.topK, reranker_threshold=self.reranker_threshold, )
        
        top_docs = []
        for key,value in ordered_results.items():
            location = value["location"] if value["location"] is not None else ""
            top_docs.append(Document(page_content=value["chunk"], metadata={"source": location, "score":value["score"]}))

        return top_docs