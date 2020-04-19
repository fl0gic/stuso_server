# Caden Kriese - 4/19/20
"""
Base app file for running the server application.
"""
from server import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
