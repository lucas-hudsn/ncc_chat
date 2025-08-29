# NCC 2022 RAG Building Advisor

## Background

This project was created to address a common challenge faced by architects and construction professionals in Australia: quickly and accurately finding relevant information within the National Construction Code (NCC). My partner, an architect, often expressed frustration with the difficulty of navigating the dense and complex NCC documents to get timely advice.

This application is a learning project that demonstrates how to build a Retrieval-Augmented Generation (RAG) system to make the NCC more accessible. It uses a Flask web framework for the frontend and a parent-child chunking strategy to improve the quality of the retrieved information.

## How it Works

The application works in the following steps:

1.  **Data Ingestion:** The application first ingests the NCC 2022 Volumes 1, 2, and 3 in PDF format.
2.  **Parent-Child Chunking:** To improve the relevance of the retrieved context, the documents are split into two levels of chunks:
    * **Parent Chunks:** Larger, more general chunks of text (e.g., 2000 characters).
    * **Child Chunks:** Smaller, more specific chunks derived from the parent chunks (e.g., 400 characters).
3.  **Vectorization:** The child chunks are then converted into numerical representations (embeddings) using a sentence transformer model and stored in a Chroma vector database. The parent chunks are stored separately.
4.  **Retrieval:** When a user asks a question, the application queries the vector database to find the most relevant child chunks.
5.  **Context Augmentation:** The application then retrieves the parent chunks associated with the top-ranked child chunks. This provides a broader and more complete context for the language model.
6.  **Generation:** Finally, the user's question and the retrieved parent chunks are passed to a Large Language Model (LLM), which generates a human-readable answer.

## How to Run the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download the NCC 2022 PDFs:**
    * Create a directory named `ncc_pdfs`.
    * Download the NCC 2022 Volumes 1, 2, and 3 from the [official ABCB website](https://ncc.abcb.gov.au/editions/ncc-2022).
    * Place the downloaded PDF files in the `ncc_pdfs` directory.
4.  **Run the Gradio application:**
    ```bash
    python app.py
    ```
5.  **Open your web browser** and navigate to `http://127.0.0.1:7860`.

## Copyright and Distribution Advice

**This project is for educational and demonstrative purposes only.**

The National Construction Code (NCC) is subject to copyright. The Australian Building Codes Board (ABCB) makes the NCC available under a **Creative Commons Attribution-NoDerivatives 4.0 International license**.

This means:

* **You are free to share** (copy and redistribute) the material in any medium or format.
* **You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* **You may not distribute the modified material.** If you remix, transform, or build upon the material, you may not distribute the modified material.

**Therefore, if you use or distribute this project, you must:**

* **Acknowledge the source of the NCC data:** The Australian Building Codes Board (ABCB).
* **Include the copyright notice:** "© Commonwealth of Australia and the States and Territories of Australia 2022, published by the Australian Building Codes Board."
* **Provide a link to the Creative Commons license:** [https://creativecommons.org/licenses/by-nd/4.0/](https://creativecommons.org/licenses/by-nd/4.0/)
* **Do not modify the NCC content itself.** This application uses the NCC content verbatim for retrieval and generation.

**Disclaimer:** This application is not a substitute for professional advice. Always consult with a qualified building professional for specific building and construction matters. The creators of this application are not liable for any errors or omissions in the information provided.
