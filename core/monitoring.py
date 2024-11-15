from prometheus_client import start_http_server, Summary, Counter, Gauge
import psutil
import time
import threading
from typing import Dict

class SystemMonitor:
    """Monitor system resources and task execution metrics"""
    
    def __init__(self, port: int = 9090):
        self.port = port
        
        # Define metrics
        self.task_duration = Summary('task_duration_seconds', 
                                   'Time spent executing tasks')
        self.task_count = Counter('tasks_total', 
                                'Total number of tasks executed',
                                ['task_type', 'status'])
        self.active_tasks = Gauge('active_tasks', 
                                'Number of currently running tasks')
        self.system_metrics = {
            'cpu': Gauge('system_cpu_usage', 'System CPU usage percentage'),
            'memory': Gauge('system_memory_usage', 'System memory usage percentage'),
            'disk': Gauge('system_disk_usage', 'System disk usage percentage')
        }
        
        self.running = False

    def start(self):
        """Start the monitoring server and metrics collection"""
        # Start Prometheus metrics server
        start_http_server(self.port)
        
        self.running = True
        
        # Start system metrics collection in a separate thread
        thread = threading.Thread(target=self._collect_metrics)
        thread.daemon = True
        thread.start()

    def _collect_metrics(self):
        """Collect system metrics periodically"""
        while self.running:
            # Update system metrics
            self.system_metrics['cpu'].set(psutil.cpu_percent())
            self.system_metrics['memory'].set(psutil.virtual_memory().percent)
            self.system_metrics['disk'].set(psutil.disk_usage('/').percent)
            
            time.sleep(30)  # Collect metrics every 30 seconds

    def record_task_execution(self, task_type: str, duration: float, 
                            status: str):
        """Record task execution metrics"""
        self.task_duration.observe(duration)
        self.task_count.labels(task_type=task_type, status=status).inc()

    def stop(self):
        """Stop the monitoring system"""
        self.running = False