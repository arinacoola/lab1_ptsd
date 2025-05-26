import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    destination_bucket = 's3-finish'
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        copy_source = {'Bucket': source_bucket, 'Key': s3_key}
        s3.copy_object(
            Bucket=destination_bucket,
            CopySource=copy_source,
            Key=s3_key
        )

