import os
import dotenv
import requests
import json

dotenv.load_dotenv()

OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
GTP_DEPLOYMENT = os.environ.get("GTP_DEPLOYMENT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INDEX_NAME=os.environ.get("INDEX_NAME")
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")

file_path = os.path.join(os.getcwd(), "data/chatCompletion.json")
with open(file_path, "r") as file:
    chatCompletion= json.load(file)
    file_path = os.path.join(os.getcwd(), "data/system-prompt.txt")
with open(file_path, "r") as file:
    sysPrompt= file.read()

chatCompletion["messages"].append({"role": "system", "content": sysPrompt })
chatCompletion["data_sources"] = [
    {
        "type": "azure_search", 
        "parameters": {
            "authentication": {
                "type": "api_key",
                "key": SEARCH_API_KEY
            },
            "endpoint": f"https://{SEARCH_SERVICE_NAME}.search.windows.net",
            "index_name": INDEX_NAME,
            "role_information": "Reference manual for the Longer 3D printers and Citizen watches."
        }
    }
]

# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling?tabs=python
# Needs specific gtp models; not available in my subscription
# chatCompletion["tools"] = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_current_weather",
#                 "description": "Get the current weather in a given location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city and state, e.g. San Francisco, CA",
#                         },
#                         "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
#                     },
#                     "required": ["location"],
#                 },
#             },
#         }
# ]

#print(json.dumps(chatCompletion, indent=2))

rest_url = f"{OPENAI_ENDPOINT}/openai/deployments/{GTP_DEPLOYMENT}/chat/completions?api-version=2024-02-01"
headers = {"api-key": OPENAI_API_KEY, "Content-Type": "application/json"}

while True:
    user_input = input("Enter your message (enter 'q' to quit): ")
    if user_input == 'q':
        break
    chatCompletion["messages"].append({"role": "user", "content": user_input})
    response = requests.post(url=rest_url, headers=headers, json=chatCompletion)
    if response.status_code == 200:
        user_data = response.json()
        #print(json.dumps(user_data, indent=2))
        for choice in user_data["choices"]:
            print(f"{choice['message']['role']}: {choice['message']['content']}")
            for citation in choice["message"]["context"]["citations"]:
                print(f"{citation["url"]}-{citation["chunk_id"]}")
                #print(f"{citation['content']}")
            chatCompletion["messages"].append({"role": "assistant", "content": choice['message']['content']})
    else:
        print(f"Error fetching user data: {response.status_code} - {response.text}")
