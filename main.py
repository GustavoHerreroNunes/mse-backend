import os
import logging
import requests
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "msesolucoes")
ZONE = os.environ.get("VM_ZONE", "southamerica-east1-a")
INSTANCE_NAME = os.environ.get("VM_INSTANCE_NAME", "pdf-generator-vm")

def get_access_token():
    """Get access token from Cloud Run's built-in metadata server."""
    url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
    resp = requests.get(url, headers={"Metadata-Flavor": "Google"}, timeout=5)
    return resp.json()["access_token"]

def get_vm_status(token):
    """Check current VM status."""
    url = f"https://compute.googleapis.com/compute/v1/projects/{PROJECT_ID}/zones/{ZONE}/instances/{INSTANCE_NAME}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
    resp.raise_for_status()
    return resp.json().get("status")

def start_vm(token):
    """Start the VM."""
    url = f"https://compute.googleapis.com/compute/v1/projects/{PROJECT_ID}/zones/{ZONE}/instances/{INSTANCE_NAME}/start"
    resp = requests.post(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()

@app.route("/start-pdf-generator", methods=["POST"])
def start_pdf_generator():
    try:
        token = get_access_token()
        status = get_vm_status(token)
        logging.info(f"VM current status: {status}")

        if status == "RUNNING":
            logging.info("VM already running, skipping start.")
            return jsonify({"status": "already_running"}), 200

        if status == "TERMINATED":
            result = start_vm(token)
            logging.info(f"VM start triggered: {result.get('status')}")
            return jsonify({"status": "started"}), 200

        # STAGING, STOPPING etc — don't interfere
        logging.info(f"VM in intermediate state: {status}, skipping.")
        return jsonify({"status": "skipped", "vm_status": status}), 200

    except Exception as e:
        logging.error(f"Error starting VM: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)