# import random
# import json
#
# import torch
#
# from model import NeuralNet
# from nltk_utils import bag_of_words, tokenize
#
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#
# with open('intents.json', 'r') as json_data:
#     intents = json.load(json_data)
#
# FILE = "data.pth"
# data = torch.load(FILE)
#
# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data['all_words']
# tags = data['tags']
# model_state = data["model_state"]
#
# model = NeuralNet(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()
#
# bot_name = "Sam"
#
# def get_response(msg):
#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)
#
#     output = model(X)
#     _, predicted = torch.max(output, dim=1)
#
#     tag = tags[predicted.item()]
#
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 return random.choice(intent['responses'])
#
#     return "I do not understand..."
#
#
# if __name__ == "__main__":
#     print("Let's chat! (type 'quit' to exit)")
#     while True:
#         # sentence = "do you use credit cards?"
#         sentence = input("You: ")
#         if sentence == "quit":
#             break
#
#         resp = get_response(sentence)
#         print(resp)

# import streamlit as st
import openai
from langchain.memory import ChatMessageHistory
import os

api_key = os.getenv('OPENAI_API_KEY')
# openai.api_key="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"
history = ChatMessageHistory()

# Define your template question
template_question = "Generate a targeted reply to understand them. Talk in a way that you are talking to your friend or family member. Keep the responses short and crisp. Make the user feel comfortable and at home.: '{}'"

# Streamlit app code
def get_response(text):
    # st.title("Targeted questions")

    chat_history = ChatMessageHistory()

    # User input for the question
    # user_question = st.text_area("Enter questions and answers", "")

    # System message to set the context
    system_message = "Generate targeted reply to understand them"

    # if st.button("Generating questions"):
    if text:
            # Use the template question to create a prompt
        prompt = template_question.format(text)

            # Add the chat history to the prompt
        prompt += f"\n{chat_history.messages}"

            # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
            )
        history.add_user_message(text)
        history.add_ai_message(response.choices[0].message["content"])

        print(history.messages)
            # Extract and display the generated translation as a code block
        translation = response.choices[0].message["content"]

            # Add the response to the chat history
        chat_history.add_ai_message(translation)
            # for message in history.messages:
            #     st.write(message)
            # st.write(translation)
        return translation
    else:
            # st.warning("Please enter a question.")
        return "Please enter a question"

# if __name__ == "__main__":
#     main()