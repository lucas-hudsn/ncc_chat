
import os
import requests
from langchain_community.document_loaders import PyPDFDirectoryLoader


def download_ncc_pdfs(urls:dict, pdf_dir:str = "ncc_pdfs"):
    """
    Downloads the NCC 2022 PDFs from the ABCB website.
    In a real application, you would need to handle the download more robustly.
    For this example, we will assume the PDFs are already in the PDF_DIR.
    You can download them manually from: https://ncc.abcb.gov.au/editions/ncc-2022
    args:
        urls (dict): A dictionary containing the filenames and their corresponding URLs.
        pdf_dir (str): The directory where the PDFs will be saved.
    """
    
    print("Download the NCC 2022 Volumes 1, 2, and 3 PDFs and place them in the 'ncc_pdfs' directory.")
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    for filename, url in urls.items():
        if not os.path.exists(os.path.join(pdf_dir, filename)):
            print(f"Downloading {filename}...")
            response = requests.get(url)
            with open(os.path.join(pdf_dir, filename), "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}.")


def load_ncc_pdfs(urls:dict, pdf_dir:str = "ncc_pdfs"):
    """
    Load the NCC PDFs from the specified directory.
    If the PDFs are not present, it will download them.
    args:        
        urls (dict): A dictionary containing the filenames and their corresponding URLs.
        pdf_dir (str): The directory where the PDFs are stored.
    """
    if not os.path.exists(pdf_dir) or not os.listdir(pdf_dir):
        print("Downloading NCC PDFs.")
        download_ncc_pdfs(urls, pdf_dir=pdf_dir)
    
    print("Loading NCC PDFs from directory:", pdf_dir)
    loader = PyPDFDirectoryLoader(pdf_dir)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {pdf_dir}.")
    print(f"Example document metadata: {docs[0].metadata}, document content: {docs[0].page_content[:200]}")  # Print first 200 characters of the first document

    return docs

