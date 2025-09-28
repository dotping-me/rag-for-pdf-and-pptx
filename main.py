# NOTE: This is just an MVP

from typing import Any, List
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader

def main() -> bool:
    """
    This is a proof of concept / MVP!
    
    Steps:
        1. Get filepath from user input
        2. Tokenize and create embeddings
    """

    # 1. Get file from user input
    filepath: str = input("Enter filepath: ")
    file_ext: str = filepath[len(filepath) - filepath[::-1].index("."):]

    if file_ext == "pdf":
        print("Converting PDF to MD")
        loader = PyPDFLoader(filepath)

    elif file_ext == "pptx":
        print("Converting PPTX to MD")
        loader = UnstructuredPowerPointLoader(filepath)

    else:
        print("Unsupported File Format")
        return False
    
    data: Any = loader.load()
    print(data)

    return True

if __name__ == "__main__":
    main()