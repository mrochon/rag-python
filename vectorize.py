import os
import dotenv

from langchain_openai import AzureOpenAIEmbeddings

dotenv.load_dotenv()

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION", "2021-08-04"),
    azure_endpoint = os.environ.get("OPENAI_ENDPOINT"),
    api_key= os.environ.get("OPENAI_API_KEY")
)

text = "this is a test document"
query_result = embeddings.embed_query(text)
doc_result = embeddings.embed_documents([text])
print(doc_result[0][:5])