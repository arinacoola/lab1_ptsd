import os
import boto3

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    print("EVENT:", event)
    destination_bucket = 's3-finish'
    queue_url = os.environ.get("SQS_QUEUE_URL")
    print("SQS_QUEUE_URL:", queue_url)
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        print("Processing object:", s3_key, "from bucket:", source_bucket)
        copy_source = {'Bucket': source_bucket, 'Key': s3_key}
        s3.copy_object(
            Bucket=destination_bucket,
            CopySource=copy_source,
            Key=s3_key
        )
        resp = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=f"Copied {s3_key} from {source_bucket} to {destination_bucket}"
        )
        print("SQS Response:", resp)
