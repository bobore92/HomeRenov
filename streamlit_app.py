import streamlit as st
import requests

# Define sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "width": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

class RenovationAssistant:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.supplier_categories = {
            'notary': 'Notary services provide witness and legal formalities for documentation.',
            'tax accountant': 'The role of a tax accountant encompasses providing assistance with regulatory compliance, which includes completing forms related to renovations and managing incentives such as the superbonus.',
            'architect': 'Architects design the structure and aesthetics of your home according to your vision.',
            'building company': 'Building companies execute the construction and renovation work on your home.'
        }

    def ask_openai(self, question, conversation_history):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}'
        }
        data = {
            'model': 'gpt-3.5-turbo-1106',
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
st.title("AI - House Renovation")

# Instantiate the assistant class using the OpenAI API key from Streamlit secrets
assistant = RenovationAssistant("YOUR_OPENAI_API_KEY")

# Set sidebar style
st.sidebar.markdown("<h1 style='color: #0b53a1;'>User Input</h1>", unsafe_allow_html=True)
user_input = st.sidebar.text_input("How may I assist with your home renovation?")
form_submit = st.sidebar.form_submit_button("Submit")

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
            st.write(f"{message['role']}: {message['content']}")

# Display the image
st.markdown(
    f'<div style="display: flex; justify-content: center; align-items: center; height: 300px;">'
    f'<img src="https://raw.githubusercontent.com/bobore92/HomeRenov/27074fefb9ce62bb5a04595e22fa0357eefdb902/house-renovation.jpg" style="width:300px; height:auto;"/>'
    '</div>',
    unsafe_allow_html=True
)

# Handle form submission
handle_form_submission()
