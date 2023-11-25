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
            return answer_content
        else:
            return f"Error: {response.status_code}, {response.text}"

    def get_category_advice(self, category):
        return self.supplier_categories.get(category.lower(), "I'm not sure about that category. Can you specify which service you are looking for?")

# Initialize the conversation history in the session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'role': 'system',
        'content': "As a Home Renovation Project Assistant, I am your indispensable guide " \
                   "throughout every phase of the renovation journey. From the initial concept " \
                   "to the final finishing touches, I seamlessly integrate into your project, " \
                   "ensuring a smooth and stress-free experience."
    }]

# Title of the Streamlit app
st.title("Home Renovation Assistant")

# Instantiate the RenovationAssistant class with the OpenAI API key from the environment variable
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

# Display all messages in the conversation history
for message in st.session_state.conversation_history:
    # Every message is displayed with the role as a title
    st.write(f"{message['role'].title()}: {message['content']}")

# Input text box for user query
user_question = st.text_input("How may I assist with your home renovation?", key="user_input")

# Process the input on pressing the 'Submit' button
if st.button("Submit"):
    # Ensure no duplicate messages by checking the last message content
    if user_question \
       and (not st.session_state['conversation_history'] or
            st.session_state['conversation_history'][-1]['content'] != user_question):
        # Add the user's message to the conversation history
        st.session_state['conversation_history'].append({
            'role': 'user',
            'content': user_question
        })
        # Find if the user's message matches a supplier category
        category_found = False
        for category, advice in assistant.supplier_categories.items():
            if category in user_question.lower():
                # Add the assistant's reply to the conversation history
                st.session_state['conversation_history'].append({
                    'role': 'assistant',
                    'content': advice
                })
                category_found = True
                break  # Exit the loop on the first match
        
        # Ask OpenAI if no categorized advice was found
        if not category_found:
            # Get the answer from OpenAI and add to the conversation history
            answer = assistant.ask_openai(user_question, st.session_state['conversation_history'])
            st.session_state['conversation_history'].append({
                'role': 'assistant',
                'content': answer
            })

        # Clear the user input field for next message
        st.session_state['user_input'] = ''
        # Rerun the app to clear the input box and avoid duplicated processing
        st.experimental_rerun()

