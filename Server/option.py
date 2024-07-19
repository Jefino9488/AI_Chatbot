"""
Install the Google AI Python SDK
$ pip install google-generativeai
See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from load_creds import load_creds

creds = load_creds()

genai.configure(credentials=creds)

model = genai.GenerativeModel(model_name="tunedModels/personal-assistant-ldkxhepfc22e")

response = model.generate_content(["touch"])

print(response.text)
