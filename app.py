# app.py
# This file contains the main Flask application.

from flask import Flask, request, jsonify
from model import RAG_Pipeline

# Initialize the Flask application
app = Flask(__name__)

# --- API Endpoint ---
# This defines the /ask endpoint which accepts POST requests.
@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Receives a question in a JSON payload, passes it to the RAG_Pipeline,
    and returns the answer.
    """
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Get the JSON data from the request
    data = request.get_json()
    question = data.get('question')

    # Validate that a 'question' was provided
    if not question:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    try:
        # Call the RAG pipeline with the user's question
        print(f"Received question: {question}")
        answer = RAG_Pipeline(question)
        print(f"Generated answer: {answer}")

        # Return the answer in a JSON response
        return jsonify({"answer": answer})

    except Exception as e:
        # Handle any potential errors during the pipeline execution
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

# --- Main execution block ---
if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 (accessible externally) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
