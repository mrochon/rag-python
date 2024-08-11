import os
import dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

# Get value of an argument passed in the py command
import argparse
parser = argparse.ArgumentParser(description='Query Creation')
parser.add_argument('--version', type=str, help='Which folder to use (suffix)')
args = parser.parse_args()
version = args.version
if(version == None):
    version = "0"

file_path = os.path.join(os.getcwd(), f"queryPrompts/ver{version}/sysPrompt.txt")
with open(file_path, "r") as file:
    sysPrompt= file.read()
file_path = os.path.join(os.getcwd(), f"queryPrompts/ver{version}/userPrompt.txt")
with open(file_path, "r") as file:
    userPrompt= file.read()

dotenv.load_dotenv('.env', verbose=True, override=True)
COMPLETION_TOKENS = 2500
llm = AzureChatOpenAI(deployment_name=os.environ["GPT_DEPLOYMENT"], temperature=0.5, max_tokens=COMPLETION_TOKENS)

messages = [
    SystemMessage(content=sysPrompt),
    HumanMessage(content=userPrompt),
]

parser = StrOutputParser()
chain = llm | parser
r = chain.invoke(messages)

print(r)
