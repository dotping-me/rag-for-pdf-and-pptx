# NOTE: This is just an MVP

from typing import Any, List
from markitdown import MarkItDown

import re

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

        # HACKJOB: "<!-- Slide 1 -->" is set by default
        lines: List[str] = mdText.split("\n")
        for i, ln in enumerate(lines):
            if "<!-- Slide number:" in ln:
                lines[i] = "Slide " + ln[18: ln.index(">") - 2] + "\n---\n"

        mdText = "\n".join(i for i in lines)
        with open("test.md", "w") as f:
            f.write(mdText)

    else:
        print("Unsupported File Format")
        return False
    
    print(mdText)
    return True

if __name__ == "__main__":
    main()