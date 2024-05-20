import sys
import os
import dotenv
import requests
import json
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

dotenv.load_dotenv('.env', verbose=True, override=True)

from common.customAzureSearch import CustomAzureSearchRetriever
from azure.identity import DefaultAzureCredential

DOCSEARCH_PROMPT_TEXT = """

## On your ability to answer question based on fetched documents (sources):
- Given extracted parts (CONTEXT) from one or multiple documents, and a question, Answer the question thoroughly with citations/references. 
- If there are conflicting information or multiple definitions or explanations, detail them all in your answer.
- In your answer, **You MUST use** all relevant extracted parts that are relevant to the question.
- **YOU MUST** place inline citations directly after the sentence they support using this Markdown format: `[[number]](url)`.
- The reference must be from the `source:` section of the extracted parts. You are not to make a reference from the content, only from the `source:` of the extract parts.
- Reference document's URL can include query parameters. Include these references in the document URL using this Markdown format: [[number]](url?query_parameters)
- **You MUST ONLY answer the question from information contained in the extracted parts (CONTEXT) below**, DO NOT use your prior knowledge.
- Never provide an answer without references.
- You will be seriously penalized with negative 10000 dollars if you don't provide citations/references in your final answer.
- You will be rewarded 10000 dollars if you provide citations/references on paragraph and sentences.
- **You must** respond in the same language as the question, regardless of the language of the CONTEXT


- Remember to respond in the same language as the question
"""

DOCSEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", DOCSEARCH_PROMPT_TEXT + "\n\nCONTEXT:\n{context}\n\n"),
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
# for chunk in chain.stream({"question": "What is the population of Denmark?"}):
#     print(chunk, end="", flush=True)