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

# Initialize the conversation history in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey. From the initial concept "
            "to the final finishing touches, I seamlessly integrate into your project, "
            "ensuring a smooth and stress-free experience."
        )
    }]

# Title of the app
st.title("Home Renovation Assistant")

# Instantiate the RenovationAssistant class with the API key from Streamlit's secret store
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

# Display the existing conversation history
for message in st.session_state['conversation_history']:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input form
with st.form(key='user_input_form'):
    user_question = st.text_input("How may I assist with your home renovation?")
    submit_button = st.form_submit_button(label='Submit')

# Process the user's question on form submission
if submit_button and user_question:
    st.session_state['conversation_history'].append({'role': 'user', 'content': user_question})

    category_found = False
    for category in assistant.supplier_categories:
        if category in user_question.lower():
            category_advice = assistant.get_category_advice(category)
            st.session_state['conversation_history'].append({'role': 'assistant', 'content': category_advice})
            category_found = True
            break

    if not category_found:
        answer = assistant.ask_openai(user_question, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append({'role': 'assistant', 'content': answer})

    # Clear the user question input and rerun the app to update the UI
    st.session_state['user_input'] = ''
    st.experimental_rerun()

# Add a button to manually update the conversation history if needed
st.button("Update conversation", on_click=lambda: st.experimental_rerun())

