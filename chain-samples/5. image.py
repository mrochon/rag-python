import dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

dotenv.load_dotenv('.env', verbose=True, override=True)

prompt = """
Anylyze this image and respond with a list of items it shows.
"""
COMPLETION_TOKENS = 2000
m = os.environ.get("GPT_DEPLOYMENT")
llm = AzureChatOpenAI(deployment_name=os.environ["GPT_DEPLOYMENT"], temperature=0.5, max_tokens=COMPLETION_TOKENS)
parser = StrOutputParser()
messages = [
    SystemMessage(content="Describe the image provided as input."),
    HumanMessage(content=[
        # {
        #     "type": "text", 
        #     "text": "What'\''s in this image?"
        # },
        {
            "type": "image_url", 
            "image_url": {
                "url": "https://cdnimg.webstaurantstore.com/images/products/large/758110/2572441.jpg"
            }
        }
    ]),
]
# res = llm.invoke(messages)
# print(res)

chain = llm | parser
res = chain.invoke(messages)
print(res)