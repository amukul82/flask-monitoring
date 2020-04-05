from flask import Flask, Response, jsonify
from prometheus_client import multiprocess, Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
 
app = Flask(__name__)
 
my_counter = Counter(
    'my_counter', 'A basic counter.',
    ['app_name']
)


@app.route("/")
def hello():
    return "hello"


# Expose metrics.
@app.route("/metrics", methods=['GET'])
def metrics():
    my_counter.labels('flask_app').inc()
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
 

if __name__ == "__main__":
    app.run()