# LLM RAG Assignment
## Running


1. Install Ollama by following the instructions in the [Ollama documentation](https://ollama.readthedocs.io/en/latest/installation.html).

2. Run Ollama with the following commands
`ollama run "phi3:latest` for the LLM model
`ollama run "nomic-embed-text"`for the embeddings model
2. Install Chromadb by following the instructions in the [Chromadb documentation](https://chromadb.readthedocs.io/en/latest/installation.html).

3. Once Ollama and Chromadb are installed, you can use the following commands to run the project:

    - To populate the database using Ollama:<br>
    `python populate_database.py`

    - To query the database using Ollama: <br><br>
    `python query_data.py "What are the latest Credit challenges for Amazon currently?"`
    

    - To reset the database<br>
    `python populate_database.py --reset`
---
>Additional Notes:
    - Embedding Model: The current embedding model being used is `nomic-embed-text`. You can utilize the `get_embedding_function.py` script to select different embedding models such as AWS Bedrock, Hugging Face, or OpenAI. The quality of the embeddings directly impacts the retrieval accuracy. <br>
    - Vector Store: Chroma is being utilized as the vector store for local development due to time constraints. However, any other vector store supported by Langchain community can be used.


