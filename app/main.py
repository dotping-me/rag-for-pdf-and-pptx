from typing import Any, Dict, Optional
import webview, json, os

class App:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.static_dir: str = os.path.join(os.path.dirname(__file__), "public")

    # API Layer
    def api_hello_world(self, username: str) -> str:
        return json.dumps({ "message": f"Hello {username}!" })

    def api_rag_service(self, json_obj: Dict[str, Any]) -> str:
        """
        Calls RAG service from backend

        Steps:
            1. Takes file input from user input (app)
            2. Stores file in backend buffer, I guess?
            3. Calls RAG service using CLI tooling
            4. Catches and returns JSON response
        """

        print(json_obj)
        return "" 

    def home(self):
        """ Serves index.html """

        self.window = webview.create_window(
            title = "Home",
            url = os.path.join(self.static_dir, "index.html"),
            width = 1200,
            height = 800,
        )

    def run(self):
        """ Runs App, duh... """
        
        self.home()

        # Exposes API layer
        if self.window:
            self.window.expose(self.api_rag_service)
            webview.start(debug = True)

if __name__ == "__main__":
    app: App = App()
    app.run()