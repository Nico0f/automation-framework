import shutil
from pathlib import Path
from typing import List
from .base_task import BaseTask
from ..utils.decorators import retry, validate_input

class FileOperationsTask(BaseTask):
    """Task for file operations"""

    def validate(self) -> bool:
        required_params = ['source_path', 'destination_path']
        return all(param in self.config for param in required_params)

    @retry(max_attempts=3)
    def execute(self) -> bool:
        try:
            source = Path(self.config['source_path'])
            dest = Path(self.config['destination_path'])
            
            if self.config.get('operation') == 'copy':
                if source.is_file():
                    shutil.copy2(source, dest)
                else:
                    shutil.copytree(source, dest)
            elif self.config.get('operation') == 'move':
                shutil.move(source, dest)
            
            self.logger.info(f"Successfully executed {self.config['operation']} operation")
            return True
        except Exception as e:
            self.logger.error(f"File operation failed: {str(e)}")
            raise