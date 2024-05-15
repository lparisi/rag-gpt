"""
This Python script is used to populate a Chroma database with documents loaded from a specified directory. 
The documents are split into smaller chunks and each chunk is added to the database with a unique ID.
"""
import argparse
import os
import shutil

from typing import List

from tqdm import tqdm

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    """
    Entry point of the script.
    
    This function checks if the database should be cleared using the `--reset` flag. If the flag is provided,
    it clears the database by calling the `clear_database` function. Then, it creates or updates the data store
    by loading documents, splitting them into chunks, and adding them to the chroma.
    """
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents() -> list[Document]:
    """
    Load documents from a specified directory.

    Returns:
        list: A list of loaded documents.
    """
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Splits a list of documents into smaller chunks using a text splitter.

    Args:
        documents (list[Document]): The list of documents to be split.

    Returns:
        List of split documents.

    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document])-> None:
    """
    Adds new documents to the Chroma database.

    Args:
        chunks (list[Document]): A list of Document objects representing the new documents to be added.

    Returns:
        None
    """
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []

    new_chunks = list(chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids)

    if len(new_chunks):
        print(f"👉 Adding new chunks of documents to database: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]

        for chunk in tqdm(new_chunks, desc="Adding chunks to database", unit="chunks"):
            db.add_documents([chunk], ids=[chunk.metadata["id"]])
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks: list[Document])-> list[Document]:
    """
    Calculate unique IDs for each chunk in a list of chunks.

    Args:
        chunks (list): A list of chunks.

    Returns:
        list: A list of chunks with unique IDs assigned to each chunk.
    """

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def generate_chunk_id(source: str, 
                      page: int, 
                      index: int
    ) -> str:
    """
    Generate a unique ID for a chunk.

    Returns:
        str: A unique ID.
    """
    return f"{source}:{page}:{index}"
def clear_database() -> None:
    """
    Clears the database by removing the CHROMA_PATH directory if it exists.

    This function deletes the CHROMA_PATH directory and all its contents if it exists.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
