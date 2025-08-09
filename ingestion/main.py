# main.py
from extract import load_ncc_pdfs
from transform import create_parent_child_chunks
from load import save_to_database

#from load import save_to_database

def run_etl_pipeline(urls, embedding_model_id, persist_directory, pdf_dir):
    # Extract
    pdf_docs = load_ncc_pdfs(urls, pdf_dir)
    
    # Transform
    parent_chunks, child_chunks = create_parent_child_chunks(pdf_docs)
    
    # Load
    save_to_database(parent_chunks, child_chunks, embedding_model_id, persist_directory)
    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    
    urls = {
         "NCC 2022 Volume One.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-one.pdf",
         "NCC 2022 Volume Two.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-two.pdf",
         "NCC 2022 Volume Three.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-three.pdf"
    }

    embedding_model_id = "all-MiniLM-L6-v2"
    persist_directory="chroma_db"
    pdf_dir="ncc_pdfs"
    
    run_etl_pipeline(urls, embedding_model_id, persist_directory, pdf_dir)


