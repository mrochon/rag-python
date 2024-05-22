import os
import dotenv
import requests
import json

dotenv.load_dotenv()

AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
GTP_DEPLOYMENT = os.environ.get("GTP_DEPLOYMENT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INDEX_NAME=os.environ.get("INDEX_NAME")
SEARCH_SERVICE_NAME = os.environ.get("SEARCH_SERVICE_NAME")
SEARCH_API_KEY=os.environ.get("SEARCH_API_KEY")

file_path = os.path.join(os.getcwd(), "data/chatCompletion.json")
with open(file_path, "r") as file:
    chatCompletion= json.load(file)
file_path = os.path.join(os.getcwd(), "data/system-prompt-02.txt")
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
            "fields_mapping": {
                "content_fields": [
                    "chunk"
                ],
                "title_field": None,
                "url_field": "uri",
                "filepath_field": "uri",
                "vector_fields": [
                    "chunkVector"
                ]
            },  
            "in_scope": False,
            "top_n_documents": 5,
            "query_type": "semantic",
            "semantic_configuration": "manuals-semantic-configuration",                      
            "role_information": "Reference manual for the Longer 3D printers and Citizen watches.",
            "filter": None,
            "strictness": 3
        }
    }
]


rest_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{GTP_DEPLOYMENT}/chat/completions?api-version=2024-02-01"
headers = {"api-key": OPENAI_API_KEY, "Content-Type": "application/json"}

while True:
    user_input = input("Enter your message (enter 'q' to quit): ")
    if user_input == 'q':
        break
    chatCompletion["messages"].append({"role": "user", "content": user_input})
    with open("requestOK.json","w") as f:
        f.write(json.dumps(chatCompletion, indent=2))    
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
        promptTokens = user_data["usage"]["prompt_tokens"]
        completionTokens = user_data["usage"]["completion_tokens"]        
        print(f"Prompt tokens    : {promptTokens}")
        print(f"Completion tokens: {completionTokens}")
        print(f"Total            : {promptTokens+completionTokens}")        
    else:
        print(f"Error fetching user data: {response.status_code} - {response.text}")


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