import uvicorn
from core.task_manager import TaskManager
from core.scheduler import TaskScheduler
from core.monitoring import SystemMonitor
from tasks.file_operations import FileOperationsTask
from tasks.database_operations import DatabaseOperationsTask
from tasks.api_operations import APIOperationsTask
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    task_manager = TaskManager()
    scheduler = TaskScheduler(task_manager)
    monitor = SystemMonitor()
    
    task_manager.register_task('file_operations', FileOperationsTask)
    task_manager.register_task('database_operations', DatabaseOperationsTask)
    task_manager.register_task('api_operations', APIOperationsTask)
    
    try:
        monitor.start()
        logger.info("Monitoring system started")
        
        scheduler.start()
        logger.info("Task scheduler started")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
    finally:
        scheduler.stop()
        monitor.stop()

if __name__ == "__main__":
    main()