import aiohttp
from typing import Dict, Any
from .base_task import BaseTask
from ..utils.decorators import retry

class APIOperationsTask(BaseTask):
    """Task for API operations"""

    def validate(self) -> bool:
        required_params = ['method', 'url']
        return all(param in self.config for param in required_params)

    @retry(max_attempts=3)
    async def execute(self) -> bool:
        try:
            method = self.config['method'].lower()
            url = self.config['url']
            headers = self.config.get('headers', {})
            data = self.config.get('data')
            
            async with aiohttp.ClientSession() as session:
                async with getattr(session, method)(
                    url, headers=headers, json=data
                ) as response:
                    self.result = await response.json()
                    success = 200 <= response.status < 300
                    
                    if success:
                        self.logger.info(f"API {method} request to {url} successful")
                    else:
                        self.logger.error(
                            f"API request failed with status {response.status}"
                        )
                    
                    return success
        except Exception as e:
            self.logger.error(f"API operation failed: {str(e)}")
            raise