from flask import Flask, request, jsonify, render_template
from rag import rag_pipeline


# --- Flask App Initialization ---
app = Flask(__name__)

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """
    Handles the user's question, retrieves relevant context,
    and generates an answer.
    """
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided."}), 400

    # --- RAG Pipeline ---
    try:
        llm_response = rag_pipeline(query)
        return jsonify({"answer": llm_response, "context": query})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':   
    app.run(debug=True)
