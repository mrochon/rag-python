import os
import dotenv
import requests
import json
import time

dotenv.load_dotenv(".env", verbose=True, override=True)

OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
OPEN_API_VERSION = os.environ.get("OPEN_API_VERSION", "2024-02-01")
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
chatCompletion["stream"] = True
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

rest_url = f"{OPENAI_ENDPOINT}/openai/deployments/{GTP_DEPLOYMENT}/chat/completions?api-version={OPEN_API_VERSION}"
headers = {"api-key": OPENAI_API_KEY, "Content-Type": "application/json"}

while True:
    #user_input = input("Enter your message (enter 'q' to quit): ")
    user_input = "What is the recommended filament?"
    if user_input == 'q':
        break
    chatCompletion["messages"].append({"role": "user", "content": user_input})
    response = requests.post(url=rest_url, headers=headers, json=chatCompletion)
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                #print(line[0:10])
                user_data = json.loads(line[6:])
                #print(json.dumps(user_data, indent=2))
                choices = user_data["choices"]
                if choices[0]['finish_reason'] == 'stop':
                    print()
                    print("Chat completed")
                    break
                for choice in choices:
                    delta = choice["delta"]
                    if 'content' in delta:
                        print(delta['content'], end="")
                        time.sleep(0.05)
                    elif 'role' in delta:
                        print()
                        print("ChatGPT used these intents when searching:")
                        print(delta['context']['intent'])
    else:
        print(f"Error fetching user data: {response.status_code} - {response.text}")
