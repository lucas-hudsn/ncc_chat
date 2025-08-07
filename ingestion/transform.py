from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re
from sentence_transformers import SentenceTransformer


def create_chunks(documents: list[Document]):
    """
    This function is responsible for transforming the data from the NCC PDFs.
    It will read the PDF files, extract the text, and perform any necessary transformations
    to prepare the data for embedding or further processing.
    """
    print("Transforming NCC data...")
    
    # Initialize a text splitter to handle large documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    # Split the list of documents
    split_documents = text_splitter.split_documents(documents)
    print(f"Split into {len(split_documents)} chunks.")
    
    #Process each document
    print("Cleaning and processing text chunks...")
    cleaned_chunks = []
    for doc in split_documents:
        # Extract text content
        text = doc.page_content
        # Clean the text: remove excessive whitespace, newlines, etc.
        clean_text = re.sub(r'\s+', ' ', text).strip()
        # Add more cleaning steps if needed, e.g., regex for specific patterns
        cleaned_chunks.append(Document(page_content=clean_text, metadata=doc.metadata))

    print(f"Cleaned {len(cleaned_chunks)} text chunks.")

    return cleaned_chunks

    