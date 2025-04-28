from flask import Flask
from controllers.blog_controller import BlogController
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Initialize and register the BlogController
blog_controller = BlogController(app)

if __name__ == "__main__":
    app.run(debug=True)