# 📄 resource_monitor.py
# This script tracks the overall health of the node. In a banking environment like Wekeza Group, 
# you need to ensure that the teleportation engine itself doesn't cause a system crash by consuming too many resources.

"""
WekezaOmniOS Resource Monitor
Tracks CPU and Memory telemetry for the host node.
"""

import psutil
import time

class ResourceMonitor:
    def __init__(self, threshold_cpu=80.0, threshold_mem=85.0):
        self.threshold_cpu = threshold_cpu
        self.threshold_mem = threshold_mem

    def get_system_stats(self):
        """Returns current CPU and RAM usage percentages."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        return {"cpu": cpu, "memory": mem}

    def check_health(self):
        """Validates if the system is within safe operating parameters."""
        stats = self.get_system_stats()
        is_healthy = stats['cpu'] < self.threshold_cpu and stats['memory'] < self.threshold_mem
        
        status = "HEALTHY" if is_healthy else "STRESSED"
        print(f"[Resource Monitor] Status: {status} | CPU: {stats['cpu']}% | MEM: {stats['memory']}%")
        return is_healthy

if __name__ == "__main__":
    monitor = ResourceMonitor()
    while True:
        monitor.check_health()
        time.sleep(5)
