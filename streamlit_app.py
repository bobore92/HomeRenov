import os
import requests
import streamlit as st

class RenovationAssistant:
    # ... (rest of the RenovationAssistant class)

# Ensure conversation_history is initialized in session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [
        {'role': 'system', 'content': "..."}  # The system's welcome message
    ]

st.title("Home Renovation Assistant")

# Instantiate the assistant class
openai_api_key = st.secrets["OPENAI_KEY"]
assistant = RenovationAssistant(openai_api_key)

# Display the conversation history
for message in st.session_state['conversation_history']:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input with a callback to update session state
def on_user_input():
    input_value = st.session_state['user_input']
    if input_value:
        st.session_state['conversation_history'].append({'role': 'user', 'content': input_value})

        # ... (rest of the processing)

        # Clear the input after processing
        st.session_state['user_input'] = ''  # Reset the input box
        # No need to rerun the whole script, just continue after user_input is processed

# Widget for the user's question
user_question = st.text_input(
    "How may I assist with your home renovation?",
    key="user_input",
    on_change=on_user_input
)

st.button("Submit", on_click=on_user_input)
