
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


## app demo 
docs are mounted in respective directory

myapp
+ simple item CRUD with pgsql db 

chatapp -> serve as talkative backend
+ modelling one-to-one, one-to-many, many-to-many relationships
+ authentication with auth0
+ deploy


## run in dev container

+ note you need to explicitly define which vscode extension you want in the dev container
  + when you make changes in devcontainer.json or Dockerfile, make sure you rebuild the dev container 

when container is up and running, start the server in terminal:
```shell
poetry run python manage.py runserver
```



The command you've provided is a common instruction used in a Dockerfile or a script to install various packages on a Debian-based Linux distribution, such as Ubuntu. Let's break down each part of the command:

### Full Command:
```bash
RUN apt-get update && apt-get install -y bash gcc git libcurl4-openssl-dev \
    libc-dev libpq-dev openssh-server && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Breakdown:

1. **`RUN apt-get update`**:
   - This command updates the package lists for the `apt-get` package manager. This ensures that `apt-get` knows about the latest versions of available packages and their dependencies. It's typically the first step before installing any new software to make sure you're getting the most recent versions.

2. **`&&`**:
   - The `&&` operator ensures that the next command only runs if the previous command was successful. In this case, it means the `apt-get install` command will only run if `apt-get update` completes without errors.

3. **`apt-get install -y bash gcc git libcurl4-openssl-dev libc-dev libpq-dev openssh-server`**:
   - This installs several packages:
     - **`bash`**: The Bourne Again SHell, which is a command-line shell used in most Linux distributions.
     - **`gcc`**: The GNU Compiler Collection, which is a compiler system supporting various programming languages, including C, C++, and others.
     - **`git`**: A version control system used to track changes in source code during software development.
     - **`libcurl4-openssl-dev`**: Development files and libraries for the cURL library, which is used for transferring data with URLs, supporting various protocols like HTTP, FTP, etc., and using OpenSSL for encryption.
     - **`libc-dev`**: Development files for the C standard library, which is essential for compiling C programs.
     - **`libpq-dev`**: Development files for PostgreSQL libraries, necessary for compiling programs that need to connect to a PostgreSQL database.
     - **`openssh-server`**: The OpenSSH server, which allows secure access to the server via SSH (Secure Shell).

   - The `-y` flag automatically answers "yes" to any prompts that might be encountered during installation, making the command non-interactive (important for automation scripts like Dockerfiles).

4. **`&& apt-get clean`**:
   - After the packages are installed, this command is used to clean up the local repository of retrieved package files. This helps reduce the size of the image by removing package files that are no longer needed.

5. **`&& rm -rf /var/lib/apt/lists/*`**:
   - This command deletes the cached files that were used by `apt-get` to determine package dependencies and versions. By removing these files, you further reduce the size of the Docker image, as these files are no longer needed after the installation is complete.

### Summary:
This command sequence is a best practice for installing packages in a Docker container. It installs essential tools and libraries, cleans up unnecessary files to reduce the image size, and ensures the system is left in a clean state without leftover package lists that might bloat the Docker image. This approach is particularly useful in environments where space efficiency is critical, such as containerized applications.





## debugger

firsly you need to have a launch.json file under .vscode
+ launch the server in debug mode by click on "run and debug" button under "run and debug" panel


## Ninja api
+ [setup CRUD api with Ninja](./docs/ninja_api.md)

find the API doc in apis > https files, similar to postman 



## Django middleware and decorators

similar to the interceptor in NestJS, onion model

## python type safety
pydantic
+ dict() vs. json()