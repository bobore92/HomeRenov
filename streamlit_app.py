import streamlit as st
import requests

# Set the sidebar style to be at the bottom
SIDEBAR_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "width": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

st.title("AI - House Renovation")

# Instantiate the assistant class using the OpenAI API key from Streamlit secrets
assistant = RenovationAssistant("YOUR_OPENAI_API_KEY")

# Display the conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [{
        'role': 'system',
        'content': (
            "As a Home Renovation Project Assistant, I am your indispensable guide throughout every phase of the renovation journey. From the initial concept to the final finishing touches, I seamlessly integrate into your project, ensuring a smooth and stress-free experience."
        )
    }]

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
            st.write(f"{message['role']}: {message['content']}")

# Set sidebar style after the form definition
st.sidebar.markdown("<h1 style='color: #0b53a1;'>User Input</h1>", unsafe_allow_html=True)
st.text_input("", key="sidebar_input")

# Move the form submit button to the end
st.write("\n\n")  # Add space between the sidebar and the form button
form_submit  # Render the form submit button

# Display the image below the form and sidebar
st.markdown(
    f'<div style="display: flex; justify-content: center; align-items: center; height: 300px;">'
    f'<img src="https://raw.githubusercontent.com/bobore92/HomeRenov/27074fefb9ce62bb5a04595e22fa0357eefdb902/house-renovation.jpg" style="width:300px; height:auto;"/>'
    '</div>',
    unsafe_allow_html=True
)
