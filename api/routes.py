from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI()

class TaskRequest(BaseModel):
    task_type: str
    parameters: Dict[str, Any]

@app.post("/tasks")
async def create_task(task_request: TaskRequest):
    """Create and execute a new task"""
    try:
        result = task_manager.execute_task(
            task_request.task_type,
            task_request.parameters
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks")
async def list_tasks():
    """List all registered tasks"""
    return {"tasks": list(task_manager.tasks.keys())}

@app.get("/metrics")
async def get_metrics():
    """Get system and task metrics"""
    return monitor.get_metrics()