# This is the project's entry point!

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_app.app.main import App

if __name__ == "__main__":
    app: App = App()
    app.run()