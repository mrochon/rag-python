# See https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter/

import os
import uuid
import tiktoken

from langchain_text_splitters import RecursiveCharacterTextSplitter

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

dir = os.path.join(os.getcwd(), "data")
files = os.listdir(dir)
txt_files = [file for file in files if file.lower().endswith(".txt")]
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
for file in txt_files:
    with open(f"{dir}/{file}", encoding='utf-8') as f:
        inputDoc = f.read()
        chunks = text_splitter.create_documents([inputDoc])
        id = str(uuid.uuid4())
        chunkNo = 0
        for chunk in chunks:
            # TODO: vectorize content
            outDoc = {
                "id": id,
                "source": f"{dir}/{file}",
                "chunk": chunkNo,
                "content": chunk.page_content
            }
            chunkNo += 1
            print(outDoc)
            print(f"Content length: {len(chunk.page_content)}")
            tokens = num_tokens_from_string(chunk.page_content, "gpt-3.5-turbo")
            print(f"Tokens: {tokens}")


    
    