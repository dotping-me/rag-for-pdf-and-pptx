# TODO: Break file into modules
# TODO: Setup args parsing (CLI tooling)

from typing import List, Tuple, Optional

# For loading documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader

# For embeddings and vector database
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma

import argparse, shutil, os

CHORMA_PATH: str = "chroma_db"

def load_document(filepath: str) -> Optional[List[Document]]:
    """
    Step 1: Getting file contents and loading them into a document
    """

    if (not filepath) or (not isinstance(filepath, str)):
        return

    file_ext: str = filepath[len(filepath) - filepath[::-1].index("."):]
    if file_ext == "pdf":
        print("Converting PDF to MD")
        loader = PyPDFLoader(filepath)

    elif file_ext == "pptx":
        print("Converting PPTX to MD")
        loader = UnstructuredPowerPointLoader(filepath)

    else:
        print("Unsupported File Format")
        return

    docs: List[Document] = loader.load()
    return docs

def chunk_doc(docs: List[Document]) -> Optional[List[Document]]:
    """
    Step 2: Split documents into smaller chunks
    """
    
    try:
        return RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 500,
            length_function = len,
            add_start_index = True
        ).split_documents(docs)
    
    except Exception as E:
        pass

    return

def query_vector_db():
    pass

def main():
    """
    This is a proof of concept / MVP!
    
    Steps:
        1. Get documents from user input (filepath)
        2. Split files into chunks
        3. Create and store embeddings in a vector database
        4. Query vector database
    """

    # 1. Get file from user input
    filepath: str = input("Enter filepath: ")
    doc = load_document(filepath)
    
    if not doc:
        return
    
    # 2. Split document into chunks
    chunks = chunk_doc(doc)
    if not chunks:
        return
    
    # 3. Create and store embeddings in a vector database
    if os.path.exists(CHORMA_PATH):
        shutil.rmtree(CHORMA_PATH)

    db = Chroma.from_documents(doc, SentenceTransformerEmbeddings(), persist_directory = CHORMA_PATH)
    db.persist()
    print(f"Saved {len(chunks)} Embeddings to Chroma Vector DB [{CHORMA_PATH}]")

    # 4. Query vector database
    results: List[Tuple[Document, float]] = db.similarity_search_with_relevance_scores("What functions manipulate strings?", k = 3)
    for matching_chunk, score in results:
        print(matching_chunk.page_content, score)

if __name__ == "__main__":
    main()