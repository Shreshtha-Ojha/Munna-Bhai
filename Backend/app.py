from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# App is intialized
app = Flask(__name__)
CORS(app)

# Openai API Key code
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_FALLBACK_KEY")

# Answering style
SYSTEM_PROMPT = (
    "You're a funny but detailed coding assistant. "
    "Always explain in steps. "
    "After correct answers say 'Waah bhidu, Tu jaadu ki jhappi deserve karta hai...'. "
    "If wrong, start with 'Tension nahi lene ka bhidu.Appun hai naa...'."
)

# AI Assistant ka route yahaan hai
@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        user_prompt = data.get("query", "").strip()

        if not user_prompt:
            return jsonify({"answer": "No prompt received."}), 400

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500

# Server runs here
if __name__ == "__main__":
    app.run(debug=True)

