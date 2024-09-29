from pydantic import BaseModel

class ItemSchema(BaseModel):
    id: int = None
    name: str
    description: str

    class Config:
        orm_mode = True


# from pydantic import BaseModel
# from typing import List, Optional

# # this is for NinjaAPI
# class Item(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None