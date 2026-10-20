import time
import random
from flask import Flask

app = Flask(__name__)

@app.get("/")
def get_products():
    # Simulate API processing delay for tracing visibility
    time.sleep(random.uniform(0.02, 0.08))
    return "Get All Products"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
