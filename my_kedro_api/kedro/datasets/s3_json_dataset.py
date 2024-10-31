# File: your_app/kedro/datasets/s3_json_dataset.py
from kedro.io import AbstractDataset
import boto3
import json
from typing import Any, Dict
from datetime import datetime
import io

# TODO: install boto3 and try to run this code
class S3JsonDataSet(AbstractDataset):
    """
    Custom dataset that handles JSON data in S3.
    
    Args:
        bucket_name: Name of the S3 bucket
        key: The S3 key (path) where the file will be saved
        aws_access_key_id: AWS access key (optional if using IAM roles)
        aws_secret_access_key: AWS secret key (optional if using IAM roles)
        region_name: AWS region name
    """
    def __init__(
        self,
        bucket_name: str,
        key: str,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        region_name: str = 'us-east-1',
        save_args: Dict[str, Any] = None,
    ):
        self._bucket_name = bucket_name
        self._key = key
        self._save_args = save_args or {"indent": 2}
        
        # Initialize S3 client
        self._s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def _load(self) -> Dict[str, Any]:
        """Loads data from S3."""
        try:
            # Get object from S3
            response = self._s3_client.get_object(
                Bucket=self._bucket_name,
                Key=self._key
            )
            
            # Read JSON data from S3 object
            json_data = response['Body'].read().decode('utf-8')
            data = json.loads(json_data)
            
            # Validate required fields
            required_fields = ["processed_at", "data"]
            if not all(field in data for field in required_fields):
                raise ValueError(f"JSON must contain fields: {required_fields}")
            
            return data
            
        except self._s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(
                f"File not found in S3: {self._bucket_name}/{self._key}"
            )

    def _save(self, data: Dict[str, Any]) -> None:
        """Saves data to S3."""
        # Add metadata
        enhanced_data = {
            "data": data,
            "processed_at": datetime.now().isoformat(),
            "version": "1.0",
            "metadata": {
                "source": "kedro_pipeline",
                "created_at": datetime.now().isoformat(),
                "bucket": self._bucket_name,
                "key": self._key
            }
        }
        
        # Convert to JSON string
        json_data = json.dumps(enhanced_data, **self._save_args)
        
        # Upload to S3
        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=self._key,
            Body=json_data.encode('utf-8'),
            ContentType='application/json'
        )

    def _describe(self) -> Dict[str, Any]:
        """Returns a description of the dataset."""
        return {
            "bucket": self._bucket_name,
            "key": self._key,
            "save_args": self._save_args
        }