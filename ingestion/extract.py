
import os
from langchain_community.document_loaders import UnstructuredURLLoader

def get_online_data(urls: list):
    """
    For each URL in the list, loads the text content of the associated web pages,
    and returns the text and metadata as Document objects.
    Args:
        urls (list): A list of URLs to download the PDF files from.
    """

    print(f"Attempting to download from:\n - {'\n - '.join(urls)}")

    try:
        loader = UnstructuredURLLoader(urls=urls)
        documents = loader.load()
        print(f"Extracted {len(documents)} documents downloaded from the provided URLs.")
        return documents
    
    except Exception as e:
        print(f"Error downloading or saving PDF from the urls provided {e}")

    
