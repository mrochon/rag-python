import requests
import json
from typing import Any, Dict, Iterator, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk

class WithDataLLM(LLM):
    systemPrompt: str
    url = ''
    headers = {}
    dataSources = {}
    
    # 'WithDataLLM' object has no attribute '__fields_set__'
    #   File "C:\Users\mrochon\source\repos\python\common\custom.py", line 22, in __new__
    #     obj.openAIServiceName = kwargs["openAIServiceName"]
    #     ^^^^^^^^^^^^^^^^^^^^^
    #   File "C:\Users\mrochon\source\repos\python\chatCompletionsWithLChain.py", line 65, in <module>
    #     llm = WithDataLLM(
    #           ^^^^^^^^^^^^
    # AttributeError: 'WithDataLLM' object has no attribute '__fields_set__'
    # def __new__ (cls, *args: Any, **kwargs: Any) -> "WithDataLLM":
    #     obj = super().__new__(cls)
    #     obj.openAIServiceName = kwargs["openAIServiceName"]
    #     obj.deploymentName = kwargs["deploymentName"]
    #     obj.openAIServiceKey = kwargs["openAIServiceKey"]
    #     obj.searchServiceName = kwargs["searchServiceName"]
    #     obj.searchApiKey = kwargs["searchApiKey"]
    #     obj.indexName = kwargs["indexName"]
    #     obj.indexRoleDescription = kwargs["indexRoleDescription"]
    #     obj.systemPrompt = kwargs["systemPrompt"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        openAIServiceName = kwargs["openAIServiceName"]
        deploymentName = kwargs["deploymentName"]
        openAIServiceKey = kwargs["openAIServiceKey"]
        searchServiceName = kwargs["searchServiceName"]
        searchApiKey = kwargs["searchApiKey"]
        indexName = kwargs["indexName"]
        indexRoleDescription = kwargs["indexRoleDescription"]
        
        self.systemPrompt = kwargs["systemPrompt"]
        self.url = f"{openAIServiceName}/openai/deployments/{deploymentName}/chat/completions?api-version=2024-02-01"
        self.headers = {"api-key": openAIServiceKey, "Content-Type": "application/json"}
        self.dataSources =     {
            "type": "azure_search", 
            "parameters": {
                "authentication": {
                    "type": "api_key",
                    "key": searchApiKey
                },
                "endpoint": f"https://{searchServiceName}.search.windows.net",
                "index_name": indexName,
                "fields_mapping": {
                    "content_fields": [
                        "chunk"
                    ],
                    "title_field": None,
                    "url_field": "uri",
                    "filepath_field": "uri",
                    "vector_fields": [
                        "chunkVector"
                    ]
                },  
                "in_scope": False,
                "top_n_documents": 5,
                "query_type": "semantic",
                "semantic_configuration": "manuals-semantic-configuration",                      
                "role_information": indexRoleDescription,
                "filter": None,
                "strictness": 3
            }
        }        

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        # object has no field _history!
        # if self._history is None:
        #     self._history = []


        payload = {
            "temperature": 0.0,
            "top_p": 1.0,
            "stream": False,
            "stop": ["***"],
            "max_tokens": 4096,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "logit_bias": {},
            "messages": [
                {"role": "system", "content": self.systemPrompt }, # this should be donw in the constructor
                {"role": "user", "content": prompt}],
            "data_sources": [self.dataSources]
        }
        with open("./temp/llm_request.json","w") as f:
            f.write(json.dumps(payload, indent=2))
        response = requests.post(self.url, json=payload, headers=self.headers, verify=False)
        response.raise_for_status()
        user_data = response.json()
        with open("./temp/llm_response.json","w") as f:
            f.write(json.dumps(user_data, indent=2)) 
        # self._history.append({"role": "user", "content": prompt})               
        # self._history.append({"role": "assistant", "content": user_data["choices"][0]["message"]["content"]})     
        return user_data["choices"][0]["message"]["content"]
        # print("API Response:", response.json())
        #return response.json()['generated_text']  # get the response from the API

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": "WithDataLLM",
        }
    
    @property
    def _llm_type(self) -> str:
        return "WithDataLLM"

# call example in ChatCompletionsWithLChain.py