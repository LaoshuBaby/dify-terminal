import json
import os

from dify_client import ChatClient

api_key = os.environ["DIFY_LOCAL_API_KEY"]
conversation_id = os.environ.get("DIFY_LOCAL_CONVERSATION_ID", None)

# Initialize ChatClient
chat_client = ChatClient(api_key)
chat_client.base_url = "http://localhost/v1"


def user_say(what: str):
    global conversation_id
    chat_response = chat_client.create_chat_message(
        inputs={}, query=what, user="dify_terminal", conversation_id=conversation_id, response_mode="streaming"
    )
    chat_response.raise_for_status()
    accumulated_answer = ""
    for line in chat_response.iter_lines(decode_unicode=True):
        # line="event: ping" when starting the LLM
        if not line.startswith("data:"):
            continue
        data: str = line.split("data:", 1)[-1]
        if data := data.strip():
            dic = json.loads(data)

            if conversation_id is None:
                conversation_id = dic.get("conversation_id")

            if answer := dic.get("answer"):
                accumulated_answer += answer
                # ref: https://stackoverflow.com/a/3249539/11397457
                print(accumulated_answer, end='\r', flush=True)


def main():
    while True:
        query = input(": ")
        if not query:
            continue
        user_say(query)
        # start a new line
        print("")


if __name__ == "__main__":
    main()
