## Running Ollama and Chromadb

To further enhance your development process and focus on the core functionalities of the assignment, you can run Ollama and Chromadb. These tools provide additional features and optimizations.

1. Install Ollama by following the instructions in the [Ollama documentation](https://ollama.readthedocs.io/en/latest/installation.html).

2. Install Chromadb by following the instructions in the [Chromadb documentation](https://chromadb.readthedocs.io/en/latest/installation.html).

3. Once Ollama and Chromadb are installed, you can use the following commands to run the project:

    - To populate the database using Ollama:<br>
    `docker run -p 11434:11434 -it --rm rag-demo python populate_database.py --use-ollama`

    - To query the database using Ollama: <br>
    `docker run -p 11434:11434 -it --rm rag-demo python query_data.py --use-ollama "{query}"`

    - To reset the database using Ollama: <br>
    `docker run -p 80:80 -it --rm rag-demo python populate_database.py --reset --use-ollama`

    Note: Make sure to replace `{query}` with your actual query.


