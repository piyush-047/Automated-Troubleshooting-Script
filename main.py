import os
import psutil
import subprocess
import logging
from datetime import datetime

# Configure logging
log_file = f"logs/error_logs_{datetime.now().strftime('%Y%m%d')}.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def collect_event_logs():
    """Collect Windows Event Viewer logs using PowerShell."""
    try:
        command = ["powershell", "-Command", "Get-EventLog -LogName System -Newest 100 | Out-File -FilePath logs/event_logs.txt"]
        subprocess.run(command, check=True)
        logging.info("Successfully collected event logs.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to collect event logs: {e}")

def analyze_performance():
    """Analyze system performance (CPU, memory, disk usage)."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")
        
        performance_data = f"""
        CPU Usage: {cpu_usage}%
        Memory Usage: {memory_info.percent}%
        Disk Usage: {disk_usage.percent}%
        """
        logging.info("Performance Data:\n" + performance_data)
        print(performance_data)
    except Exception as e:
        logging.error(f"Failed to analyze performance: {e}")

def troubleshoot_connectivity():
    """Check network connectivity."""
    try:
        response = subprocess.run(["ping", "google.com", "-n", "4"], capture_output=True, text=True)
        if response.returncode == 0:
            logging.info("Network connectivity is fine.")
            print("Network connectivity is fine.")
        else:
            logging.warning("Network connectivity issues detected.")
            print("Network connectivity issues detected.")
    except Exception as e:
        logging.error(f"Failed to check connectivity: {e}")

def run_powershell_script(script_path):
    """Run a PowerShell script."""
    try:
        subprocess.run(["powershell", "-File", script_path], check=True)
        logging.info(f"PowerShell script {script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute PowerShell script {script_path}: {e}")

if __name__ == "__main__":
    print("Starting Automated Troubleshooting Script...")
    collect_event_logs()
    analyze_performance()
    troubleshoot_connectivity()
    run_powershell_script("scripts/config_check.ps1")
