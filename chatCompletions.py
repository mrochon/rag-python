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


chatCompletion["messages"].append({"role": "system", "content": "You are a helpful assistant answering questions about astronomy."})
chatCompletion["messages"].append({"role": "user", "content": "How far is the moon from the earth?"})
chatCompletion["messages"].append({"role": "assistant", "content": "The average distance from the Earth to the Moon is 238,855 miles."})
chatCompletion["messages"].append({"role": "user", "content": "What is it in light units?"})

#print(json.dumps(chatCompletion, indent=2))

rest_url = f"{OPENAI_ENDPOINT}/openai/deployments/{GTP_DEPLOYMENT}/chat/completions?api-version=2024-02-01"
headers = {"api-key": OPENAI_API_KEY, "Content-Type": "application/json"}

response = requests.post(url=rest_url, headers=headers, json=chatCompletion)

if response.status_code == 200:
    user_data = response.json()
    #print(json.dumps(user_data, indent=2))
    for choice in user_data["choices"]:
        print(f"{choice['message']['role']}: {choice['message']['content']}")
        chatCompletion["messages"].append({"role": "assistant", "content": choice['message']['content']})
else:
    print(f"Error fetching user data: {response.status_code} - {response.text}")
