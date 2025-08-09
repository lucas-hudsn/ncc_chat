from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def save_to_database(parent_chunks: list, child_chunks: list, embedding_model_id: str = "all-MiniLM-L6-v2", persist_directory="chroma_db"):
    """
    Saves the processed documents to a Chroma database with embeddings.
    
    Args:
        documents (list): A list of Document objects to be saved.
        embedding_model_id (str): The ID of the embedding model to use.
    """
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("Vector store already exists. Skipping processing.")
        return
    print("Creating vector store...")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_id)
    vectorstore = Chroma.from_documents(
        documents=child_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()

    # We will also store the parent chunks for later retrieval
    # In a real application, you would use a more robust storage solution like a database.
    import pickle
    with open(os.path.join(persist_directory, "parent_chunks.pkl"), "wb") as f:
        pickle.dump(parent_chunks, f)

    print("Vector store created successfully.")
