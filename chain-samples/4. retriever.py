import dotenv
dotenv.load_dotenv('.env', verbose=True, override=True)
import os
from langchain_openai import AzureChatOpenAI
COMPLETION_TOKENS = 2500
llm = AzureChatOpenAI(deployment_name=os.environ["GTP_DEPLOYMENT"], temperature=0.5, max_tokens=COMPLETION_TOKENS)

from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

dotenv.load_dotenv('.env', verbose=True, override=True)

from common.customAzureSearch import CustomAzureSearchRetriever
from azure.identity import DefaultAzureCredential

DOCSEARCH_PROMPT_TEXT = """Answer the question thoroughly, based **ONLY** on the following context:
{context}

Question: {question}
"""

DOCSEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", DOCSEARCH_PROMPT_TEXT),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{question}"),
    ]
)

cred = DefaultAzureCredential()
retriever = CustomAzureSearchRetriever(indexes=[os.environ['INDEX_NAME']], credential=cred, topK=5, reranker_threshold=1)

chain = (
    {
        "context": itemgetter("question") | retriever, # Passes the question to the retriever and the results are assign to context
        "question": itemgetter("question")
    }
    | DOCSEARCH_PROMPT
)
resp = chain.invoke({"question": "Which fillaments does Longer recommend?"})
print(resp)
