import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from g4f.client import Client
import google.generativeai as genai

app = Flask(__name__)
client = Client()
load_dotenv()
@app.after_request
def add_cors_headers(response):
    """
    :param response:
    :return:
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/chat', methods=['POST'])
def chat():
    """
    :return:
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request: message field is required'}), 400

    user_message = data['message']
    context = data.get('context', '')

    chatbot_response = generate_response(user_message, context)
    return jsonify({'response': chatbot_response})

def Gemini_response(user_message):
    try:
        api_key = os.getenv('API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])
        response = chat.send_message(user_message, stream=False)
        chatbot_response = response.text
        return chatbot_response
    except Exception as e:
        return str(e)

def generate_response(user_message, context):
    """
    :param user_message:
    :param context:
    :return:
    """
    try:
        user_message_with_context = user_message + "\n" + context
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """
                You are a helpful assistant that can answer any questions.
                Use the provided context to give accurate answers.
                """},
                {"role": "user", "content": user_message_with_context}
            ],
            max_tokens=150,
            temperature=0.5,
            language="en",
            best_of=1,
            stop=None
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8000, debug=True)