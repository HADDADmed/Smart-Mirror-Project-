import google.generativeai as genai
from flask_cors import CORS  # Import CORS from flask_cors

def chatbot(question):
    genai.configure(api_key="")
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
    response = model.generate_content([f"{question}"])
    return response.text  # Return the response instead of printing it

from flask import Flask
from flask import request
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the Flask app

@app.route("/", methods=['GET', 'POST'])
def chat():
    question=request.data
    print(question)
    response = chatbot(question)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
