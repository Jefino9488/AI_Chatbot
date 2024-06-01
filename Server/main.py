from flask import Flask, request, jsonify

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        user_message = data['message']
        chatbot_response = generate_response(user_message)
        return jsonify({'response': chatbot_response})
    else:
        return jsonify({'message': ['Hello', 'Hi', 'How are you?']})


def generate_response(user_message):
    if user_message.lower() == 'how are you?':
        return "I'm fine, thank you!"
    return f"You said: {user_message}"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
