import os
import requests
import streamlit as st

class RenovationAssistant:
    # Removed self.conversation_history from __init__ as it will be managed by st.session_state

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

# Initialize conversation history in st.session_state if not present
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

# Streamlit app
st.title("Home Renovation Assistant")

# Create an instance of the assistant
openai_api_key = st.secrets["OPENAI_KEY"]
assistant = RenovationAssistant(openai_api_key)

# Display the conversation history
for message in st.session_state['conversation_history']:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input
user_question = st.text_input("How may I assist with your home renovation?", key="user_input")

if user_question:
    # Add input question to the conversation and clear the input
    st.session_state['conversation_history'].append({'role': 'user', 'content': user_question})
    st.session_state['user_input'] = ""

    category_found = False
    for category in assistant.supplier_categories:
        if category in user_question.lower():
            category_advice = assistant.get_category_advice(category)
            st.session_state['conversation_history'].append({'role': 'assistant', 'content': category_advice})
            category_found = True
            break
    
    # If no specific category was asked for, proceed with OpenAI response
    if not category_found:
        answer = assistant.ask_openai(user_question, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append({'role': 'assistant', 'content': answer})

    # Re-display conversation history with the new messages
    st.experimental_rerun()

# Clear the display and add a way to show the updated conversation history
st.button("Update conversation", on_click=st.experimental_rerun)
