# from ninja import Router
# from kedro.framework.session import KedroSession
# from kedro.framework.startup import bootstrap_project

# router = Router()

# @router.get("/")
# def index(request):
#     return {"message": "Hello, world!"}

# @router.get("/run/")
# def run_pipeline(request):
#     # project_path = "../my-kedro-app" # FIXME: what?
#     # bootstrap_project(project_path)

#     # with KedroSession.create("my-kedro-project", project_path) as session:
#     #     session.run(pipeline_name="my_pipeline")
    
#     return {"success": True}