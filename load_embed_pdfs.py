import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def load_and_embed_pdfs_to_chroma(pdf_filenames, pdf_directory="NCC_PDFs", embeddings_model_name="all-MiniLM-L6-v2", chroma_db_path="chroma_db"):
    """
    Loads specified PDF files, chunks them by page, generates embeddings,
    and saves them to a Chroma vector database.

    Args:
        pdf_filenames (list): A list of strings, where each string is the
                              filename of a PDF (e.g., ["volume_one.pdf", "volume_two.pdf"]).
        pdf_directory (str): The directory where the PDF files are located.
                             Defaults to "NCC_Pdfs".
        chroma_db_path (str): The path where the Chroma DB will be stored.
                              Defaults to "chroma_db".
    """
    all_pages = []
    print(f"--- Starting PDF Processing and Embedding ---")

    # 1. Load PDFs and Chunk by Page
    for filename in pdf_filenames:
        full_pdf_path = os.path.join(pdf_directory, filename)
        if not os.path.exists(full_pdf_path):
            print(f"Error: PDF file not found at '{full_pdf_path}'. Skipping.")
            continue

        print(f"Loading and chunking '{filename}' by page...")
        try:
            # PyPDFLoader loads each page as a separate document (chunk)
            loader = PyPDFLoader(full_pdf_path)
            pages = loader.load()
            all_pages.extend(pages)
            print(f"  - Loaded {len(pages)} pages from '{filename}'.")
        except Exception as e:
            print(f"  - Failed to load '{filename}': {e}")

    if not all_pages:
        print("No PDF pages were successfully loaded. Exiting.")
        return

    print(f"\nTotal pages loaded across all PDFs: {len(all_pages)}")

    # 2. Initialize Embedding Model
    print("Initializing embedding model (this might take a moment the first time)...")
    # Using a local Sentence-BERT model (all-MiniLM-L6-v2)
    # This model is good for general purpose embeddings and runs locally.
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    print("Embedding model initialized.")

    # 3. Initialize Chroma DB
    print(f"Initializing Chroma DB at '{chroma_db_path}'...")
    # This will create the directory if it doesn't exist and persist the DB.
    # If the DB already exists, it will load it.
    vectorstore = Chroma.from_documents(
        documents=all_pages,
        embedding=embeddings,
        persist_directory=chroma_db_path
    )
    print(f"Chroma DB created/loaded and pages embedded.")
    print(f"You can now find the Chroma DB files in the '{chroma_db_path}' directory.")

   
if __name__ == "__main__":
    # List of PDF filenames to process
    pdf_filenames_list = [
        "ncc2022-volume-one-20230501b.pdf",
        "ncc2022-volume-two-20230501b.pdf",
        "ncc2022-volume-three20230501b.pdf"
    ]

    # Directory where your PDFs are stored (e.g., the one created by the first script)
    pdf_source_directory = "NCC_PDFs"

    # Directory where the Chroma DB will be saved
    chroma_db_output_path = "ncc_chroma_db"

    # Embeddings model name
    embeddings_model_name="all-MiniLM-L6-v2"

    # --- Run the function ---
    load_and_embed_pdfs_to_chroma(
        pdf_filenames=pdf_filenames_list,
        pdf_directory=pdf_source_directory,
        embeddings_model_name=embeddings_model_name,
        chroma_db_path=chroma_db_output_path,
    )