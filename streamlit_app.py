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
            'model': 'whisper-1',  # Model updated to 'gpt-4'
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

# Streamlit app initialization
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey. From the initial concept "
            "to the final finishing touches, I seamlessly integrate into your project, "
            "ensuring a smooth and stress-free experience."
        )
    }]

st.title("Home Renovation Assistant")

# Instantiate the assistant class using the OpenAI API key from Streamlit secrets
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

# Display the conversation history
for message in st.session_state.conversation_history:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input form to manage the state properly
with st.form(key='user_input_form'):
    user_input = st.text_input("How may I assist with your home renovation?")
    form_submit = st.form_submit_button("Submit")

# Callback function to handle form submission
def handle_form_submission():
    user_question = user_input  # Retrieve the input from the form
    if user_question:
        # Append the user's question
        st.session_state.conversation_history.append({'role': 'user', 'content': user_question})

        # Process the user's question against the assistant's supplier categories
        category_found = False
        for category, advice in assistant.supplier_categories.items():
            if category in user_question.lower():
                st.session_state.conversation_history.append({'role': 'assistant', 'content': advice})
                category_found = True
                break

        # If the user's question does not match any category, ask the assistant (GPT-4 model)
        if not category_found:
            answer = assistant.ask_openai(user_question, st.session_state.conversation_history)
            st.session_state.conversation_history.append({'role': 'assistant', 'content': answer})

        # The form has been submitted, now display the assistant's response
        for message in st.session_state.conversation_history[-2:]:  # Displaying the last 2 messages from the conversation history
            st.write(f"{message['role'].title()}: {message['content']}")

# Check if the user input form has been submitted
if form_submit:
    handle_form_submission()
