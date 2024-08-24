import time
from functools import wraps
from django.http import JsonResponse
import json

def append_timestamp_middleware(func):
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
         # Check if the response is a JsonResponse
        if isinstance(response, JsonResponse):
            # Decode the original content
            data = json.loads(response.content)

            # Add a new field
            data['items'][0]['timestamp'] = end_time

            # Encode the modified content back to JSON and update the response
            response.content = json.dumps(data)
        
        
        print(f"Response status: {response.status_code}, duration: {duration:.2f} seconds, added a timestamp ------")

        return response
    return wrapper
