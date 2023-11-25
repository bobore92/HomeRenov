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
            'model': 'gpt-4',  # Updated model to "gpt-4"
            'messages': conversation_history + [{'role': 'user', 'content': question}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            answer_content = response.json()['choices'][0]['message']['content']
            return answer_content
        else:
            # Log the error response with the status code and returned message
            error_message = response.json().get('error', {}).get('message', '')
            return f"Error: {response.status_code}, {response.text}"

    def get_category_advice(self, category):
        return self.supplier_categories.get(category.lower(), "I'm not sure about that category. Can you specify which service you are looking for?")

# Initialize session_state for first-time use
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

st.title("Home Renovation Assistant")

# Instantiate the assistant class with the API key from the environment variable
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

# Display the existing conversation history
for message in st.session_state['conversation_history']:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input
user_input = st.text_input("How may I assist with your home renovation?", key="user_input")

# When the 'Submit' button is clicked, process the user's question
if st.button("Submit"):
    if user_input:
        # Append the user's question to the conversation history
        st.session_state['conversation_history'].append({'role': 'user', 'content': user_input})
        category_advice = assistant.get_category_advice(user_input)
        
        # Check if user input matches a supplier category
        if category_advice != "I'm not sure about that category. Can you specify which service you are looking for?":
            answer = category_advice
        else:
            # If no category is matched, use the OpenAI model to respond
            answer = assistant.ask_openai(user_input, st.session_state['conversation_history'])

        # Append the assistant's answer to the conversation history only if it is unique
        if not any(message['content'] == answer for message in st.session_state['conversation_history']):
            st.session_state['conversation_history'].append({'role': 'assistant', 'content': answer})

        # Clear the user input field
        st.session_state['user_input'] = ''

        # Update the UI with new messages by rerunning the script
        st.experimental_rerun()

