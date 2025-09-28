# NOTE: This is just an MVP

from typing import Any
from markitdown import MarkItDown

def main() -> bool:
    """
    This is a proof of concept / MVP!
    
    Steps:
        1. Get filepath from user input
    """

    # 1. Get file from user input
    filepath: str = input("Enter filepath: ")
    file_ext: str = filepath[len(filepath) - filepath[::-1].index("."):]
    print(file_ext)

    mdConverter = MarkItDown()
    mdText: str = ""
    if file_ext in ["pdf", "pptx"]:
        print("Converting PDF to MD")
        
        mdText = mdConverter.convert(r"{}".format(filepath)).text_content
        with open("test.md", "w") as f:
            f.write(mdText)

    else:
        print("Unsupported File Format")
        return False
    
    print(mdText)
    return True

if __name__ == "__main__":
    main()