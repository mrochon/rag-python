from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

class WithDataLLM(LLM):
    url: str
    def __init__(self, openAIServiceName, **kwargs):
        #super().__init__(**kwargs)
        self.url = f"{openAIServiceName}/openai/deployments"
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


llm = WithDataLLM("test")

