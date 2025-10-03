from typing import Any, List, Dict, Optional
import webview, json, os

from ..services.main import test

class App:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.__static_dir: str = os.path.join(os.path.dirname(__file__), "public")
        self.__upload_dir: str = os.path.join(os.path.dirname(__file__), "../services/uploads")

        os.makedirs(self.__upload_dir, exist_ok = True) # Creates upload directory if it doesn't exist

    # API Layer
    def api_rag_load_doc(self, json_obj: Dict[str, Any]) -> str:
        """
        Calls RAG service from backend

        Steps:
            1. Takes file input from user input (app)
            2. Stores file in backend buffer, I guess?
            3. Calls RAG service using CLI tooling
            4. Catches and returns JSON response
        """

        if not json_obj:
            return json.dumps({ "error": "No input parsed" })

        # 1.1 Catching inputs
        filename: str = json_obj["name"]
        file_bytes: List[int] = json_obj["bytes"]

        # 1.2 Validates file input
        file_ext: str = filename.split(".")[-1]
        if file_ext not in ["pdf", "pptx"]:
            return json.dumps({ "error": "Invalid file format!" })

        # 2. Store the file
        try:
            store_fpath: str = os.path.join(self.__upload_dir, filename)
            with open(store_fpath, "wb") as f:
                f.write(bytes(file_bytes))

        except Exception as E:
            print(E.__class__.__name__, E)
            return json.dumps({ "error": "Could not save file for processing" })        

        # 3. Calls RAG service to embed document

        print(f"File '{filename}' received! ({len(file_bytes)} bytes)")
        return json.dumps({ "message": test() })

    def home(self):
        """ Serves index.html """

        self.window = webview.create_window(
            title = "Home",
            url = os.path.join(self.__static_dir, "index.html"),
            width = 720,
            height = 480,
        )

    def run(self):
        """ Runs App, duh... """
        
        self.home()

        # Exposes API layer
        if self.window:
            self.window.expose(self.api_rag_load_doc)
            webview.start(debug = True)

if __name__ == "__main__":
    app: App = App()
    app.run()