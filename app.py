import gradio as gr
from rag import rag_pipeline

def ask(query):
    if not query:
        return "No query provided."
    try:
        llm_response = rag_pipeline(query)
        return llm_response
    except Exception as e:
        return f"Error: {str(e)}"

iface = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(lines=2, placeholder="Ask your question here..."),
    outputs="text",
    title="RAG Chatbot",
    description="Ask a question and get an answer using the RAG pipeline."
)

if __name__ == '__main__':
    iface.launch()
