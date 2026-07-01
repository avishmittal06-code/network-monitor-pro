import time
import yaml
from concurrent.futures import ThreadPoolExecutor
from rich.live import Live
from rich.table import Table
from rich.console import Console

from src.checkers import check_icmp, check_tcp, check_http
from src.storage import init_db, log_to_db
from src.alerts import send_webhook_alert

console = Console()

class NetworkMonitor:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.settings = self.config["settings"]
        self.targets = self.config["targets"]
        self.webhook_url = self.config.get("notifications", {}).get("webhook_url", "")
        
        self.state = {
            t["host"]: {"history": [], "total": 0, "success": 0, "last_latency": 0.0, "alerted": False} 
            for t in self.targets
        }
        init_db()

    def run_single_check(self, target):
        host = target["host"]
        ttype = target["type"]
        name = target["name"]
        
        if ttype == "icmp":
            latency = check_icmp(host)
        elif ttype == "tcp":
            latency = check_tcp(host, target.get("port", 80))
        elif ttype == "http":
            latency = check_http(host)
        else:
            latency = None

        status = "ONLINE" if latency is not None else "OFFLINE"
        t_state = self.state[host]
        
        t_state["total"] += 1
        if latency is not None:
            t_state["success"] += 1
            t_state["last_latency"] = latency
            t_state["history"].append(latency)
        else:
            t_state["history"].append(0.0)
            
        if len(t_state["history"]) > self.settings["history_size"]:
            t_state["history"].pop(0)

        success_rate = (t_state["success"] / t_state["total"]) * 100
        
        log_to_db(name, host, ttype, latency if latency else 0.0, status)

        if success_rate < self.settings["alert_threshold_pct"] and not t_state["alerted"]:
            send_webhook_alert(self.webhook_url, name, host, "DOWN", success_rate)
            t_state["alerted"] = True
        elif success_rate >= self.settings["alert_threshold_pct"] and t_state["alerted"]:
            send_webhook_alert(self.webhook_url, name, host, "RECOVERED", success_rate)
            t_state["alerted"] = False

    def generate_ui_table(self) -> Table:
        table = Table(title="✨ Advanced Network & Service Monitor (Pro)", header_style="bold cyan")
        table.add_column("Target Name", style="white")
        table.add_column("Host Endpoint", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Status", style="bold")
        table.add_column("Last Latency", justify="right")
        table.add_column("Success Rate", justify="right")

        for t in self.targets:
            host = t["host"]
            t_state = self.state[host]
            success_rate = (t_state["success"] / t_state["total"]) * 100 if t_state["total"] > 0 else 100.0
            
            status_str = "[bold green]ONLINE[/bold green]" if t_state["history"] and t_state["history"][-1] > 0 else "[bold red]OFFLINE[/bold red]"
            latency_str = f"{t_state['last_latency']:.1f} ms" if status_str == "[bold green]ONLINE[/bold green]" else "N/A"
            
            table.add_row(t["name"], host, t["type"].upper(), status_str, latency_str, f"{success_rate:.1f}%")
        return table

    def start(self):
        console.print("[bold green]Starting background telemetry loops...[/bold green]")
        with Live(self.generate_ui_table(), refresh_per_second=1) as live:
            while True:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(self.run_single_check, self.targets)
                
                live.update(self.generate_ui_table())
                time.sleep(self.settings["ping_interval"])

if __name__ == "__main__":
    monitor = NetworkMonitor()
    try:
        monitor.start()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitoring stopped safely. Historical data preserved.[/bold yellow]")
