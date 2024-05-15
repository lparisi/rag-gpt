from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings


def get_embedding_function(local: bool = True):
    
    if local is False:
        embeddings = BedrockEmbeddings(
            credentials_profile_name="default", region_name="us-east-1"
        )
    else:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings
