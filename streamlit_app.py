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
for message in st.session_state.conversation_history:
    st.write(f"{message['role'].title()}: {message['content']}")

# User input
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

user_question = st.text_input("How may I assist with your home renovation?", value=st.session_state.user_input, key="user_input")

submit_button = st.button("Submit")

if submit_button and user_question:
    st.session_state['conversation_history'].append({'role': 'user', 'content': user_question})
    st.session_state['user_input'] = ''  # Clear the input
    st.session_state.save()  # Save the session state changes

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

    st.experimental_rerun()

st.button("Update conversation", on_click=lambda: st.experimental_rerun())
