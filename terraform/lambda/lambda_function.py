import os
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    
    source_bucket = os.environ["S3_START"]
    destination_bucket = os.environ["S3_FINISH"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    copy_source = {
        'Bucket': source_bucket,
        'Key': object_key
    }
    s3.copy_object(
        Bucket=destination_bucket,
        Key=object_key,
        CopySource=copy_source
    )
