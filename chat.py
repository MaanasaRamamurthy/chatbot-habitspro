import openai
from langchain.memory import ChatMessageHistory
import os

api_key = os.getenv('OPENAI_API_KEY')
history = ChatMessageHistory()

# Define your template question
template_question = "Generate a targeted reply to understand them. Talk in a way that you are talking to your friend " \
                    "or family member. Keep the responses short and crisp. Make the user feel comfortable and at home." \
                    " Use cognitive behavioural therapy techniques to help the user overcome their problem: '{}'"


class ChatMessageHistory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, text):
        self.messages.append({"role": "user", "content": text})

    def add_ai_message(self, text):
        self.messages.append({"role": "assistant", "content": text})


def get_response(text):

    chat_history = ChatMessageHistory()
    system_message = "Generate targeted reply to understand them"
    if text:
        chat_history.add_user_message(text)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history.messages + [
                {"role": "system", "content": system_message},
            ],
        )
        translation = response.choices[0].message["content"]
        print(translation)
        chat_history.add_ai_message(translation)
        return translation
    else:
        return "Please enter a question"
