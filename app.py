from flask import Flask, request, render_template, jsonify
import socket
import os
import logging
import platform

app = Flask(__name__)


class PodInfo:
    def __init__(self, hostname, ip, namespace, uri, method, remote_addr):
        self.hostname = hostname
        self.ip = ip
        self.namespace = namespace
        self.uri = uri
        self.method = method
        self.remote_addr = remote_addr

    def to_dict(self):
        return {
            'hostname': self.hostname,
            'ip': self.ip,
            'namespace': self.namespace,
            'uri': self.uri,
            'method': self.method,
            'remote_addr': self.remote_addr
        }


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_namespace():
    try:
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def get_pod_info():
    hostname = platform.node()
    ip = get_ip()
    namespace = get_namespace()
    uri = request.path
    method = request.method
    remote_addr = request.remote_addr

    return PodInfo(hostname, ip, namespace, uri, method, remote_addr)


@app.route('/')
def handle_request():
    info = get_pod_info()
    background_color = os.environ.get('BACKGROUND_COLOR', '#fff')

    try:
        return render_template('index.html',
                               info=info,
                               background_color=background_color)
    except Exception as e:
        logging.error("Error rendering template:", e)
        response = "Error rendering template"

    return response


@app.route('/json')
def handle_json_request():
    try:
        info = get_pod_info()
        return jsonify(info.to_dict())
    except Exception as e:
        logging.error("Error handling JSON request:", e)
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    logging.info("Starting server on port %d", 8080)
    app.run(port=8080)
