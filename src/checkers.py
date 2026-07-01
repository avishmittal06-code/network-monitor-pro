import time
import socket
import requests
from ping3 import ping

def check_icmp(host, timeout=2):
    """Returns latency in ms if successful, else None."""
    try:
        response = ping(host, timeout=timeout)
        if response is not False and response is not None:
            return response * 1000  # Convert to milliseconds
        return None
    except Exception:
        return None

def check_tcp(host, port, timeout=2):
    """Measures connection latency to a specific TCP port."""
    start_time = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return (time.perf_counter() - start_time) * 1000
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None

def check_http(url, timeout=3):
    """Measures latency of an HTTP GET request returning status 200."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    start_time = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return (time.perf_counter() - start_time) * 1000
        return None
    except requests.RequestException:
        return None
