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
            return jsonify({'error': 'Invalid request: message field is required'}), 400
        user_message = data['message']
        chatbot_response = generate_response(user_message)
        return jsonify({'response': chatbot_response})
    else:
        return jsonify({'error': 'Invalid request method: use POST'}), 400


def generate_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """
                you only converse in english
                You are a helpful assistant that can answer any questions.
                Great as a personal assistant, customer service agent, or for general information.
                Get infos from web always up to date.
                always get right answer from web
                """},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.5,
            language="en",
            stop=["\n"],
            logprobs=10,
            presence_penalty=0.5,
            frequency_penalty=0.5,
            best_of=1,
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
