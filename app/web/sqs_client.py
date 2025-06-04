import boto3
from config import AWS_REGION, SQS_QUEUE_URL

sqs = boto3.client('sqs', region_name=AWS_REGION, endpoint_url="http://localhost:4566")  # Localstack

def receive_messages(max_messages=5, wait_time=10):
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time
    )
    return response.get("Messages", [])
