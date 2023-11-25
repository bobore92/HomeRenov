import os
import requests
import streamlit as st

class RenovationAssistant:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.supplier_categories = {
            'notary': 'Notary services provide witness and legal formalities for documentation.',
            'tax accountant': 'Tax accountants can help you maximize your returns and manage your financial paperwork.',
            'architect': 'Architects design the structure and aesthetics of your home according to your vision.',
            'building company': 'Building companies execute the construction and renovation work on your home.'
        }

    def ask_openai(self, question, conversation_history):
        # Rest of the ask_openai code

    def get_category_advice(self, category):
        # Rest of the get_category_advice code

# Ensure `conversation_history` is initialized in session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey."
        )
    }]

# Streamlit app interface
st.title("Home Renovation Assistant")

# Instantiate the RenovationAssistant class
openai_api_key = st.secrets["OPENAI_KEY"]
assistant = RenovationAssistant(openai_api_key)

# Display the conversation history
for message in st.session_state['conversation_history']:
    role = message['role'].title()
    st.write(f"{role}: {message['content']}")

# User input
user_question = st.text_input("How may I assist with your home renovation?", key="user_input")
submit_button = st.button("Submit")

if submit_button and user_question:
    st.session_state['conversation_history'].append({'role': 'user', 'content': user_question})

    category_found = False
    for category, advice in assistant.supplier_categories.items():
        if category in user_question.lower():
            st.session_state['conversation_history'].append({'role': 'assistant', 'content': advice})
            st.write(f"Assistant: {advice}")
            category_found = True
            break

    if not category_found:
        # Call the ask_openai method and append its response to the conversation history
        answer = assistant.ask_openai(user_question, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append({'role': 'assistant', 'content': answer})
        st.write(f"Assistant: {answer}")

    # Clear the text input box after processing
    st.session_state['user_input'] = ""

# Display an update button (optional, may help with rerun flow)
st.button("Update conversation", on_click=lambda: st.experimental_rerun())
