import os
import requests

class RenovationAssistant:

    def __init__(self):
        self.conversation_history = [{
            'role': 'system',
            'content': (
                "As a Home Renovation Project Assistant, I am your indispensable guide "
                "throughout every phase of the renovation journey. From the initial concept "
                "to the final finishing touches, I seamlessly integrate into your project, "
                "ensuring a smooth and stress-free experience."
            )
        }]
        self.openai_api_key = os.getenv('OPENAI_KEY')  # Fetching API key from environment variable
        self.supplier_categories = {
            'notary': 'Notary services provide witness and legal formalities for documentation.',
            'tax accountant': 'Tax accountants can help you maximize your returns and manage your financial paperwork.',
            'architect': 'Architects design the structure and aesthetics of your home according to your vision.',
            'building company': 'Building companies will execute the construction and renovation work on your home.'
        }

    def ask_openai(self, question):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}'
        }
        data = {
            'model': 'gpt-4-1106-preview',
            'messages': self.conversation_history + [{'role': 'user', 'content': question}]
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

        if response.status_code == 200:
            self.conversation_history.append({'role': 'user', 'content': question})
            answer_content = response.json()['choices'][0]['message']['content']
            self.conversation_history.append({'role': 'assistant', 'content': answer_content})
            return answer_content
        else:
            return f"Error: {response.status_code}, {response.text}"

    def get_category_advice(self, category):
        return self.supplier_categories.get(category.lower(), "I'm not sure about that category. Can you specify which service you are looking for?")

    def interact(self):
        while True:
            user_question = input("How may I assist with your home renovation? ")

            if user_question.lower() in ['exit', 'quit', 'stop']:
                print("Goodbye!")
                break

            category_found = False
            for category in self.supplier_categories:
                if category in user_question.lower():
                    category_advice = self.get_category_advice(category)
                    print(category_advice)
                    category_found = True
                    break
            if not category_found:  # No specific category was asked for, proceed with OpenAI response
                answer = self.ask_openai(user_question)
                print(answer)

# Create an instance of the assistant and begin interaction with the user
assistant = RenovationAssistant()
assistant.interact()
