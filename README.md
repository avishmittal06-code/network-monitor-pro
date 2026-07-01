# ✨ Network & Service Monitor (Pro)

A production-grade, asynchronous, multi-protocol network and service reliability monitoring tool built with Python. It continuously tracks target accessibility, maintains long-term metrics telemetry, and triggers high-visibility incident alerts.

## 🚀 Key Features

* **Multi-Protocol Probing:** Supports concurrent monitoring via low-level **ICMP (Ping)**, raw **TCP ports** (e.g., SSH, databases), and **HTTP status codes** (web applications).
* **High-Performance Architecture:** Utilizes a concurrent `ThreadPoolExecutor` engine to probe dozens of hosts simultaneously without network blocking or performance degradation.
* **Beautiful Real-Time UI:** Leverages the `Rich` live-updating table UI to provide live dashboard statistics (latency trends, rolling success rates, and device states) inside the terminal.
* **Persistent Telemetry Logging:** Automatically streams every health event into a local, isolated **SQLite database** for historical downtime audits.
* **Smart Incident Alerting:** Seamlessly integrates with **Discord/Slack Webhooks** to fire rich embed notifications the moment a target's success rate falls below configurable safety thresholds.
* **Dockerized Container Deployment:** Pre-configured with an optimized `Dockerfile` for universal, single-command environment deployment.

## 🛠️ Quick Start

### 1. Installation
Clone the codebase and install the locked dependencies manifest:
```bash
git clone [https://github.com/avishmittal06-code/network-monitor-pro.git](https://github.com/avishmittal06-code/network-monitor-pro.git)
cd network-monitor-pro
pip install -r requirements.txt
```
### 2. Configuration
Modify `config.yaml` to configure monitoring frequencies, safety thresholds, alert webhooks, and endpoints:
```yaml
settings:
  ping_interval: 2.0
  history_size: 10
  alert_threshold_pct: 80.0

notifications:
  webhook_url: ""

targets:
  - host: "8.8.8.8"
    type: "icmp"
    name: "Google DNS"
- host: "github.com"
    type: "http"
    name: "GitHub Web"
  ```
### 3. Execution
Launch the live terminal monitoring console dashboard:
```bash
python main.py
```
### 4. Docker Containerization
Deploy the entire package inside an isolated, lightweight container environment:
```bash
docker build -t network-monitor-pro .
docker run -it network-monitor-pro
```
