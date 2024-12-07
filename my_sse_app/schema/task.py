# tasks/schemas.py
from ninja import Schema
from datetime import datetime
from uuid import UUID
from typing import Optional

class TaskCreate(Schema):
    name: Optional[str] = None

class TaskResponse(Schema):
    task_id: UUID
    status: str
    created_at: datetime

class TaskEvent(Schema):
    task_id: str
    subtask_name: str
    status: str
    progress: Optional[int] = None
    message: Optional[str] = None