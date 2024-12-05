from ninja import NinjaAPI
# from kedro_demo.api.endpoints import router as kedro_router
from my_kedro_api.api import router as kedro_router
from myapp.api import router as myapp_router
from my_redis_app.api import router as redis_router
from my_aws_app.api import router as aws_router
from my_sse_app.api import router as sse_router

# ! this should be the entry point of your NinjaAPI
api = NinjaAPI()

# ! mount router to the api here
# Mount the Kedro demo router
api.add_router("/kedro/", kedro_router)  # e.g. /api/kedro/
api.add_router("/myapp/", myapp_router)
api.add_router("/redis/items", redis_router)
api.add_router("/aws-app/", aws_router)
api.add_router("/sse/", sse_router)

