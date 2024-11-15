import functools
import time
from typing import Callable
from ..exceptions.custom_exceptions import TaskExecutionError

def retry(max_attempts: int = 3, delay: int = 5):
    """Decorator to retry failed operations"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise TaskExecutionError(f"Failed after {max_attempts} attempts: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def validate_input(validator: Callable):
    """Decorator to validate input parameters"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not validator(*args, **kwargs):
                raise ValidationError("Input validation failed")
            return func(*args, **kwargs)
        return wrapper
    return decorator