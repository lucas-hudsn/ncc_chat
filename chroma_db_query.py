from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def query_chroma_db(prompt, chroma_db_path, embeddings_model_name, top_k=5):
    # Load embeddings model
    embeddings = SentenceTransformerEmbeddings(model_name=embeddings_model_name)
    # Load Chroma DB
    db = Chroma(persist_directory=chroma_db_path, embedding_function=embeddings)
    # Query for most similar documents
    results = db.similarity_search(prompt, k=top_k)
    # Output results
    for i, doc in enumerate(results, 1):
        print(f"{i}. File: {doc.metadata.get('source', 'Unknown')}")
        print(f"   Content: {doc.page_content[:200]}...\n")

    return results

if __name__ == "__main__":
    embeddings_model_name = "all-MiniLM-L6-v2"  # Local Sentence-BERT model
    chroma_db_output_path = "ncc_chroma_db"  # Path to store Chroma DB
    prompt = "fire safety requirements for buildings"
    query_chroma_db(prompt, chroma_db_output_path, embeddings_model_name)