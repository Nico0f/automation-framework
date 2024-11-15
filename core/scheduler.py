import schedule
import time
import threading
from typing import Dict, Any
from ..utils.logger import setup_logger
from .task_manager import TaskManager
import yaml

class TaskScheduler:
    """Handles scheduling and periodic execution of tasks"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.logger = setup_logger()
        self.running = False
        self._load_schedules()

    def _load_schedules(self):
        """Load schedule configuration from YAML"""
        try:
            with open('config/schedule.yaml', 'r') as f:
                self.schedules = yaml.safe_load(f)['schedules']
        except Exception as e:
            self.logger.error(f"Failed to load schedules: {e}")
            self.schedules = []

    def _schedule_task(self, task_config: Dict[str, Any]):
        """Schedule a single task"""
        def job():
            try:
                self.task_manager.execute_task(
                    task_config['task'],
                    task_config['parameters']
                )
            except Exception as e:
                self.logger.error(f"Scheduled task failed: {e}")

        schedule_str = task_config['schedule']
        if schedule_str.startswith("0 "):  # Daily schedule
            schedule.every().day.at(schedule_str.split(" ")[1]).do(job)
        else:
            schedule.every().hour.do(job)

    def start(self):
        """Start the scheduler in a separate thread"""
        self.running = True

        for task_config in self.schedules:
            self._schedule_task(task_config)
        
        thread = threading.Thread(target=self._run_scheduler)
        thread.daemon = True
        thread.start()

    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """Stop the scheduler"""
        self.running = False