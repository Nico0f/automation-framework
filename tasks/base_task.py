from abc import ABC, abstractmethod
from typing import Any, Dict
from ..utils.logger import setup_logger

class BaseTask(ABC):
    """Base class for all automation tasks"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = setup_logger()

    @abstractmethod
    def execute(self) -> bool:
        """Execute the task"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate task parameters"""
        pass

    def cleanup(self) -> None:
        """Cleanup after task execution"""
        pass