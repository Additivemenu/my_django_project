from ninja import NinjaAPI
from ninja import Router
from django.http import JsonResponse
from typing import List
# from myapp.middlewares.logging import logging_middleware
from myapp.models import Item
from myapp.schema.Item import ItemSchema
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
import json

# Create router instance
router = Router()

# Create - POST
@router.post("/items")
def create_item(request, item: ItemSchema):
    db_item = Item.objects.create(**item.dict())
    return JsonResponse({
        "message": "Item created successfully",
        "item": json.loads(serialize('json', [db_item]))[0]['fields']
    }, status=201)

# Read - GET all items
@router.get("/items")
def list_items(request):
    items = Item.objects.all()
    return JsonResponse({
        "items": json.loads(serialize('json', items))
    })

# Read - GET single item by id
@router.get("/items/{item_id}")
def get_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({
        "item": json.loads(serialize('json', [item]))[0]['fields']
    })

# Update - PUT
@router.put("/items/{item_id}")
def update_item(request, item_id: int, data: ItemSchema):
    item = get_object_or_404(Item, id=item_id)
    for attr, value in data.dict().items():
        setattr(item, attr, value)
    item.save()
    return JsonResponse({
        "message": "Item updated successfully",
        "item": json.loads(serialize('json', [item]))[0]['fields']
    })

# Delete - DELETE
@router.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return JsonResponse({
        "message": "Item deleted successfully"
    })

# from ninja import NinjaAPI
# from django.http import JsonResponse
# from typing import List
# from myapp.middlewares.logging import logging_middleware
# from myapp.models import Item
# from myapp.schema.Item import ItemSchema
# from django.shortcuts import get_object_or_404

# api = NinjaAPI()

# # Create - POST
# @api.post("/items")
# def create_item(request, item: ItemSchema):
#     db_item = Item.objects.create(**item.dict())
#     return {"message": "Item created successfully", "item": ItemSchema.from_orm(db_item)}

# # Read - GET all items
# @api.get("/items", response=List[ItemSchema])
# @logging_middleware
# def list_items(request):
#     items = Item.objects.all()
#     return [ItemSchema.from_orm(item) for item in items]

# # Read - GET single item by id
# @api.get("/items/{item_id}", response=ItemSchema)
# def get_item(request, item_id: int):
#     item = get_object_or_404(Item, id=item_id)
#     return ItemSchema.from_orm(item)

# # Update - PUT
# @api.put("/items/{item_id}")
# def update_item(request, item_id: int, data: ItemSchema):
#     item = get_object_or_404(Item, id=item_id)
#     for attr, value in data.dict().items():
#         setattr(item, attr, value)
#     item.save()
#     return {"message": "Item updated successfully", "item": ItemSchema.from_orm(item)}

# # Delete - DELETE
# @api.delete("/items/{item_id}")
# def delete_item(request, item_id: int):
#     item = get_object_or_404(Item, id=item_id)
#     item.delete()
#     return {"message": "Item deleted successfully"}

 
 
# original code -- using in-memory storage  -------------
# from ninja import NinjaAPI
# from django.http import JsonResponse
# from typing import List
# from myapp.middlewares.logging import logging_middleware
# from myapp.middlewares.modify_item import modify_item_middleware
# from myapp.schema.Item import Item

# # Initialize the Ninja API
# api = NinjaAPI()

# # In-memory storage for items (no database)
# items: List[Item] = [{
#     "id": 1,
#     "name": "Item 1",
#     "description": "First item"
# }]


# # Create - POST
# @api.post("/items")
# def create_item(request, item: Item):
#     # items.append(item.model_dump_json())
#     items.append(item.model_dump())
#     return {"message": "Item created successfully", "item": item}

# # Read - GET all items
# @api.get("/items", response=List[Item])
# @logging_middleware
# @modify_item_middleware
# def list_items(request):
#     return JsonResponse({"items":items})

# # Read - GET single item by id
# @api.get("/items/{item_id}", response=Item)
# def get_item(request, item_id: int):
#     for item in items:
#         if item['id'] == item_id:
#             return item
#     return {"message": "Item not found"}, 404

# # Update - PUT
# @api.put("/items/{item_id}")
# def update_item(request, item_id: int, data: Item):
#     for index, item in enumerate(items):
#         if item['id'] == item_id:
#             items[index] = data.dict()
#             return {"message": "Item updated successfully", "item": data}
#     return {"message": "Item not found"}, 404

# # Delete - DELETE
# @api.delete("/items/{item_id}")
# def delete_item(request, item_id: int):
#     for index, item in enumerate(items):
#         if item['id'] == item_id:
#             items.pop(index)
#             return {"message": "Item deleted successfully"}
#     return {"message": "Item not found"}, 404