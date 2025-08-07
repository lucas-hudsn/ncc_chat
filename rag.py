import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnablePassthrough

# --- 1. Configuration ---
# Define the paths and model names
CHROMA_DB_PATH = "./chroma_db"  # Directory where your ChromaDB is stored
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_LLM_NAME  = "Qwen/Qwen3-4B-Instruct-2507" # The model you downloaded with Ollama

def main(question):
    """
    Main function to run the local RAG pipeline.
    """
    # --- 2. Load the Vector Database ---
    print("Loading vector database...")
    try:
        embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_function
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks
        print("Vector database loaded successfully.")
    except Exception as e:
        print(f"Error loading vector database: {e}")
        print(f"Please ensure you have a ChromaDB at '{CHROMA_DB_PATH}' and it was created with the '{EMBEDDING_MODEL_NAME}' model.")
        return

    # --- 3. Initialize the Local LLM ---
    print(f"Initializing local LLM: {LOCAL_LLM_NAME}...")
    try:
        llm = pipeline("text-generation", model=LOCAL_LLM_NAME)
        # Test the LLM connection
        llm.invoke("Hello, are you running?")
        print("LLM initialized successfully.")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return

    # --- 4. Define the RAG Prompt Template ---
    # This template structures how the context and question are passed to the LLM
    template = """
    You are an expert in Australian Construction Code. Use the following context, provided from the NCC website, to answer the user's question.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    Provide a concise and helpful response.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # --- 5. Create the RAG Chain ---
    # This chain ties together the retriever, the prompt, and the LLM
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # --- 6. Ask a Question ---
    print("\n--- Ready to answer questions ---")
    

    print(f"\nQuerying the model with: '{question}'")
    try:
        # Invoke the chain with the question
        response = rag_chain.invoke(question)
        print("\n--- Model's Answer ---")
        print(response)
        print("----------------------\n")
    except Exception as e:
        print(f"An error occurred during chain invocation: {e}")


if __name__ == "__main__":
    # Check if the ChromaDB path exists
    if not os.path.exists(CHROMA_DB_PATH):
        print(f"Error: ChromaDB path not found at '{CHROMA_DB_PATH}'")
        print("Please run your data ingestion script first to create the vector database.")
    else:
        question = "What are the key fire safety requirements for commercial buildings?"
        main(question)
