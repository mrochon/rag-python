import os
import dotenv
import uuid

dotenv.load_dotenv()

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION", "2021-08-04"),
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_API_KEY")
)
dir = os.path.join(os.getcwd(), "data")
files = os.listdir(dir)
txt_files = [file for file in files if file.lower().endswith(".txt")]
for file in txt_files:
    with open(f"{dir}/{file}", encoding='utf-8') as f:
        inputDoc = f.read()
        text_splitter = SemanticChunker(
            embeddings, breakpoint_threshold_type="percentile"
        )
        chunks = text_splitter.create_documents([inputDoc])
        id = str(uuid.uuid4())
        chunkNo = 0
        for chunk in chunks:
            outDoc = {
                "id": id,
                "source": f"{dir}/{file}",
                "chunk": chunkNo,
                "content": chunk.page_content
            }
            chunkNo += 1
            print(outDoc)
            print(f"Content length: {len(chunk.page_content)}")


    
    