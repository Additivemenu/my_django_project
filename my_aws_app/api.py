# schemas.py
from ninja import Schema
from typing import Optional

class UploadResponseSchema(Schema):
    message: str
    file_url: str

class ErrorResponseSchema(Schema):
    error: str

# api.py
import boto3
import os
from ninja import Router
from django.http import JsonResponse
from django.conf import settings
from typing import Optional

router = Router()

@router.post("/upload/{filename}/",
    response={
        200: UploadResponseSchema,
        404: ErrorResponseSchema,
        415: ErrorResponseSchema,  # Add 415 Unsupported Media Type response
        500: ErrorResponseSchema
    }
)
def upload_to_s3(request, filename: str):
    """
    just a dummy api to upload files from local server to s3
    see more at https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
    """
    try:
        # Define the base directory where files are stored
        base_upload_directory = os.path.join(settings.BASE_DIR, 'uploads') 
        file_path = os.path.join(base_upload_directory, filename)

        # Check if file exists
        if not os.path.exists(file_path):
            return JsonResponse(
                {'error': f'File {filename} not found in the specified directory'},
                status=404
            )

        # Get file mime type
        import mimetypes
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or 'application/octet-stream'

        # Allow only PNG and JPG files
        if content_type not in ['image/png', 'image/jpeg']:
            return JsonResponse(
                {'error': 'Only PNG and JPG files are allowed'},
                status=415
            )

        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # Upload to S3
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_file_path = f'uploads/{filename}'

        # Upload the file directly from the file path
        s3_client.upload_file(
            file_path,
            bucket_name,
            s3_file_path,
            ExtraArgs={'ContentType': content_type}
        )

        # Generate the URL -> aws uses this format: https://<bucket_name>.s3.<region>.amazonaws.com/<file_path>
        file_url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_file_path}"

        return JsonResponse({
            'message': 'Upload successful',
            'file_url': file_url
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)