from typing import Dict, Any
from sqlalchemy import create_engine, text
from .base_task import BaseTask
from ..utils.decorators import retry

class DatabaseOperationsTask(BaseTask):
    """Task for database operations"""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.engine = create_engine(config['database_url'])

    def validate(self) -> bool:
        required_params = ['operation', 'query']
        return all(param in self.config for param in required_params)

    @retry(max_attempts=3)
    def execute(self) -> bool:
        try:
            operation = self.config['operation']
            query = self.config['query']
            
            with self.engine.connect() as connection:
                if operation == 'select':
                    result = connection.execute(text(query))
                    self.result = result.fetchall()
                else:
                    connection.execute(text(query))
                    connection.commit()
            
            self.logger.info(f"Database operation '{operation}' completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Database operation failed: {str(e)}")
            raise