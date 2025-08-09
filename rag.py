import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import pipeline
from langchain.prompts import PromptTemplate
import pickle
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.llms import HuggingFacePipeline

# --- 1. Configuration ---
# Define the paths and model names
CHROMA_DB_PATH = "./chroma_db"  # Directory where your ChromaDB is stored
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LOCAL_LLM_NAME  = "HuggingFaceTB/SmolLM3-3B" # The model you downloaded with Ollama

def rag_pipeline(question):
    """
    Main function to run the local RAG pipeline.
    """
    # --- 2. Load the Vector Database ---
    print("Loading vector database...")


    try:
        embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_function
        )
        with open(os.path.join(CHROMA_DB_PATH, "parent_chunks.pkl"), "rb") as f:
            parent_chunks = pickle.load(f)

        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        def retrieve_context(query):
            """
            Retrieve relevant context from the vector store based on the question.
            """
            retrieved_docs = retriever.get_relevant_documents(query)

            parent_ids = {doc.metadata["parent_id"] for doc in retrieved_docs}
            context_docs = [p for p in parent_chunks if p.metadata["parent_id"] in parent_ids]
            context = "\n\n".join([doc.page_content for doc in context_docs])
            return context

        print("Vector database loaded successfully.")
    except Exception as e:
        print(f"Error loading vector database: {e}")
        print(f"Please ensure you have a ChromaDB at '{CHROMA_DB_PATH}' and it was created with the '{EMBEDDING_MODEL_NAME}' model.")
        return

    # --- 3. Initialize the Local LLM ---
    print(f"Initializing local LLM: {LOCAL_LLM_NAME}...")
    try:

        hf_pipeline = pipeline("text-generation", model=LOCAL_LLM_NAME)
        # Test the LLM connection
        llm = HuggingFacePipeline(pipeline=hf_pipeline)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return

    # --- 4. Define the RAG Prompt Template ---
    # This template structures how the context and question are passed to the LLM
    template = """
    You are an expert in Australian Construction Code. Use the following context, provided from the NCC website, to answer the user's question.
    Please refer direcly to the context provided, and do not make assumptions or provide information outside of it.
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
        {"context": retrieve_context, "question": RunnablePassthrough()}
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
        question = "Describe a class 2 building"
        rag_pipeline(question)
