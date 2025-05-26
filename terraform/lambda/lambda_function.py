import boto3

def lambda_handler(event, context):
    print("Event:", event)
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
    
    source_bucket = 's3-start'
    destination_bucket = 's3-finish'
    queue_url = 'http://localhost:4566/000000000000/lambda-queue' 

    try:
        object_key = event['Records'][0]['s3']['object']['key']
        print(f"Object key: {object_key}")
        copy_source = {'Bucket': source_bucket, 'Key': object_key}
        s3.copy_object(
            CopySource=copy_source,
            Bucket=destination_bucket,
            Key=object_key
        )
        print("File copied!")
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=f"Copied {object_key} from {source_bucket} to {destination_bucket}"
        )
        print("Message sent to SQS!")
        return {"status": "success"}
    except Exception as e:
        print("Error:", str(e))
        raise
