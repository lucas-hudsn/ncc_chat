import os
import uuid
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_parent_child_chunks(documents: list[Document], parent_chunk_size: int = 2000, child_chunk_size: int = 400):
    """
    Applies a parent-child chunking strategy to a list of documents.

    This function splits documents first into larger "parent" chunks, and then
    each parent chunk is split into smaller "child" chunks. The child chunks
    are what you would typically embed and store in a vector database. The parent
    chunks are stored separately and retrieved alongside the relevant child chunks
    to provide more context to the LLM.

    Args:
        documents (list[Document]): A list of LangChain Document objects, as loaded
                                    by a loader like PyPDFDirectoryLoader.
        parent_chunk_size (int): The character size for the parent chunks.
        child_chunk_size (int): The character size for the child chunks.

    Returns:
        tuple[list[Document], list[Document]]: A tuple containing two lists:
                                               - The first list contains the parent documents.
                                               - The second list contains the child documents.
    """
    # Initialize text splitters
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=parent_chunk_size)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=child_chunk_size)

    all_parent_docs = []
    all_child_docs = []

    # Split the initial documents into parent chunks
    parent_chunks = parent_splitter.split_documents(documents)
    print(f"Created {len(parent_chunks)} parent chunks.")

    # Iterate through each parent chunk to create child chunks
    for parent_chunk in parent_chunks:
        # Generate a unique ID for the parent chunk
        parent_id = str(uuid.uuid4())
        parent_chunk.metadata["parent_id"] = parent_id
        all_parent_docs.append(parent_chunk)

        # Split the content of the parent chunk into child chunks
        child_content_chunks = child_splitter.split_text(parent_chunk.page_content)

        # Create child Document objects, inheriting metadata from the parent
        for child_content in child_content_chunks:
            # The child document inherits all metadata from its parent
            child_doc = Document(
                page_content=child_content,
                metadata=parent_chunk.metadata.copy() # Use .copy() to avoid metadata mix-ups
            )
            all_child_docs.append(child_doc)

    print(f"Created {len(all_child_docs)} child chunks from {len(all_parent_docs)} parent chunks.")

    return all_parent_docs, all_child_docs
