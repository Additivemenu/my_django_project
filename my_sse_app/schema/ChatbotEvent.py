from datetime import datetime
from ninja import Schema
from typing import Literal, Optional, Union

class ChatbotEventData(Schema):
    """
    Represents events emitted during a chat session, including chat lifecycle events
    and task tracking events.

    Chat Events:
    - chat_start: Marks the beginning of a chat session
    - chat_completed: Marks the successful completion of a chat session

    Task Events:
    - task_start: Indicates a new task has begun within the chat
    - task_completed: Indicates a task has been completed
    """
    timestamp: str
    taskName: Optional[str]  # Present only for task events
    taskIndex: Optional[int]  # Tracks the sequence of tasks within a chat
    type: Literal["task_start", "task_completed", "chat_start", "chat_completed"]

    class Config:
        schema_extra = {
            "examples": [
                # Chat start event
                {
                    "timestamp": "2024-12-05T12:00:00Z",
                    "taskName": None,
                    "taskIndex": None,
                    "type": "chat_start"
                },
                # Task start event
                {
                    "timestamp": "2024-12-05T12:00:05Z",
                    "taskName": "data_processing",
                    "taskIndex": 1,
                    "type": "task_start"
                },
                # Task completed event
                {
                    "timestamp": "2024-12-05T12:00:10Z",
                    "taskName": "data_processing",
                    "taskIndex": 1,
                    "type": "task_completed"
                },
                # Chat completed event
                {
                    "timestamp": "2024-12-05T12:00:15Z",
                    "taskName": None,
                    "taskIndex": None,
                    "type": "chat_completed"
                }
            ]
        }

    def is_chat_event(self) -> bool:
        """Returns True if this is a chat lifecycle event."""
        return self.type in ["chat_start", "chat_completed"]

    def is_task_event(self) -> bool:
        """Returns True if this is a task event."""
        return self.type in ["task_start", "task_completed"]

    def validate_event(self) -> bool:
        """
        Validates that the event data is consistent:
        - Chat events should not have taskName or taskIndex
        - Task events must have both taskName and taskIndex
        """
        if self.is_chat_event():
            return self.taskName is None and self.taskIndex is None
        return self.taskName is not None and self.taskIndex is not None