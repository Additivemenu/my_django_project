FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y bash gcc git libcurl4-openssl-dev libc-dev libpq-dev openssh-server postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="/opt/poetry" \
    VIRTUAL_ENV="/venv" \
    PYTHONPATH="/workspace:$PYTHONPATH"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /workspace

# Copy only the poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# We don't copy the rest of the code here, as it will be mounted as a volume

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


# Using an official Python runtime as a parent image
# FROM python:3.10-slim

# ARG POETRY_DIR

# # ! Install system dependencies (linux) ----------------------------------------
# # RUN apt-get update && apt-get install -y \
# #     build-essential \
# #     libpq-dev \
# #     curl \
# #     && apt-get clean \
# #     && rm -rf /var/lib/apt/lists/*

# # try this if line 22 - 26 doesn't work
# # RUN apt-get update && apt-get install -y bash gcc git libcurl4-openssl-dev \
# #     libc-dev libpq-dev openssh-server && apt-get clean && rm -rf /var/lib/apt/lists/*

# # if below doesn't work, try the above
# RUN apt-get update \ 
#     && apt-get install -y bash gcc git libcurl4-openssl-dev libc-dev libpq-dev openssh-server postgresql-client\
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

#     # Set environment variables ---------------------------------------------------
# # ! note we set poetry env vars here
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV POETRY_NO_INTERACTION=1 \  
#     POETRY_VIRTUALENVS_CREATE=0 \
#     POETRY_HOME="opt/poetry" \
#     VIRTUAL_ENV="/venv" \
#     PYTHONPATH="/app:$PYTHONPATH"
# ENV PATH="$POETRY_HOME/bin:$PATH"

# # ! Install Poetry --------------------------------------------------------------
# # RUN curl -sSL https://install.python-poetry.org | python3 - \
# #     && poetry config virtualenvs.create false

# RUN pip install poetry
# RUN poetry config cache-dir $POETRY_DIR  # ! note there is a cache dir

# # Set the working directory
# WORKDIR /workspace

# # Copy only the poetry files to leverage Docker cache
# COPY pyproject.toml poetry.lock ./

# # Install Python dependencies
# RUN poetry install --no-root

# # Copy the entire project
# COPY . .

# # Expose the port
# EXPOSE 8000

# # Command to run the development server
# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
