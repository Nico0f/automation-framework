class AutomationError(Exception):
    """Base exception for automation framework"""
    pass

class TaskExecutionError(AutomationError):
    """Raised when task execution fails"""
    pass

class ValidationError(AutomationError):
    """Raised when validation fails"""
    pass

class ConfigurationError(AutomationError):
    """Raised when configuration is invalid"""
    pass