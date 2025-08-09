import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
import pickle
from langchain.schema.runnable import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from config import persist_dir, embedding_model_id, gemini_model_id

def rag_pipeline(question):
    """
    Main function to run the local RAG pipeline.
    """
    print("Loading vector database...")

    try:
        embedding_function = HuggingFaceEmbeddings(model_name=embedding_model_id)
        vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_function
        )
        with open(os.path.join(persist_dir, "parent_chunks.pkl"), "rb") as f:
            parent_chunks = pickle.load(f)

        retriever = vector_store.as_retriever(search_kwargs={"k": 10})

        def retrieve_context(query):
            """
            Retrieve relevant context from the vector store based on the question.
            """
            retrieved_docs = retriever.invoke(query)

            parent_ids = {doc.metadata["parent_id"] for doc in retrieved_docs}
            context_docs = [p for p in parent_chunks if p.metadata["parent_id"] in parent_ids]
            context = "\n\n".join([doc.page_content for doc in context_docs])
            return context

        print("Vector database loaded successfully.")
    except Exception as e:
        print(f"Error loading vector database: {e}")
        print(f"Please ensure you have a ChromaDB at '{CHROMA_DB_PATH}' and it was created with the '{EMBEDDING_MODEL_NAME}' model.")
        return

    # Initialize LLM
    print(f"Initializing LLM: {gemini_model_id}...")
    try:
        model = ChatGoogleGenerativeAI(model=gemini_model_id)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return

    # Define the RAG Prompt Template 
    template = """
    You are an expert in Australian Construction Code. Use the following context, provided from the NCC website, to answer the user's question.
    Please refer direcly to the context provided, and do not make assumptions or provide information outside of it.
    Provide a concise and helpful response.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # This chain ties together the retriever, the prompt, and the LLM
    rag_chain = (
        {"context": retrieve_context, "question": RunnablePassthrough()}
        | prompt
        | model
    )

    print(f"\nQuerying the model with: '{question}'")
    try:
        # Invoke the chain with the question
        response = rag_chain.invoke(question)
        return response.content
    
    except Exception as e:
        print(f"An error occurred during chain invocation: {e}")


if __name__ == "__main__":

    # Check if the ChromaDB path exists
    if not os.path.exists(persist_dir):
        print(f"Error: ChromaDB path not found at '{persist_dir}'")
        print("Please run your data ingestion script first to create the vector database.")
    else:
        question = "How do I convert a class 3 building to a class 4?"
        response = rag_pipeline(question)
        print(response)
