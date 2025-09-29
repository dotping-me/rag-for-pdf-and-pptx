from typing import Optional
import webview, json, os

class App:
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.static_dir: str = os.path.join(os.path.dirname(__file__), "public")

    # API Layer
    def api_hello_world(self, username: str) -> str:
        return json.dumps({ "message": f"Hello {username}!" })

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
            self.window.expose(self.api_hello_world)
            webview.start(debug = True)

if __name__ == "__main__":
    app: App = App()
    app.run()