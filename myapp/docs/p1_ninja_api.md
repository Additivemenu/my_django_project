Below are the steps to create a simple Django CRUD API using Django Ninja. This example will create a CRUD API without storing data in a database, using in-memory storage (a simple Python list) instead.

### Step 1: Install Django and Django Ninja

First, you need to install Django and Django Ninja. Since you're using Poetry, you can add these dependencies with the following command:

```bash
poetry add django django-ninja
```

### Step 2: Set Up Your Django Project

If you haven’t already set up a Django project, you can create one with the following commands:

```bash
poetry run django-admin startproject config .
```

### Step 3: Create a Django App

Create a new Django app where you'll implement the API:

```bash
poetry run python manage.py startapp myapp
```

### Step 4: Configure Django Ninja in Your App

In your `config/settings.py`, add `'ninja'` and your new app `'myapp'` to the `INSTALLED_APPS` list:

```python
# config/settings.py

INSTALLED_APPS = [
    # other apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja',
    'myapp',
]
```

### Step 5: Set Up the Django Ninja API

In your `myapp` directory, create a file named `api.py` where you'll define the API.

```bash
touch myapp/api.py
```

In `myapp/api.py`, set up a simple CRUD API using in-memory storage (a Python list):

```python
from ninja import NinjaAPI
from pydantic import BaseModel
from typing import List, Optional

# Initialize the Ninja API
api = NinjaAPI()

# In-memory storage for items (no database)
items = []

# Pydantic model for the Item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Create - POST
@api.post("/items")
def create_item(request, item: Item):
    items.append(item.dict())
    return {"message": "Item created successfully", "item": item}

# Read - GET all items
@api.get("/items", response=List[Item])
def list_items(request):
    return items

# Read - GET single item by id
@api.get("/items/{item_id}", response=Item)
def get_item(request, item_id: int):
    for item in items:
        if item['id'] == item_id:
            return item
    return {"message": "Item not found"}, 404

# Update - PUT
@api.put("/items/{item_id}")
def update_item(request, item_id: int, data: Item):
    for index, item in enumerate(items):
        if item['id'] == item_id:
            items[index] = data.dict()
            return {"message": "Item updated successfully", "item": data}
    return {"message": "Item not found"}, 404

# Delete - DELETE
@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    for index, item in enumerate(items):
        if item['id'] == item_id:
            items.pop(index)
            return {"message": "Item deleted successfully"}
    return {"message": "Item not found"}, 404
```

### Step 6: Include the API in Your Django Project

You need to wire up the API in your `config/urls.py`:

```python
# config/urls.py

from django.contrib import admin
from django.urls import path
from myapp.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # Include the Ninja API
]
```

### Step 7: Run the Django Server

Start the Django development server:

```bash
poetry run python manage.py runserver
```

### Step 8: Test the API

You can now test your API using tools like `curl`, Postman, or your browser.

- **Create an Item** (POST):

  ```bash
  curl -X POST "http://127.0.0.1:8000/api/items" -H "Content-Type: application/json" -d '{"id": 1, "name": "Item 1", "description": "First item"}'
  ```

- **List All Items** (GET):

  ```bash
  curl "http://127.0.0.1:8000/api/items"
  ```

- **Get a Single Item** (GET):

  ```bash
  curl "http://127.0.0.1:8000/api/items/1"
  ```

- **Update an Item** (PUT):

  ```bash
  curl -X PUT "http://127.0.0.1:8000/api/items/1" -H "Content-Type: application/json" -d '{"id": 1, "name": "Updated Item", "description": "Updated description"}'
  ```

- **Delete an Item** (DELETE):
  ```bash
  curl -X DELETE "http://127.0.0.1:8000/api/items/1"
  ```

### Summary:

- **Django Ninja** is a powerful and easy-to-use framework for building APIs in Django.
- This example stores data in-memory using a Python list, which means the data will not persist after the server is restarted.

You now have a fully functioning Django API using Django Ninja with simple CRUD operations. Let me know if you need further assistance!
