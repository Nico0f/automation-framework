from typing import Dict, List, Type
from ..tasks.base_task import BaseTask
from ..exceptions.custom_exceptions import TaskExecutionError
from ..utils.logger import setup_logger

class TaskManager:
    """Manages task execution and scheduling"""
    
    def __init__(self):
        self.tasks: Dict[str, Type[BaseTask]] = {}
        self.logger = setup_logger()

    def register_task(self, task_name: str, task_class: Type[BaseTask]) -> None:
        """Register a new task type"""
        self.tasks[task_name] = task_class
        self.logger.info(f"Registered task type: {task_name}")

    def execute_task(self, task_name: str, config: Dict) -> bool:
        """Execute a single task"""
        if task_name not in self.tasks:
            raise TaskExecutionError(f"Unknown task type: {task_name}")

        task = self.tasks[task_name](task_name, config)
        
        if not task.validate():
            raise TaskExecutionError(f"Task validation failed: {task_name}")

        try:
            result = task.execute()
            task.cleanup()
            return result
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            raise TaskExecutionError(f"Task execution failed: {str(e)}")

    def execute_workflow(self, workflow: List[Dict]) -> bool:
        """Execute a sequence of tasks"""
        for task_config in workflow:
            task_name = task_config['task_type']
            task_params = task_config['parameters']
            
            self.logger.info(f"Executing task: {task_name}")
            success = self.execute_task(task_name, task_params)
            
            if not success:
                return False
        return True