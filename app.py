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

generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 65536,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-thinking-exp-01-21",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def get_hints_from_gemini(question):
    prompt = f"""
    You are an AI homework helper. Given the question below, let us walk through the problem together. What steps should we do first? Follow all the hints given and provide a JSON response with hints and an answer WITHOUT the beginning ```json and ending ```.
    Format:
    {{
      "question": "<restate the question>",
      "hint_1": "<first hint>",
      "hint_2": "<second hint>",
      "hint_3": "<third hint>",
      "answer": "<final answer>"
    }}

    "answer" should only have the answer.
    Feel free to add as many hints as you feel is needed. 
    Please make the hints build on each other with values so that you help the user get closer to the answer each time.
    
    Question: {question}
    """

    response = chat_session.send_message(prompt)

    data = response.text.strip("`json")
    
    try:
        hints_data = data
    except:
        hints_data = {"error": "Invalid response format from AI."}

    return hints_data

def get_hints_from_gemini_math(question):
    prompt = f"""
    You are an AI homework helper. Given the question below, let us walk through the problem together. What steps should we do first? Follow all the hints given and provide a JSON response with hints and an answer WITHOUT the beginning ```json and ending ```.
    Format the inline math parts including variables and constants in LaTeX using \\( <math> \\); use double backslashes for all single backslashes. There should be no single backslashes.
    Format:
    {{
      "question": "<restate the question>",
      "hint_1": "<first hint>",
      "hint_2": "<second hint>",
      "hint_3": "<third hint>",
      "answer": "\(<final answer>\)" 
    }}

    "answer" should only have the answer formatted in Latex.
    Feel free to add as many hints as you feel is needed. 
    Please make the hints build on each other with values so that you help the user get closer to the answer each time.
    If it is not a valid question, do not return a json. Return the string "not a valid question."

    Question: {question}
    """

    response = chat_session.send_message(prompt)

    print(response.text.strip("`json"))
  
    
    try:
        hints_data = eval(response.text.strip("`json")) 
    except:
        hints_data = {"error": "Invalid response format from AI."}

    return hints_data

@app.route('/get-hints', methods=['POST'])
def get_hints():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    hints_data = get_hints_from_gemini_math(question)

    return jsonify(hints_data)

if __name__ == '__main__':
    app.run(debug=True)
