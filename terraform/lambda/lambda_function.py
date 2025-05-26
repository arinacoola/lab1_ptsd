import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    
    source_bucket = 's3-start'
    destination_bucket = 's3-finish'
    queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/lambda-queue'  
    
    object_key = event['Records'][0]['s3']['object']['key']
    copy_source = {'Bucket': source_bucket, 'Key': object_key}
    
    s3.copy_object(
        CopySource=copy_source,
        Bucket=destination_bucket,
        Key=object_key
    )
    
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=f"Copied {object_key} from {source_bucket} to {destination_bucket}"
    )
