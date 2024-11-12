import pytest
import os
from django.conf import settings
from unittest.mock import MagicMock, patch
from django.test import Client
# magic is that we don't import any thing about the api here, a bit different to NestJS
# I guess there is a way to test a 'service' class directly in Django? it's just that I didn't organize code in ''service'' classes

@pytest.fixture
def mock_s3_client():
    with patch('boto3.client') as mock_client:
        s3_instance = MagicMock()
        mock_client.return_value = s3_instance
        yield s3_instance

@pytest.fixture
def test_image_setup(tmp_path):
    # Create a test uploads directory
    uploads_dir = tmp_path / "uploads"
    uploads_dir.mkdir()
    
    # Create a test PNG file
    test_file = uploads_dir / "test.png"
    test_file.write_bytes(b"fake png content")
    
    # Temporarily override BASE_DIR setting
    original_base_dir = settings.BASE_DIR
    settings.BASE_DIR = str(tmp_path)
    
    yield str(test_file)
    
    # ! Cleanup - anything after yield runs after the test
    settings.BASE_DIR = original_base_dir

# @pytest.mark.skip(reason="Skipping this test temporarily")
@pytest.mark.django_db
def test_successful_upload(mock_s3_client, test_image_setup):
    client = Client()
    
    # Configure test settings
    settings.AWS_STORAGE_BUCKET_NAME = 'test-bucket'
    settings.AWS_REGION = 'us-east-1'
    settings.AWS_ACCESS_KEY_ID = 'test-key-id'
    settings.AWS_SECRET_ACCESS_KEY = 'test-secret-key'
    
    # Configure mock S3 client behavior before making request
    mock_s3_client.upload_file.return_value = None
    
    response = client.post(f'/api/aws-app/upload/test.png/')
    
    # Add error debugging this test
    if response.status_code == 500:
        print(f"Server Error Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()['message'] == 'Upload successful'
    assert response.json()['file_url'] == 'https://test-bucket.s3.us-east-1.amazonaws.com/uploads/test.png'
    
    # Verify S3 upload was called correctly
    mock_s3_client.upload_file.assert_called_once()

@pytest.mark.django_db
def test_file_not_found(mock_s3_client):
    client = Client()
    
    response = client.post('/api/aws-app/upload/nonexistent.png/')
    
    assert response.status_code == 404
    assert 'error' in response.json()
    assert 'not found' in response.json()['error']

@pytest.mark.django_db
def test_invalid_file_type(mock_s3_client, tmp_path):
    client = Client()
    
    # Create a test text file
    uploads_dir = tmp_path / "uploads"
    uploads_dir.mkdir()
    test_file = uploads_dir / "test.txt"
    test_file.write_text("test content")
    
    settings.BASE_DIR = str(tmp_path)
    
    response = client.post('/api/aws-app/upload/test.txt/')
    
    assert response.status_code == 415
    assert 'error' in response.json()
    assert 'Only PNG and JPG files are allowed' in response.json()['error']