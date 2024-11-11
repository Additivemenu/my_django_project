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
        # "price": 99.99
    }

@pytest.fixture
def create_sample_item(sample_item_data):
    return Item.objects.create(**sample_item_data)

# ! test class that groups all the tests for the Item API
@pytest.mark.django_db
class TestItemAPI:
    def test_create_item(self, client, sample_item_data):
        response = client.post(
            '/api/items',
            data=json.dumps(sample_item_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['message'] == "Item created successfully"
        assert response.json()['item']['name'] == sample_item_data['name']
        assert response.json()['item']['description'] == sample_item_data['description']
        assert float(response.json()['item']['price']) == sample_item_data['price']
        assert Item.objects.count() == 1

    def test_list_items(self, client, create_sample_item):
        response = client.get('/api/items')
        
        assert response.status_code == 200
        items = response.json()['items']
        assert len(items) == 1
        assert items[0]['fields']['name'] == create_sample_item.name

    def test_get_item_by_id(self, client, create_sample_item):
        response = client.get(f'/api/items/{create_sample_item.id}')
        
        assert response.status_code == 200
        item = response.json()['item']
        assert item['name'] == create_sample_item.name
        assert item['description'] == create_sample_item.description
        assert float(item['price']) == create_sample_item.price

    def test_get_nonexistent_item(self, client):
        response = client.get('/api/items/999')
        assert response.status_code == 404

    def test_update_item(self, client, create_sample_item):
        updated_data = {
            "name": "Updated Item",
            "description": "Updated Description",
            "price": 199.99
        }
        
        response = client.put(
            f'/api/items/{create_sample_item.id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.json()['message'] == "Item updated successfully"
        assert response.json()['item']['name'] == updated_data['name']
        assert response.json()['item']['description'] == updated_data['description']
        assert float(response.json()['item']['price']) == updated_data['price']

        # Verify database was updated
        updated_item = Item.objects.get(id=create_sample_item.id)
        assert updated_item.name == updated_data['name']

    def test_delete_item(self, client, create_sample_item):
        response = client.delete(f'/api/items/{create_sample_item.id}')
        
        assert response.status_code == 200
        assert response.json()['message'] == "Item deleted successfully"
        assert Item.objects.count() == 0

    def test_delete_nonexistent_item(self, client):
        response = client.delete('/api/items/999')
        assert response.status_code == 404