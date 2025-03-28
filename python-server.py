from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# # OpenAI API key (Uncomment if using OpenAI)
# # openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load FAISS index and Quranic verses once at startup
print("Loading FAISS index and Quranic verses...")
index = faiss.read_index("quran_index.faiss")

with open("quran_verses.pkl", "rb") as f:
    verses = pickle.load(f)

# Load Sentence Transformer model once at startup
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("Model and FAISS index loaded successfully.")


def retrieve_context(query):
    """
    Retrieves relevant Quranic verses based on the given query using FAISS.
    """
    try:
        print("Retrieving context for query:", query)
        query_embedding = model.encode([query], convert_to_numpy=True)
        distances, indices = index.search(query_embedding, 3)  # Retrieve top 3 matches
        results = [verses[i] for i in indices[0]]

        return "\n".join(results)

    except Exception as e:
        print(f"Error retrieving context: {e}")
        return f"Error retrieving context: {str(e)}"


@app.route("/generate-answer", methods=["POST"])
def generate_answer():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing question field"}), 400

    question = data["question"].strip()
    history = data.get("history", [])  # Get conversation history (default empty list)

    print("Received question:", question)
    print("Conversation History:", history)

    context = retrieve_context(question)

    if "Error retrieving context" in context:
        return jsonify({"error": context}), 500

    # Format conversation history (last 5 Q&A)
    history_text = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in history[-5:]])

    
    prompt2 = f"""Answer the user's question using the retrieved Quranic context and the previous conversation history. Determine if the user's question is a follow-up question. If it is (e.g., if it contains phrases like "explain in detail", "elaborate", "I don't understand", "in simple words", etc.), then base your answer on the previous answer in the conversation history, expanding or clarifying that response. If the question introduces a new topic that is not clearly a follow-up, then use the retrieved Quranic context to answer.

Guidelines:
- If the Quranic context contains relevant information, use it to answer thoughtfully.
- For follow-up questions, use both the previous conversation history (especially the last answer) and the Quranic context to provide additional details.
- If neither the Quranic context nor the conversation history provide sufficient information, respond with:
  "No information related to this could be found in the Quran."
- Do not speculate, provide personal opinions, or go beyond the given references.
- Ensure the response remains respectful, avoiding controversial or offensive statements.
- Provide the answer once in English and once in Arabic.

**Previous Conversation History:**  
{history_text}  

**Quranic Context:**  
{context}  

**User's Question:**  
{question}  

**Answer:**  
**English:**  

**Arabic:**  
"""



    # Use Gemini (Default)
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt2)
    answer = response.text

     # Option 2: Use OpenAI GPT-4o mini 
     # response = openai.ChatCompletion.create(
     #         model="gpt-4o-mini",  # Use "gpt-4o" or "gpt-3.5-turbo"
     #         messages=[{"role": "system", "content": "You are an AI Quranic assistant."},
     #                   {"role": "user", "content": prompt}],
     #         temperature=0.7,
     #         max_tokens=500
     #     )
     # answer = response["choices"][0]["message"]["content"].strip()

    return jsonify({"question": question, "context": context, "answer": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
