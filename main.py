import os
import time
import random

from flask import Flask

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# 1. Resource: how this service appears in Jaeger
resource = Resource.create({"service.name": "products-api"})

# 2. Exporter: where spans are sent (collector on the node, OTLP/HTTP)
collector_ip = os.getenv("COLLECTOR_IP", "localhost")
exporter = OTLPSpanExporter(endpoint=f"http://{collector_ip}:4318/v1/traces")

# 3. Provider + batch processor
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# 4. Flask app, auto-instrumented (one span per request)
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

tracer = trace.get_tracer(__name__)


@app.route("/")
def home():
    time.sleep(random.uniform(0.1, 0.5))
    return "Hello! My Python application is running."


@app.route("/products")
def products():
    # custom child span, visible inside the request trace
    with tracer.start_as_current_span("fetch-products"):
        time.sleep(random.uniform(0.1, 0.5))
    return {"products": ["Laptop", "Mobile", "Keyboard"]}


@app.route("/health")
def health():
    return {"status": "UP"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
