import requests
import json
from typing import Any, Dict, Iterator, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk

class WithDataLLM(LLM):
    openAIServiceName: str
    deploymentName: str
    openAIServiceKey: str
    searchServiceName: str
    searchApiKey: str
    indexName: str
    indexRoleDescription: str
    systemPrompt: str
    _history: List[str]

    @property
    def _llm_type(self) -> str:
        return "WithDataLLM"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        url = f"{self.openAIServiceName}/openai/deployments/{self.deploymentName}/chat/completions?api-version=2024-02-01"
        headers = {"api-key": self.openAIServiceKey, "Content-Type": "application/json"}
        data_sources =     {
            "type": "azure_search", 
            "parameters": {
                "authentication": {
                    "type": "api_key",
                    "key": self.searchApiKey
                },
                "endpoint": f"https://{self.searchServiceName}.search.windows.net",
                "index_name": self.indexName,
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
                "role_information": self.indexRoleDescription,
                "filter": None,
                "strictness": 3
            }
        }

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
                {"role": "system", "content": self.systemPrompt },
                {"role": "user", "content": prompt}],
            "data_sources": [data_sources]
        }
        with open("request.json","w") as f:
            f.write(json.dumps(payload, indent=2))
        response = requests.post(url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        user_data = response.json()
        with open("response.json","w") as f:
            f.write(json.dumps(user_data, indent=2))        
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
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "custom"
