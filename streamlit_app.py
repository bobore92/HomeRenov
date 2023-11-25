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
        # ... (rest of the ask_openai code)

    def get_category_advice(self, category):
        # ... (rest of the get_category_advice code)

# Initialize conversation history in st.session_state if not present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey."
        )
    }]

# Streamlit app interface setup
st.title("Home Renovation Assistant")

# Instantiate the assistant class
openai_api_key = st.secrets["OPENAI_KEY"]
assistant = RenovationAssistant(openai_api_key)

# Display conversation history
for message in st.session_state['conversation_history']:
    role = message['role'].title()
    st.write(f"{role}: {message['content']}")

# User input
user_question = st.text_input("How may I assist with your home renovation?", key="user_input")
submit_button = st.button("Submit")

if submit_button and user_question:
    st.session_state['conversation_history'].append({'role': 'user', 'content': user_question})

    category_found = False
    for category in assistant.supplier_categories:
        if category in user_question.lower():
            category_advice = assistant.get_category_advice(category)
            st.session_state['conversation_history'].append({'role': 'assistant', 'content': category_advice})
            st.write(f"Assistant: {category_advice}")
            category_found = True
            break
    
    if not category_found:
        answer = assistant.ask_openai(user_question, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append({'role': 'assistant', 'content': answer})
        st.write(f"Assistant: {answer}")

    st.experimental_rerun()
