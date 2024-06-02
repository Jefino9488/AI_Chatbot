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
        return jsonify({'error': 'Invalid request'}), 400


def generate_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": user_message
                       }],
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
