# schemas.py
from ninja import Schema
from datetime import datetime

class EventData(Schema):
    timestamp: str
    value: int