
Demo project to learn Django features

NEXT:
+ use docker-compose to inlude a postgres db for chat app. Chat app is always a simple but good practice to learn a framework
+ try to deploy the app to aws
  + this is important! and this skills is transferrable!
+ try to do an async programming demo app (e.g. user submit long-running tasks)
+ try to add a kedro app within myapp


use poetry for package management
+ select the corresponding python interpreter by poetry
  + `cmd + shift + p` : `python: select interpreter` 


# This Project specific





## app demo 
docs are mounted in respective app directory. Here is just overview:

[myapp](./myapp/docs/readme.md)
+ simple item CRUD with pgsql db 

[chat app](./my_chatpp/docs/mychatapp.md) -> serve as talkative backend
+ modelling one-to-one, one-to-many, many-to-many relationships
+ authentication with auth0
+ deploy

[redis app](./my_redis_app/docs/readme.md)


[kedro app](./my_kedro_api/docs/readme.md)


[AWS app](./my_aws_app/docs/readme.md)

> check /api_client for API test endpoints, just like postman


## vscode devcontainer

[understanding dev container](.devcontainer/doc/readme.md)

## debugger

firsly you need to have a launch.json file under .vscode
+ launch the server in debug mode by click on "run and debug" button under "run and debug" panel


## env setup

```shell
python manage.py check
```




# Django & Python Specific

## Django middleware and decorators
similar to the interceptor in NestJS, onion model

## python type safety
pydantic
+ dict() vs. json()

## pytest & unittest

[pytest & unittest](./tests/docs/readme.md)