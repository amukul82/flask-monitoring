from flask import Flask, request, Response, jsonify
from prometheus_client import multiprocess, Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
 
my_counter = Counter(
    'my_counter', 'A basic counter.',
    ['app_name']
)

request_count = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)


def record_request_data(response):
    request_count.labels(app_name='flask_app', method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    return response


def setup_metrics(app):
    app.after_request(record_request_data)

app = Flask(__name__)
setup_metrics(app)


@app.route("/")
@app.route("/hello")
def hello():
    return "hello"


@app.route("/error")
def error():
    return "error", 500


# Expose metrics.
@app.route("/metrics", methods=['GET'])
def metrics():
    my_counter.labels('flask_app').inc()
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
 

if __name__ == "__main__":
    app.run()