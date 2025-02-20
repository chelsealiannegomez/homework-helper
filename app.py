from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

load_dotenv()

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_hints_from_gemini(question):
    prompt = f"""
    You are an AI homework helper. Given the question below, provide a JSON response with hints and an answer.
    Format:
    {{
      "question": "<restate the question>",
      "hint_1": "<first hint>",
      "hint_2": "<second hint>",
      "hint_3": "<third hint>",
      "answer": "<final answer>"
    }}
    Feel free to add as many hints as you feel is needed. Please only return the json format without the beginning and ending ```, only the dictionary.
    Question: {question}
    """
    response = model.generate_content(prompt)
    try:
        hints_data = eval(response.text) 
    except:
        hints_data = {"error": "Invalid response format from AI."}

    return hints_data

@app.route('/get-hints', methods=['POST'])
def get_hints():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    hints_data = get_hints_from_gemini(question)

    return jsonify(hints_data)

if __name__ == '__main__':
    app.run(debug=True)
