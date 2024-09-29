# import time
# from functools import wraps

# def logging_middleware(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         # Before request processing
#         start_time = time.time()
#         print(f"Request {request.method} {request.path} received at {start_time} ========================")

#         # Process the request
#         response = func(request, *args, **kwargs)
    
#         # After request processing
#         end_time = time.time()
#         duration = end_time - start_time
#         print(f"Response status: {response.status}, duration: {duration:.2f} seconds ====================================================================")

#         return response
#     return wrapper
