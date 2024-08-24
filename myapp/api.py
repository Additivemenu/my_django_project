from ninja import NinjaAPI
from django.http import JsonResponse
from pydantic import BaseModel
from typing import List, Optional
from myapp.middlewares.logging import logging_middleware
from myapp.middlewares.append_timestamp import append_timestamp_middleware

# Initialize the Ninja API
api = NinjaAPI()


# TODO: Declare the type for item, and its serialization/deserialization


# In-memory storage for items (no database)
items = [{
    "id": 1,
    "name": "Item 1",
    "description": "First item"
}]

# Pydantic model for the Item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Create - POST
@api.post("/items")
def create_item(request, item: Item):
    items.append(item.dict())
    return {"message": "Item created successfully", "item": item}

# Read - GET all items
@api.get("/items", response=List[Item])
@logging_middleware
@append_timestamp_middleware
def list_items(request):
    print("get all items - right before breakpoint")
    
    return JsonResponse({"items":items})
    # return items

# Read - GET single item by id
@api.get("/items/{item_id}", response=Item)
def get_item(request, item_id: int):
    for item in items:
        if item['id'] == item_id:
            return item
    return {"message": "Item not found"}, 404

# Update - PUT
@api.put("/items/{item_id}")
def update_item(request, item_id: int, data: Item):
    for index, item in enumerate(items):
        if item['id'] == item_id:
            items[index] = data.dict()
            return {"message": "Item updated successfully", "item": data}
    return {"message": "Item not found"}, 404

# Delete - DELETE
@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    for index, item in enumerate(items):
        if item['id'] == item_id:
            items.pop(index)
            return {"message": "Item deleted successfully"}
    return {"message": "Item not found"}, 404