from ninja import Router
from typing import List, Generator
from django.http import StreamingHttpResponse
from datetime import datetime
import time
import asyncio
from my_sse_app.schema.ChatbotEvent import ChatbotEventData

router = Router()

def create_chat_event(event_type: str) -> ChatbotEventData:
    """Create a chat lifecycle event"""
    return ChatbotEventData(
        timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        taskName=None,
        taskIndex=None,
        type=event_type
    )

def create_task_event(task_index: int, event_type: str) -> ChatbotEventData:
    """Create a task event"""
    task_names = ["data_processing", "analysis", "report_generation", "visualization"]
    return ChatbotEventData(
        timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        taskName=task_names[task_index % len(task_names)],
        taskIndex=task_index,
        type=event_type
    )

def simulate_chat_session() -> Generator[ChatbotEventData, None, None]:
    """Simulate a complete chat session with multiple tasks"""
    # Start chat
    yield create_chat_event("chat_start")
    time.sleep(2)  # Initial delay

    # Simulate 3 tasks
    for task_index in range(1, 4):
        # Task start
        yield create_task_event(task_index, "task_start")
        time.sleep(3)  # Simulate task processing

        # Task completion
        yield create_task_event(task_index, "task_completed")
        time.sleep(2)  # Delay between tasks

    # End chat
    yield create_chat_event("chat_completed")

def event_stream() -> Generator[str, None, None]:
    """Generate SSE events for a chat session"""
    for event in simulate_chat_session():
        yield f"data: {event.json()}\n\n"

@router.get("/chat-session")
def sse_chat_session(request):
    """
    Stream a simulated chat session with multiple tasks
    The session follows this sequence:
    1. Chat start
    2. Multiple tasks (start -> complete)
    3. Chat complete
    """
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

# Test endpoint for single events
@router.get("/test-event/{event_type}")
def test_event(request, event_type: str):
    """
    Get a single test event
    event_type can be: chat_start, chat_completed, task_start, task_completed
    """
    if event_type.startswith('task'):
        return create_task_event(1, event_type)
    return create_chat_event(event_type)