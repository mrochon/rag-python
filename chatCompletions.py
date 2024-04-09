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


#chatCompletion["messages"].append({"role": "system", "content": "You are a helpful assistant answering questions about creativity. Use Azure Search data whenever possible."})
chatCompletion["messages"].append({"role": "user", "content": "What are the two modes people function in?"})


chatCompletion["data_sources"] = [
    {
        "type": "azure_search",
        "parameters": {
            "authentication": {
                "type": "api_key",
                "key": SEARCH_API_KEY
            },
            "endpoint": f"https://{SEARCH_SERVICE_NAME}.search.windows.net",
            "index_name": INDEX_NAME
        }
    }
]

#print(json.dumps(chatCompletion, indent=2))

rest_url = f"{OPENAI_ENDPOINT}/openai/deployments/{GTP_DEPLOYMENT}/chat/completions?api-version=2024-02-01"
headers = {"api-key": OPENAI_API_KEY, "Content-Type": "application/json"}

while True:
    user_input = input("Enter your message (enter 'q' to quit): ")
    #example: What are the two modes people function in?
    if user_input == 'q':
        break
    chatCompletion["messages"].append({"role": "user", "content": user_input})
    response = requests.post(url=rest_url, headers=headers, json=chatCompletion)
    if response.status_code == 200:
        user_data = response.json()
        #print(json.dumps(user_data, indent=2))
        for choice in user_data["choices"]:
            print(f"{choice['message']['role']}: {choice['message']['content']}")
            chatCompletion["messages"].append({"role": "assistant", "content": choice['message']['content']})
    else:
        print(f"Error fetching user data: {response.status_code} - {response.text}")
