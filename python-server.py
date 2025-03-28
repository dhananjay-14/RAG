from flask import Flask, request, jsonify
import google.generativeai as genai
import subprocess
from dotenv import load_dotenv
import os
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

def retrieve_context(query):
    """
    Calls the retrieval script to get Quranic context based on the user query.
    """
    try:
        print("Retrieving context for query:", query)
        result = subprocess.run(
            ["python", "retrieve_context.py"],
            input=query + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8", 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error retrieving context: {e.stderr}"

@app.route("/generate-answer", methods=["POST"])
def generate_answer():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing question field"}), 400

    question = data["question"].strip()
    print("Received question:", question)
    context = retrieve_context(question)

    if "Error retrieving context" in context:
        return jsonify({"error": context}), 500

    # Construct prompt
#     prompt = f"""Using only the following Quranic context, answer the question below.
# Your answer must be entirely based on this context and provided in both English and Arabic.

# Quranic Context:
# {context}

# Question: {question}

# Answer (English and Arabic):"""
    prompt = f"""Using only the following Quranic context, answer the question below.
    Your response must be strictly based on the provided context. If the context does not contain relevant information, respond with: 
    "I do not have sufficient information from the Quran to answer this question."

    Ensure the answer is provided in both English and Arabic.

    Quranic Context:
    {context}

    Question: {question}

    Answer:"""


    # Initialize Gemini model
    # model = genai.GenerativeModel("gemini-1.5-flash")
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Generate answer
    response = model.generate_content(prompt)

    return jsonify({"question": question, "context": context, "answer": response.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
