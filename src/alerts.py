import requests

def send_webhook_alert(webhook_url, target_name, host, status, success_rate):
    """Sends a clean failure alert to Discord or Slack."""
    if not webhook_url:
        return

    color = 15158332 if status == "DOWN" else 3066993
    payload = {
        "embeds": [{
            "title": f"🚨 Network Alert: {target_name} is {status}",
            "description": f"Host `{host}` is showing issues.\n**Current Success Rate**: {success_rate}%",
            "color": color
        }]
    }
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except requests.RequestException:
        pass  # Fail silently to avoid interrupting the main thread
