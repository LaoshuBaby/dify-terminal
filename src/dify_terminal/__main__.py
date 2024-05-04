import json
import os

from dify_client import ChatClient

api_key = os.environ["DIFY_LOCAL_API_KEY"]

# Initialize ChatClient
chat_client = ChatClient(api_key)
chat_client.base_url = "http://localhost/v1"

while True:
    query = input("输入：")
    if not query:
        continue

    chat_response = chat_client.create_chat_message(inputs={}, query=query, user="user_id", response_mode="streaming")
    chat_response.raise_for_status()

    accumulated_answer = ""
    for line in chat_response.iter_lines(decode_unicode=True):
        line = line.split('data:', 1)[-1]
        if line.strip():
            line = json.loads(line.strip())
            if answer := line.get('answer'):
                accumulated_answer += answer
                print("\r", accumulated_answer, end="")

    print("")
