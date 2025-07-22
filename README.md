# NCC Code Bot: Learning AI Engineering with Architectural Data

## Project Overview

This project is my personal endeavor to transition from a Data Scientist role into the field of AI Engineering. The idea for this project came from my partner, an architect, who frequently navigates the dense and complex National Construction Code (NCC). The core concept is to build a chatbot/information aggregation system that can make the vast amount of NCC code information more accessible and easily queryable.

**This project is purely for learning, development, and personal exploration.** It is designed as a hands-on exercise to understand the practical aspects of building AI-powered applications, particularly focusing on Retrieval-Augmented Generation (RAG) principles and vector databases.

## Motivation & Learning Goals

As a Data Scientist, I've worked extensively with data analysis, machine learning models, and predictive analytics. AI Engineering, however, brings a new set of challenges and skills related to deploying, maintaining, and scaling AI systems, especially those that leverage large language models (LLMs) and vector databases.

My key learning goals for this project include:

* **Data Ingestion & Preprocessing:** Mastering the extraction of structured and unstructured data from complex documents like PDFs.
* **Text Chunking Strategies:** Understanding how to effectively break down large texts into manageable "chunks" for optimal retrieval.
* **Embeddings & Vector Databases:** Gaining practical experience with creating and utilizing text embeddings, and storing them efficiently in vector databases (specifically ChromaDB).
* **Retrieval-Augmented Generation (RAG) Fundamentals:** Building a system that can retrieve relevant information from a knowledge base before generating responses with an LLM (though LLM integration is a future, optional phase).
* **API Integration & System Design:** Thinking about how different components of an AI system fit together and interact.
* **Finetuning Language Models** Exploring the viability of fine tuning Open Source models and comparing the results to a RAG system for more complex guidance on the code.

## Project Structure & Components

This project is built incrementally, focusing on modularity.

### Core Components Implemented So Far:

1.  **PDF Downloader (`download_ncc.py`):**
    * **Purpose:** Programmatically fetches the complete NCC series ZIP file from the ABCB website.
    * **Functionality:** Downloads the ZIP, extracts PDF volumes, and saves them to a local directory (e.g., `NCC_PDFs`).
3.  **PDF to ChromaDB Embedder (`embed_ncc.py`):**
    * **Purpose:** The core ingestion pipeline.
    * **Functionality:**
        * Reads specified NCC PDF volumes.
        * Chunks the PDFs page by page (each page becomes a separate document).
        * Utilizes a local `HuggingFaceEmbeddings` model (`all-MiniLM-L6-v2`) to convert page content into numerical vectors (embeddings).
        * Stores these embeddings and the corresponding text content in a persistent [Chroma](https://www.trychroma.com/) vector database (saved to `ncc_chroma_db` by default).
4.  **ChromaDB Query Tool (`query_ncc_db.py`):**
    * **Purpose:** To test the retrieval capabilities of the embedded data.
    * **Functionality:**
        * Loads the previously saved ChromaDB.
        * Takes a user query.
        * Performs a vector similarity search to find the most relevant NCC pages based on the query.
        * Displays snippets of the retrieved content, along with source file and page number.

### Technologies Used:

* **Python 3.x**
* **`requests`**: For downloading files from the web.
* **`zipfile`**: For handling ZIP archives.
* **`os`**: For file system operations.
* **`pypdf` (or `PyPDF2`)**: For robust PDF reading and parsing.
* **`langchain`**: A framework for developing applications powered by LLMs, used here for document loading, embeddings integration, and vector store management.
* **`langchain-community`**: Contains various integrations for LangChain.
* **`langchain-chroma`**: The specific integration for ChromaDB with LangChain.
* **`chromadb`**: The open-source vector database used for storing and querying embeddings.
* **`sentence-transformers`**: Provides the local embedding model (`all-MiniLM-L6-v2`).
* **`pycryptodome`**: Essential for handling encrypted PDF files, which some NCC versions might be.

## How to Get Started (For My Future Self)

1.  **Clone this repository:** (Once it's in a repo)
    `git clone [your-repo-url]`
    `cd ncc-code-buddy`
2.  **Set up a virtual environment** (recommended):
    `python -m venv venv`
    `source venv/bin/activate` (on Linux/macOS)
    `.\venv\Scripts\activate` (on Windows)
3.  **Install dependencies:**
    `pip install -r requirements.txt` (or manually with `pip install pypdf requests zipfile langchain langchain-community langchain-chroma sentence-transformers chromadb pycryptodome`)
4.  **Download NCC PDFs:**
    * Run `python download_ncc.py`.
    * **IMPORTANT:** You will need to manually find and input the direct download URL for the "Complete Series" ZIP file from the ABCB website ([https://ncc.abcb.gov.au/editions-national-construction-code](https://ncc.abcb.gov.au/editions-national-construction-code)). Right-click the download link and select "Copy Link Address."
    * This will create an `NCC_Pdfs` directory with your extracted NCC volumes.
5.  **Embed PDFs into ChromaDB:**
    * Run `python embed_ncc.py`.
    * When prompted, enter the exact filenames of your NCC volumes (e.g., `NCC 2022 Volume One.pdf,NCC 2022 Volume Two.pdf,NCC 2022 Volume Three.pdf`). Press Enter for default suggestions if applicable.
    * This will create a `ncc_chroma_db` directory containing your embedded data.
6.  **Query the Database:**
    * Run `python query_ncc_db.py`.
    * Enter your natural language questions about the NCC code.
    * The script will retrieve and display relevant sections.

## Future Enhancements (AI Engineering Horizons)

* **LLM Integration:** Connect the retrieved information to a large language model (LLM) (e.g., a local open-source LLM like Llama 3 via `ollama`, or an API-based LLM like OpenAI/Gemini) to generate coherent, conversational responses.
* **Improved Chunking:** Experiment with more sophisticated chunking strategies beyond just page-by-page (e.g., semantic chunking, fixed-size with overlap, recursive character splitting).
* **User Interface:** Develop a simple web-based UI (e.g., using Streamlit or Gradio) for a more interactive chatbot experience.
* **Error Handling & Robustness:** Enhance error handling for corrupted PDFs, network issues, and edge cases.
* **Metadata Utilization:** Leverage PDF metadata (e.g., chapters, sections) to improve search relevance.
* **Performance Optimization:** Optimize embedding generation and search for larger datasets.
* **Evaluation Metrics:** Establish metrics to evaluate the quality of retrieval and generated responses.

---

## Important Note on NCC Copyright

**The National Construction Code (NCC) is subject to copyright by the Commonwealth of Australia and the States and Territories of Australia, administered by the Australian Building Codes Board (ABCB).**

This project is developed strictly for **personal learning, non-commercial research, and educational purposes only.** The NCC content downloaded and processed within this project will **NOT be publicly distributed, shared, or used for any commercial applications.** All processing and storage of NCC data will remain solely on my local machine for the duration of this learning project. Appropriate measures will be taken to ensure the NCC data is not inadvertently exposed or shared.