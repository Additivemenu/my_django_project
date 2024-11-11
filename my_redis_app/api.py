# api.py
from ninja import Router, Schema
from django.http import JsonResponse
from typing import Optional
import redis
import json
from django.conf import settings

router = Router()

# Initialize Redis connection
redis_client = redis.Redis.from_url(settings.REDIS_URL)  # we get this env when building the image

class Item(Schema):
    id: Optional[str] = None
    name: str
    description: str
    price: float

@router.post("/")
def create_item(request, item: Item):
    """Create a new item in Redis"""
    try:
        # Generate a simple ID if none provided
        if not item.id:
            item.id = str(redis_client.incr('item:id:counter'))
        
        # Convert item to dictionary and store in Redis
        item_dict = item.dict()
        redis_client.set(f'item:{item.id}', json.dumps(item_dict))
        
        return JsonResponse({
            "status": "success",
            "data": item_dict,
            "message": "Item created successfully"
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@router.get("/{item_id}")
def get_item(request, item_id: str):
    """Get an item from Redis by ID"""
    try:
        item_data = redis_client.get(f'item:{item_id}')
        if not item_data:
            return JsonResponse({
                "status": "error",
                "message": "Item not found"
            }, status=404)
        
        return JsonResponse({
            "status": "success",
            "data": json.loads(item_data),
            "message": "Item retrieved successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@router.get("/")
def list_items(request):
    """List all items from Redis"""
    try:
        # Get all keys matching the pattern 'item:*' but not the counter
        keys = redis_client.keys('item:*')
        keys = [k.decode('utf-8') for k in keys if k != b'item:id:counter']
        
        items = []
        for key in keys:
            item_data = redis_client.get(key)
            if item_data:
                items.append(json.loads(item_data))
        
        return JsonResponse({
            "status": "success",
            "data": items,
            "message": "Items retrieved successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@router.put("/{item_id}")
def update_item(request, item_id: str, item: Item):
    """Update an item in Redis"""
    try:
        if not redis_client.exists(f'item:{item_id}'):
            return JsonResponse({
                "status": "error",
                "message": "Item not found"
            }, status=404)
        
        item.id = item_id
        item_dict = item.dict()
        redis_client.set(f'item:{item_id}', json.dumps(item_dict))
        
        return JsonResponse({
            "status": "success",
            "data": item_dict,
            "message": "Item updated successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@router.delete("/{item_id}")
def delete_item(request, item_id: str):
    """Delete an item from Redis"""
    try:
        if not redis_client.exists(f'item:{item_id}'):
            return JsonResponse({
                "status": "error",
                "message": "Item not found"
            }, status=404)
        
        redis_client.delete(f'item:{item_id}')
        return JsonResponse({
            "status": "success",
            "message": "Item deleted successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)