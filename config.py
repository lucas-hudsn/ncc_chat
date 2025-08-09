import os

urls = {
         "NCC 2022 Volume One.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-one.pdf",
         "NCC 2022 Volume Two.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-two.pdf",
         "NCC 2022 Volume Three.pdf": "https://ncc.abcb.gov.au/system/files/ncc/ncc2022-volume-three.pdf"
    }
pdf_dir = "ncc_pdfs"
os.makedirs(pdf_dir, exist_ok=True)
persist_dir = "./chroma_db"  # Directory where your ChromaDB is stored
os.makedirs(persist_dir, exist_ok=True)
embedding_model_id = "all-MiniLM-L6-v2"
gemini_model_id  = "gemini-2.5-flash"