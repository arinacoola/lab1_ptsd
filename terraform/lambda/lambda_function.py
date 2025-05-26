import os
import boto3

def lambda_handler(event, context):
    print("EVENT:", event)
    queue_url = os.environ.get("SQS_QUEUE_URL")
    print("SQS_QUEUE_URL:", queue_url)
    destination_bucket = 's3-finish'
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        print("SOURCE BUCKET:", source_bucket)
        s3_key = record['s3']['object']['key']
        print("S3 KEY:", s3_key)
        copy_source = {'Bucket': source_bucket, 'Key': s3_key}
        try:
            s3.copy_object(
                Bucket=destination_bucket,
                CopySource=copy_source,
                Key=s3_key
            )
            print(f"Copied {s3_key} to {destination_bucket}")
        except Exception as e:
            print("Error copying object:", e)
        try:
            resp = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=f"Copied {s3_key} from {source_bucket} to {destination_bucket}"
            )
            print("SQS send_message response:", resp)
        except Exception as e:
            print("Error sending SQS message:", e)
