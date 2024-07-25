import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import PIL.Image

load_dotenv()
app = Flask(__name__)

AVAILABLE_MODELS = [
    'models/gemini-1.5-flash', 'models/gemini-1.0-pro', 'models/gemini-1.0-pro-001', 'models/gemini-1.0-pro-latest',
    'models/gemini-1.0-pro-vision-latest', 'models/gemini-1.5-flash-001',
    'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro', 'models/gemini-1.5-pro-001',
    'models/gemini-1.5-pro-latest', 'models/gemini-pro', 'models/gemini-pro-vision'
]

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def clear_uploads_folder(max_files=3):
    files = os.listdir(UPLOAD_FOLDER)
    if len(files) > max_files:
        files_to_delete = files[:-max_files]
        for file in files_to_delete:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/', methods=['GET'])
def home():
    return 'Chatbot Server is running!'


@app.route('/chat', methods=['POST'])
def chat():
    clear_uploads_folder()

    data = request.form
    file = request.files.get('file')
    if not data or 'message' not in data or 'model' not in data:
        return jsonify({'error': 'Invalid request: message and model fields are required'}), 400
    user_message = data['message']
    context = data.get('context', '')
    model_name = data['model']
    gemini_api_key = data.get('geminiApiKey')

    image_path = None
    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

    chatbot_response, image_path = Gemini_response(user_message, context, model_name, image_path, gemini_api_key)

    return jsonify({'response': chatbot_response, 'image_url': image_path if image_path else ''})


def Gemini_response(user_message, context, model_name, image_path=None, api_key=None):
    try:
        if not api_key:
            return "API Key is missing", None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])

        if image_path:
            img = PIL.Image.open(image_path)
            inputs = [user_message, img]
            response = model.generate_content(inputs, stream=False)
            chatbot_response = response.text
            return chatbot_response, image_path
        user_message_with_context = user_message + "\n" + context
        response = chat.send_message(user_message_with_context, stream=False)
        chatbot_response = response.text
        return chatbot_response, None
    except Exception as e:
        return str(e), None


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
