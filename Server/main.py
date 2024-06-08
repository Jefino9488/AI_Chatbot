import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
load_dotenv()

AVAILABLE_MODELS = [
    'models/gemini-1.0-pro', 'models/gemini-1.0-pro-001', 'models/gemini-1.0-pro-latest',
    'models/gemini-1.0-pro-vision-latest', 'models/gemini-1.5-flash', 'models/gemini-1.5-flash-001',
    'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro', 'models/gemini-1.5-pro-001',
    'models/gemini-1.5-pro-latest', 'models/gemini-pro', 'models/gemini-pro-vision'
]


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data or 'model' not in data:
        return jsonify({'error': 'Invalid request: message and model fields are required'}), 400

    user_message = data['message']
    context = data.get('context', '')
    model_name = data['model']

    chatbot_response = Gemini_response(user_message, context, model_name)
    return jsonify({'response': chatbot_response})


def Gemini_response(user_message, context, model_name):
    try:
        api_key = os.getenv('API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        user_message_with_context = user_message + "\n" + context
        response = chat.send_message(user_message_with_context, stream=False)
        chatbot_response = response.text
        return chatbot_response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
