# Using an official Python runtime as a parent image
FROM python:3.10-slim

ARG POETRY_DIR

# Set environment variables


# ! Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     curl \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y bash gcc git libcurl4-openssl-dev \
    libc-dev libpq-dev openssh-server && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="opt/poetry" \
    VIRTUAL_ENV="/venv" \
    PYTHONPATH="/app:$PYTHONPATH"
ENV PATH="$POETRY_HOME/bin:$PATH"

# ! Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 - \
#     && poetry config virtualenvs.create false

RUN pip install poetry
RUN poetry config cache-dir $POETRY_DIR

# Set the working directory
WORKDIR /workspace

# Copy only the poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# Copy the entire project
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
