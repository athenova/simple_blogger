import os
import boto3
import uuid

class S3Uploader():
    def __init__(self, key_id=None, secret=None, bucket=None, endpoint='https://storage.yandexcloud.net'):
        key_id = os.environ.get('S3_KEY_ID') if key_id is None else key_id
        secret = os.environ.get('S3_SECRET') if secret is None else secret
        self.bucket = os.environ.get('S3_BUCKET') if bucket is None else bucket
        self.client = boto3.client("s3"
                            , aws_access_key_id=key_id
                            , aws_secret_access_key=secret
                            , endpoint_url=endpoint)

    def upload(self, image_file_name, extraArgs={ 'ContentType': 'image/jpeg' }):
        file_name = str(uuid.uuid4())
        self.client.upload_file(image_file_name, self.bucket, file_name, ExtraArgs=extraArgs)
        return self.client.generate_presigned_url(ClientMethod='get_object', Params={ 'Bucket': self.bucket, 'Key': file_name })