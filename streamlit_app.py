import os
import requests
import streamlit as st

class RenovationAssistant:
    # ... [existing class definition] ...

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{
        'id': 'welcome',
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide "
            "throughout every phase of the renovation journey."
        )
    }]

# Function that generates a unique identifier for a message
def generate_message_id():
    return str(hash(f"{st.session_state['conversation_history'][-1]['id']}:{len(st.session_state['conversation_history'])}"))

st.title("Home Renovation Assistant")

# Instantiate the assistant class
assistant = RenovationAssistant(st.secrets["OPENAI_KEY"])

# Display the existing conversation history
for message in st.session_state['conversation_history']:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input
user_input = st.text_input("How may I assist with your home renovation?", key="user_input")

# On 'Submit' button click
if st.button("Submit"):
    # Append the user question to the conversation history only if it is not the last one
    if user_input and (not st.session_state['conversation_history'] or 
                       st.session_state['conversation_history'][-1].get('content') != user_input):
        # Add the user question with a unique ID
        st.session_state['conversation_history'].append({
            'id': generate_message_id(),
            'role': 'user',
            'content': user_input
        })
        
        category_found = False
        for category, advice in assistant.supplier_categories.items():
            if category in user_input.lower():
                st.session_state['conversation_history'].append({
                    'id': generate_message_id(),
                    'role': 'assistant',
                    'content': advice
                })
                category_found = True
                break

        # If no category found ask OpenAI API
        if not category_found:
            answer = assistant.ask_openai(user_input, st.session_state['conversation_history'])
            st.session_state['conversation_history'].append({
                'id': generate_message_id(),
                'role': 'assistant',
                'content': answer
            })

        # Clear the input
        st.session_state['user_input'] = ''
        # Rerun to refresh the state and the display
        st.experimental_rerun()

# Always show the last message
if st.session_state['conversation_history']:
    last_msg = st.session_state['conversation_history'][-1]
    st.write(f"{last_msg['role'].title()}: {last_msg['content']}")

