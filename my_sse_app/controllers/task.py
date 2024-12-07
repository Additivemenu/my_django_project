# tasks/api.py
from ninja import Router
from typing import Generator
import asyncio
import time
import uuid
from django.http import StreamingHttpResponse
from my_sse_app.schema.task import TaskCreate, TaskResponse, TaskEvent
from my_sse_app.models.task import Task, SubTask
from django.shortcuts import get_object_or_404
import json

router = Router()


@router.post("/tasks", response=TaskResponse)
def create_task(request, task_data: TaskCreate):
    """Create a new task"""
    task = Task.objects.create(status='created')
    return {
        "task_id": task.id,
        "status": task.status,
        "created_at": task.created_at
    }

@router.post("/tasks/{task_id}/start")
def start_task(request, task_id: uuid.UUID):
    """Start processing a specific task"""
    task = get_object_or_404(Task, id=task_id)
    if task.status != "created":
        return {"error": "Task is not in a startable state"}
    
    task.status = "pending"
    task.save()
    
    # Create subtasks
    subtasks = [
        ("Data Validation", 0),
        ("Data Processing", 1),
        ("Report Generation", 2)
    ]
    
    for name, order in subtasks:
        SubTask.objects.create(
            task=task,
            name=name,
            order=order
        )
    
    return {"status": "started"}

def create_event(task_id: uuid.UUID, subtask_name: str, status: str, progress: int = None, message: str = None) -> dict:
    """Create a task event"""
    return {
        "task_id": str(task_id),
        "subtask_name": subtask_name,
        "status": status,
        "progress": progress,
        "message": message
    }

# !simulator 
def process_subtask(task_id: uuid.UUID, subtask_name: str) -> Generator[dict, None, None]:
    """Process a single subtask with progress updates"""
    try:
        # Update subtask status in database
        subtask = SubTask.objects.get(task_id=task_id, name=subtask_name)
        subtask.status = 'processing'
        subtask.save()

        # Initial progress event
        yield create_event(
            task_id=task_id,
            subtask_name=subtask_name,
            status="processing",
            progress=0,
            message=f"Starting {subtask_name}"
        )
        
        # Simulate work with progress updates
        for progress in range(20, 100, 20):
            time.sleep(1)  # Simulate work
            subtask.progress = progress
            subtask.message = f"{subtask_name} in progress: {progress}%"
            subtask.save()
            
            yield create_event(
                task_id=task_id,
                subtask_name=subtask_name,
                status="processing",
                progress=progress,
                message=subtask.message
            )
        
        # Complete subtask
        subtask.status = 'completed'
        subtask.progress = 100
        subtask.message = f"{subtask_name} completed"
        subtask.save()
        
        yield create_event(
            task_id=task_id,
            subtask_name=subtask_name,
            status="completed",
            progress=100,
            message=subtask.message
        )
        
    except Exception as e:
        subtask.status = 'failed'
        subtask.message = str(e)
        subtask.save()
        
        yield create_event(
            task_id=task_id,
            subtask_name=subtask_name,
            status="failed",
            message=str(e)
        )

# !simulator
def task_progress_stream(task_id: uuid.UUID) -> Generator[str, None, None]:
    """Stream task progress events"""
    task = get_object_or_404(Task, id=task_id)
    task.status = 'processing'
    task.save()
    
    try:
        # Process each subtask
        subtasks = SubTask.objects.filter(task=task).order_by('order')
        
        for subtask in subtasks:
            for event in process_subtask(task_id, subtask.name):
                yield f"data: {json.dumps(event)}\n\n"
        
        # Update task status to completed
        task.status = 'completed'
        task.save()
        
    except Exception as e:
        task.status = 'failed'
        task.save()
        yield f"data: {json.dumps(create_event(task_id, 'Error', 'failed', message=str(e)))}\n\n"

@router.get("/tasks/{task_id}/progress")
def task_progress(request, task_id: uuid.UUID):
    """Stream task progress events"""
    response = StreamingHttpResponse(
        task_progress_stream(task_id),
        content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response