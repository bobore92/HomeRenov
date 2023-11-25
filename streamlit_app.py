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
            'model': 'gpt-4-1106-preview',
            'messages': conversation_history + [{'role': 'user', 'content': question}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            answer_content = response.json()['choices'][0]['message']['content']
            conversation_history.append({'role': 'user', 'content': question})
            conversation_history.append({'role': 'assistant', 'content': answer_content})
            return answer_content
        else:
            return f"Error: {response.status_code}, {response.text}"

    def get_category_advice(self, category):
        return self.supplier_categories.get(category.lower(), "I'm not sure about that category. Can you specify which service you are looking for?")

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey."
        )
    }]

if 'last_question' not in st.session_state:
    st.session_state['last_question'] = ""

st.title("Home Renovation Assistant")
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

for message in st.session_state.conversation_history:
    st.write(f"{message['role'].title()}: {message['content']}")

with st.form(key='user_interaction_form'):
    user_question = st.text_input("How may I assist with your home renovation?", key="user_question")
    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    if user_question and user_question != st.session_state.last_question:
        st.session_state.last_question = user_question
        st.session_state.conversation_history.append({'role': 'user', 'content': user_question})

        category_found = False
        for category in assistant.supplier_categories:
            if category in user_question.lower():
                category_advice = assistant.get_category_advice(category)
                st.session_state.conversation_history.append({'role': 'assistant', 'content': category_advice})
                category_found = True
                break  # Break the loop since we found the category

        if not category_found:
            # No category found, let's ask OpenAI
            answer = assistant.ask_openai(user_question, st.session_state.conversation_history)
            st.session_state.conversation_history.append({'role': 'assistant', 'content': answer})

        # Since we've processed this new question, let's rerun the app to clean up for the next input
        st.experimental_rerun()

