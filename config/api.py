from ninja import NinjaAPI
# from kedro_demo.api.endpoints import router as kedro_router
from my_kedro_api.api import router as kedro_router
from myapp.api import router as myapp_router

# ! this should be the entry point of your NinjaAPI
api = NinjaAPI()

# ! mount router to the api here
# Mount the Kedro demo router
api.add_router("/kedro/", kedro_router)
api.add_router("/myapp/", myapp_router)