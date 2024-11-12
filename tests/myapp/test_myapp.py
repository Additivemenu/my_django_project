import pytest
from django.test import Client
from django.urls import reverse
from myapp.models import Item
import json

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def sample_item_data():
    return {
        "name": "Test Item",
        "description": "Test Description",
    }

@pytest.fixture
def create_sample_item(sample_item_data):
    """
    this fixture will create an item in the database using the sample_item_data fixture
    """
    return Item.objects.create(**sample_item_data)


@pytest.mark.django_db
class TestItemAPI:
    """
    ! test class that groups all the tests for the Item API
    @pytest.mark.django_db doesn't actually modify your real database. Here's what it actually does:

    Test Database Creation:
        !Creates a temporary test database for each test run
        This is completely separate from your actual/production database
        Usually creates it by copying your database structure (tables/schemas) but with no data

    Transaction Management:
        By default, it wraps each test in a transaction
        After each test, it rolls back the transaction
        !This ensures tests don't affect each other even when using the same test database
    
    But note @pytest.mark.django_db still need database access, so you need a database connection to run these tests
        we have defined the database config in /tests/settings.py
    """
    
    def test_database_is_empty_at_start(self, client):
        assert Item.objects.count() == 0  # This will pass even after other tests
        # that create/modify items, because each test starts fresh
    
    def test_create_item(self, client, sample_item_data):
        response = client.post(
            '/api/myapp/items',
            data=json.dumps(sample_item_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['message'] == "Item created successfully"
        assert response.json()['item']['name'] == sample_item_data['name']
        assert response.json()['item']['description'] == sample_item_data['description']
        assert Item.objects.count() == 1

    def test_list_items(self, client, create_sample_item):
        """
        !no matter which test framework, always prepare the fixture or mock first, then run the test logic
        
        Execution order:
        1. client fixture runs -> returns Client()
        2. create_sample_item fixture needs sample_item_data fixture
        3. sample_item_data fixture runs -> returns test data dict
        4. create_sample_item creates database item using that data
        !5. Finally the actual test function runs with all fixtures ready
        """
        response = client.get('/api/myapp/items') 
        
        assert response.status_code == 200
        items = response.json()['items']
        assert len(items) == 1
        assert items[0]['fields']['name'] == create_sample_item.name

    def test_get_item_by_id(self, client, create_sample_item):
        response = client.get(f'/api/myapp/items/{create_sample_item.id}')
        
        assert response.status_code == 200
        item = response.json()['item']
        assert item['name'] == create_sample_item.name
        assert item['description'] == create_sample_item.description

    def test_get_nonexistent_item(self, client):
        response = client.get('/api/myapp/items/999')
        assert response.status_code == 404

    def test_update_item(self, client, create_sample_item):
        """
        pytest has prepared a sample item data in database using the create_sample_item fixture
        now we want to update that item in this test
        """
        # step1: arrange
        updated_data = {
            "name": "Updated Item",
            "description": "Updated Description",
        }
        
        # step2: action
        response = client.put(
            f'/api/myapp/items/{create_sample_item.id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        # step3: assertion
        assert response.status_code == 200
        assert response.json()['message'] == "Item updated successfully"
        assert response.json()['item']['name'] == updated_data['name']
        assert response.json()['item']['description'] == updated_data['description']

        ## Verify database was updated
        # updated_item = Item.objects.get(id=create_sample_item.id)
        # assert updated_item.name == updated_data['name']
        
    def test_delete_item(self, client, create_sample_item):
        response = client.delete(f'/api/myapp/items/{create_sample_item.id}')
        
        assert response.status_code == 200
        assert response.json()['message'] == "Item deleted successfully"
        assert Item.objects.count() == 0

    def test_delete_nonexistent_item(self, client):
        response = client.delete('/api/myapp/items/999')
        assert response.status_code == 404