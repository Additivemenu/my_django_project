
Demo project to learn Django features

use poetry for package management
+ select the corresponding python interpreter by poetry
  + `cmd + shift + p` : `python: select interpreter` 


## run in dev container

+ note you need to explicitly define which vscode extension you want in the dev container
  + when you make changes in devcontainer.json or Dockerfile, make sure you rebuild the dev container 

when container is up and running, start the server in terminal:
```shell
poetry run python manage.py runserver
```




## Ninja api
+ [setup CRUD api with Ninja](./docs/ninja_api.md)

find the API doc in apis > https files, similar to postman 
