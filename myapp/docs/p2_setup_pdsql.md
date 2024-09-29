# Django PostgreSQL and pgAdmin Setup Summary

## 1. Setting up pgAdmin and PostgreSQL Database

We added pgAdmin to our Docker Compose setup by updating the `docker-compose.yml` file:

```yaml
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: django_db

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
```

After updating the Docker Compose file, we rebuilt the containers:

```
docker-compose up -d --build
```

## 2. Creating the Database Model

We defined an Item model in Django:

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
```

After creating the model or whenever you changed any database model, we ran migrations:

```
python manage.py makemigrations
python manage.py migrate
```

## 3. Browsing the Database in pgAdmin 

To access and browse the database using pgAdmin:

1. Open a web browser and go to `http://localhost:5050`.
2. Log in with (we set this in docker-compose.yml file):
   - Email: admin@admin.com
   - Password: admin
3. Add a new server connection:
   - Right-click on 'Servers' > 'Create' > 'Server'
   - General tab: Name the server (e.g., "Django DB")
   - Connection tab:
     - Host name/address: db
     - Port: 5432
     - Maintenance database: django_db
     - Username: postgres
     - Password: postgres
4. Click 'Save' to connect to the database.

Now you can browse your database, tables, and perform SQL queries through the pgAdmin interface. You can:
- View the 'myapp_item' table (corresponding to your Item model)
- Execute SQL queries
- Inspect table structure and data
- Perform database administration tasks

Remember, these credentials are for development purposes only. In a production environment, you would use more secure passwords and limit access to the pgAdmin interface.