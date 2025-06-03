from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

# Review needed
openai.api_key = os.getenv("OPENAI_API_KEY")  

# AI Assistant prompt
SYSTEM_PROMPT = (
    "You're a coding mentor who explains with Munna Bhai style humor and clarity. "
    "After answering a chunk of the programming question, generate a follow-up MCQ with:\n"
    "- question (text)\n"
    "- options (list of 3 options)\n"
    "- correct_index (integer index 0/1/2)\n\n"
    "Return everything as a JSON object with 'message' and 'quiz'."
)

@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        user_prompt = data.get("query", "").strip()

        if not user_prompt:
            return jsonify({"answer": "No prompt received."}), 400

        # GPT-4o-mini model 
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        content = completion.choices[0].message.content

        # Parse response via JSON
        try:
            response_json = json.loads(content)
        except json.JSONDecodeError:
            return jsonify({"answer": "Sorry bhidu, model se kuch error aaya. Try again."}), 500

        return jsonify(response_json)

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)


