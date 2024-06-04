from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request: message field is required'}), 400

    user_message = data['message']
    context = data.get('context', '')

    chatbot_response = generate_response(user_message, context)
    return jsonify({'response': chatbot_response})

def generate_response(user_message, context):
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
            stop=None
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
