import time
from functools import wraps
from django.http import JsonResponse
import json
from typing import List
from pydantic import ValidationError
from myapp.schema.Item import Item

def modify_response(response: JsonResponse):
    # Decode the original content
    data = json.loads(response.content)
    
    # !Deserialize data['items'] to a list of Item instances
    try:
        items: List[Item] = [Item.parse_obj(item) for item in data['items']]
    except ValidationError as e:
        print(f"Validation error: {e}")
        return JsonResponse({"error": "Invalid item data"}, status=400)

    # Modify the data to add a timestamp
    for item in items:
        # mofidy the item directly
        item.name = item.name + " - modified"
        
        # # append new field, so you need to convert the item to a dictionary first
        # item_dict = item.dict()
        # item_dict['timestamp'] = end_time
    
    # !Re-serialize the items back to JSON format
    data['items'] = [item.dict() for item in items]

    # Encode the modified content back to JSON and update the response
    response.content = json.dumps(data)


"""
apply this middleware to a route handler function to modify the content of the response before it is sent back to the client.
"""
def modify_item_middleware(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Before request processing
        start_time = time.time()
        print(f"Request {request.method} {request.path} received at {start_time} ------")

        # Process the request
        response = func(request, *args, **kwargs)

        # After request processing
        end_time = time.time()
        duration = end_time - start_time
        if isinstance(response, JsonResponse):
            modify_response(response)
            
        print(f"Response status: {response.status_code}, duration: {duration:.2f} seconds, modified item content------")

        return response
    return wrapper
