
from flask import Flask
import time
import random

app = Flask(__name__)

@app.route("/")
def home():
    time.sleep(random.uniform(0.1, 0.5))
    return "Hello! My Python application is running."

@app.route("/products")
def products():
    time.sleep(random.uniform(0.1, 0.5))
    return {"products": ["Laptop", "Mobile", "Keyboard"]}

@app.route("/health")
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
