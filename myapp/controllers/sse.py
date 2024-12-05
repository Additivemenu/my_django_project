# from django.http import StreamingHttpResponse # for SSE real-time streaming events 
# from myapp.schema.Event import EventData
# import time
# import random
# from datetime import datetime
# from typing import List, Generator
# from myapp.api import router

# # SSE real-time streaming events -------------------------------------
# def event_stream() -> Generator[str, None, None]:
#     """Generate SSE events"""
#     while True:
#         data = EventData(
#             timestamp=datetime.now().strftime('%H:%M:%S'),
#             value=random.randint(1, 100)
#         )
        
#         # Format as SSE event
#         yield f"data: {data.json()}\n\n"
#         time.sleep(2)

# @router.get("/sse")
# def sse_endpoint(request):
#     """
#     Stream real-time events
#     Returns random numbers with timestamps every 2 seconds
#     """
#     response = StreamingHttpResponse(
#         event_stream(),
#         content_type='text/event-stream' # ! important
#     )
#     response['Cache-Control'] = 'no-cache'
#     response['X-Accel-Buffering'] = 'no'
#     return response


# # Alternative endpoint that sends a single event (useful for testing)
# @router.get("/event", response=EventData)
# def single_event(request):
#     """Get a single event data"""
#     return EventData(
#         timestamp=datetime.now().strftime('%H:%M:%S'),
#         value=random.randint(1, 100)
#     )