from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None