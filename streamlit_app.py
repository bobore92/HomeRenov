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
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}'
        }
        data = {
            'model': 'gpt-4',  # Use OpenAI's GPT-4 model
            'messages': conversation_history + [{'role': 'user', 'content': question}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            answer_content = response.json()['choices'][0]['message']['content']
            return answer_content
        else:
            error_info = response.json().get('error', {})
            return f"Error: {error_info.get('message', 'Unknown error occurred')}"

    def get_category_advice(self, category):
        return self.supplier_categories.get(category.lower(), "I'm not sure about that category. Can you specify which service you are looking for?")

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': "As a Home Renovation Project Assistant, I am your indispensable guide throughout every phase of the renovation journey."
    }]

st.title("Home Renovation Assistant")

assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

for message in st.session_state.conversation_history:
    st.write(f"{message['role'].title()}: {message['content']}")

# A form to handle the question submission
with st.form(key='user_input_form'):
    user_input = st.text_input("How may I assist with your home renovation?", key="user_input")
    submit_button = st.form_submit_button("Submit")

# Function that controls response addition
def add_response(question, role='user'):
    if not st.session_state.conversation_history or st.session_state.conversation_history[-1]['content'] != question:
        st.session_state.conversation_history.append({
            'role': role,
            'content': question
        })

if submit_button:
    # Process the input here
    add_response(user_input)

    category_found = False
    for category, advice in assistant.supplier_categories.items():
        if category in user_input.lower():
            add_response(advice, 'assistant')
            category_found = True
            break

    if not category_found:
        answer = assistant.ask_openai(user_input, st.session_state.conversation_history)
        add_response(answer, 'assistant')

    # Clear the user_input
    st.session_state.user_input = ""
