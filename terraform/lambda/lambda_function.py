import os
import boto3

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    destination_bucket = 's3-finish'
    queue_name = os.environ["SQS_QUEUE"]
    queue_url = f"http://localhost:4566/000000000000/{queue_name}"
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        copy_source = {'Bucket': source_bucket, 'Key': s3_key}
        s3.copy_object(
            Bucket=destination_bucket,
            CopySource=copy_source,
            Key=s3_key
        )
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=f"Copied {s3_key} from {source_bucket} to {destination_bucket}"
        )
        
