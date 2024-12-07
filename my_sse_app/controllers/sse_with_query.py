from ninja import Router
from typing import List, Generator
from django.http import StreamingHttpResponse
from datetime import datetime
import time
import asyncio
from my_sse_app.schema.ChatbotEvent import ChatbotEventData

router = Router()

"""
! not yet used in nextjs-react-all-in-one app
"""

def create_chat_event(event_type: str, user_id: int, project_id: int) -> ChatbotEventData:
    """Create a chat lifecycle event with user and project context"""
    return ChatbotEventData(
        timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        taskName=None,
        taskIndex=None,
        type=event_type,
        userId=user_id,
        projectId=project_id
    )

def create_task_event(task_index: int, event_type: str, user_id: int, project_id: int) -> ChatbotEventData:
    """Create a task event with user and project context"""
    task_names = ["data_processing", "analysis", "report_generation", "visualization"]
    return ChatbotEventData(
        timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        taskName=task_names[task_index % len(task_names)],
        taskIndex=task_index,
        type=event_type,
        userId=user_id,
        projectId=project_id
    )

def simulate_chat_session(user_id: int, project_id: int) -> Generator[ChatbotEventData, None, None]:
    """Simulate a complete chat session with multiple tasks for specific user and project"""
    # Start chat
    yield create_chat_event("chat_start", user_id, project_id)
    time.sleep(2)  # Initial delay

    # Simulate 3 tasks
    for task_index in range(1, 4):
        # Task start
        yield create_task_event(task_index, "task_start", user_id, project_id)
        time.sleep(3)  # Simulate task processing
        
        # Task completion
        yield create_task_event(task_index, "task_completed", user_id, project_id)
        time.sleep(2)  # Delay between tasks

    # End chat
    yield create_chat_event("chat_completed", user_id, project_id)

def event_stream(user_id: int, project_id: int) -> Generator[str, None, None]:
    """Generate SSE events for a chat session with user and project context"""
    for event in simulate_chat_session(user_id, project_id):
        yield f"data: {event.json()}\n\n"

@router.get("/users/{user_id}/projects/{project_id}/chat-session")
def sse_chat_session(request, user_id: int, project_id: int):
    """
    Stream a simulated chat session with multiple tasks for a specific user and project
    The session follows this sequence:
    1. Chat start
    2. Multiple tasks (start -> complete)
    3. Chat complete
    """
    response = StreamingHttpResponse(
        event_stream(user_id, project_id),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response