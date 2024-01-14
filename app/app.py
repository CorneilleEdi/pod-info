import time

from flask import Flask, request, render_template, jsonify
import socket
import os
import logging
import kubernetes as k
import platform

GIVEN_NAMESPACE = os.environ.get("namespace", "default")

app = Flask(__name__)


class PodInfo:
    def __init__(self, nodeName, podName, namespace, status, pod_ip):
        self.nodeName = nodeName
        self.podName = podName
        self.namespace = namespace
        self.status = status
        self.pod_ip = pod_ip

    def to_dict(self):
        return {
            'nodeName': self.nodeName,
            'podName': self.podName,
            'namespace': self.namespace,
            'status': self.status,
            'pod_ip': self.pod_ip,
        }


def get_pod_info():
    # Load the in-cluster Kubernetes configuration
    k.config.load_incluster_config()

    # Create the CoreV1Api object
    v1 = k.client.CoreV1Api()

    # Get the pod object
    pod = v1.read_namespaced_pod(name=platform.node(), namespace=GIVEN_NAMESPACE)

    # Extract pod information
    nodeName = pod.spec.node_name
    podName = pod.metadata.name
    namespace = pod.metadata.namespace
    status = pod.status.phase
    pod_ip = pod.status.pod_ip

    # Create and return a PodInfo instance
    return PodInfo(nodeName, podName, namespace, status, pod_ip)


@app.route('/')
def handle_request():
    podInfo = None
    error_message = None
    try:
        podInfo = get_pod_info()
    except Exception as e:
        logging.error("Error getting pod infos:", e)
        error_message = "Failed to retrieve pod information."

    background_color = os.environ.get('BACKGROUND_COLOR', '#fff')

    try:
        return render_template("index.html",
                               podInfo=podInfo,
                               background_color=background_color, error_message=error_message)
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
        logging.error("Error getting pod infos:", e)
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    logging.info("Starting server on port %d", 8080)
    app.run(port=8080)
