import dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from common.customAzureSearch import (CustomAzureSearchRetriever, QueryConfig)
from azure.identity import DefaultAzureCredential
from langchain_community.vectorstores.azuresearch import AzureSearch

dotenv.load_dotenv('.env', verbose=True, override=True)

DOCSEARCH_PROMPT_TEXT = """Answer the question thoroughly, based **ONLY** on the following context.
You must include references to document sources in your answer.

<context>
{context}
</contenxt>

Question: {question}
"""

DOCSEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", DOCSEARCH_PROMPT_TEXT),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{question}"),
    ]
)

COMPLETION_TOKENS = 2500
llm = AzureChatOpenAI(deployment_name=os.environ["GPT_DEPLOYMENT"], temperature=0.5, max_tokens=COMPLETION_TOKENS)
cred = DefaultAzureCredential()
index1 = {
    "endpoint": f"https://{os.environ['SEARCH_SERVICE_NAME']}.search.windows.net",
    "index": os.environ['INDEX_NAME'],
    "selectFields": ["uri", "chunk"],
    "queryType": "semantic",
    "vectorFieldName": "chunkVector",
    "semanticConfigurationName": "semantic-configuration",
}
retriever = CustomAzureSearchRetriever(
    configs=[
        QueryConfig(**index1)
    ], credential=cred)
parser = StrOutputParser()
chain = (
    {
        "context": itemgetter("question") | retriever, # Passes the question to the retriever and the results are assign to context
        "question": itemgetter("question")
    }
    | DOCSEARCH_PROMPT
    | llm
    | parser
)
resp = chain.invoke({"question": "Which fillaments does Longer recommend?"})
print(resp)
