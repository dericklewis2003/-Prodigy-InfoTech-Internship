import PySimpleGUI as sg
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variable
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# API endpoint
API_URL = "https://api-inference.huggingface.co/models/gpt2-large"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                window['-OUTPUT-'].print(f"API Error: {str(e)}. Retrying in {delay} seconds...\n")
                time.sleep(delay)
            else:
                return f"API Error: {str(e)}"

def generate_text(prompt, max_length=250):  # Increased from 150 to 250
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "top_k": 50,
            "top_p": 0.95,
            "temperature": 0.7,
            "num_return_sequences": 1,
        }
    }
    response = query(payload)
    if isinstance(response, str):  # This means we got an error message
        return response
    elif isinstance(response, list) and len(response) > 0:
        return response[0]["generated_text"]
    else:
        return f"Unexpected response format: {response}"

def create_window():
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text('Topic Chatbot', font=('Helvetica', 20))],
        [sg.Text('Enter a topic:', font=('Helvetica', 14)), sg.InputText(key='-TOPIC-', font=('Helvetica', 14))],
        [sg.Button('Generate', font=('Helvetica', 14)), sg.Button('Clear', font=('Helvetica', 14)), sg.Button('Exit', font=('Helvetica', 14))],
        [sg.Multiline(size=(60, 15), key='-OUTPUT-', font=('Helvetica', 12), autoscroll=True, disabled=True)]
    ]
    return sg.Window('Topic Chatbot', layout, finalize=True)

def main():
    window = create_window()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Generate':
            topic = values['-TOPIC-']
            if topic:
                prompt = f"Provide information about {topic}. Focus on key facts, details, and interesting aspects related to {topic}:"
                window['-OUTPUT-'].print(f"Generating text for topic: {topic}...\n")
                generated_text = generate_text(prompt)
                if generated_text.startswith("API Error"):
                    window['-OUTPUT-'].print(f"Error: {generated_text}\n")
                    window['-OUTPUT-'].print("You can try the following:\n")
                    window['-OUTPUT-'].print("1. Wait a few minutes and try again.\n")
                    window['-OUTPUT-'].print("2. Check your internet connection.\n")
                    window['-OUTPUT-'].print("3. Verify your API token in the .env file.\n")
                else:
                    window['-OUTPUT-'].print(f"Topic: {topic}\n\n{generated_text}\n\n")
            else:
                window['-OUTPUT-'].print("Please enter a topic.\n\n")
        if event == 'Clear':
            window['-OUTPUT-'].update('')
            window['-TOPIC-'].update('')

    window.close()

if __name__ == "__main__":
    main()
