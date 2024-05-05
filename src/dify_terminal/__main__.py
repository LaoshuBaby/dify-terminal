import json
import os
import warnings

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

    for line in chat_response.iter_lines(decode_unicode=True):
        # line="event: ping" when starting the LLM
        if not line.startswith("data:"):
            continue
        data: str = line.split("data:", 1)[-1]
        if data := data.strip():
            dic: dict = json.loads(data)

            if conversation_id is None:
                conversation_id = dic.get("conversation_id")

            if answer := dic.get("answer"):
                # ref: https://stackoverflow.com/questions/3249524/print-in-one-line-dynamically/3249539#3249539
                print(answer, end="", flush=True)

    # append a "\n" at the end of LLM response
    print("")


def main():
    counter = 0
    while True:
        try:
            query = input("> ")
            if not query:
                continue
            print("-")
            user_say(query)
            counter += 1
        except Exception as e:
            warnings.warn(str(e), stacklevel=1)
        finally:
            print(f"--- {counter} ---")


if __name__ == "__main__":
    main()
