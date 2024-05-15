from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function(local: bool) -> OllamaEmbeddings:
    """
    Returns an embedding function based on the specified configuration.

    Parameters:
        local (bool): Flag indicating whether to use local or remote embeddings.
            If True, local embeddings will be used. If False, remote embeddings
            will be used.

    Returns:
        OllamaEmbeddings: An instance of the embedding function based on the specified
            configuration.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings