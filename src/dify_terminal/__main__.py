import json

from dify_client import ChatClient

api_key = "your_api_key"

# Initialize ChatClient
chat_client = ChatClient(api_key)

# Create Chat Message using ChatClient
chat_response = chat_client.create_chat_message(inputs={}, query="Hello", user="user_id", response_mode="streaming")
chat_response.raise_for_status()

for line in chat_response.iter_lines(decode_unicode=True):
    line = line.split('data:', 1)[-1]
    if line.strip():
        line = json.loads(line.strip())
        print(line.get('answer'))
