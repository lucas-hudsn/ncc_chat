from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def save_to_database(documents: list, embedding_model_id: str = "sentence-transformers/all-MiniLM-L6-v2", persist_directory="chroma_db"):
    """
    Saves the processed documents to a Chroma database with embeddings.
    
    Args:
        documents (list): A list of Document objects to be saved.
        embedding_model_id (str): The ID of the embedding model to use.
    """
    print("Saving documents to Chroma database...")

    # Initialize the embedding model
    embeddings = SentenceTransformerEmbeddings(model_name=embedding_model_id)
    
    # Create a Chroma vector store
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)
    
    print("Documents saved successfully to Chroma database.")
    print(f"Total documents saved: {len(documents)}")   