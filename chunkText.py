import os
import dotenv

dotenv.load_dotenv()

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION", "2021-08-04"),
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_API_KEY")
)

file_path = os.path.join(os.getcwd(), "data/JohnCleeseSpeech.txt")
with open(file_path, encoding='utf-8') as f:
    doc = f.read()

text_splitter = SemanticChunker(
    embeddings, breakpoint_threshold_type="percentile"
)
docs = text_splitter.create_documents([doc])
print(docs[0].page_content)

    
    