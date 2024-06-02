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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                You are a helpful assistant with detailed knowledge about XYZ College.
                Here are some details about XYZ College:
                - Located in ABC City.
                - Established in 1900.
                - Known for its excellent programs in Computer Science, Engineering, and Business.
                - Has a student body of 10,000 students.
                - Famous alumni include John Doe, Jane Smith, and others.
                - The college motto is "Knowledge and Wisdom".
                - Offers a variety of extracurricular activities including sports, music, and drama.
                - The college has a strong research focus with several research centers in AI, Robotics, and Biotechnology.
                """},
                {"role": "user", "content": user_message}
            ]
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
