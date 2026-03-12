import requests
import json

# Test the chatbot API
url = "http://localhost:8000/api/chat/"

test_messages = [
    "Hello",
    "I need motivation",
    "I feel sad",
    "Give me a love quote",
    "Show me success quotes"
]

print("Testing NLP Backend...\n")

for message in test_messages:
    try:
        response = requests.post(url, json={"message": message})
        data = response.json()
        
        print(f"User: {message}")
        print(f"Bot: {data.get('response')}")
        print(f"Source: {data.get('source', 'backend')}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}\n")

print("\nNLP Backend is working! No Rasa needed.")
