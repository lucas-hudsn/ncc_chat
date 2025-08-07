# main.py
from extract import get_online_data
from transform import create_chunks
from load import save_to_database

#from load import save_to_database

def run_etl_pipeline(urls, embedding_model_id, persist_directory):
    # 1. Extract
    raw_data = get_online_data(urls)
    
    # 2. Transform
    processed_data = create_chunks(raw_data)
    
    # 3. Load
    save_to_database(processed_data, embedding_model_id, persist_directory)
    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    
    urls = [
        "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-one.pdf",
        "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-two.pdf",
        "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-three.pdf"
    ]

    embedding_model_id = "sentence-transformers/all-MiniLM-L6-v2"
    persist_directory="chroma_db"
    
    run_etl_pipeline(urls, embedding_model_id, persist_directory)


