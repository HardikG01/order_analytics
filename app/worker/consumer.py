import boto3
import time
from processor import process_message

sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

QUEUE_NAME = "order-queue"

# Get the queue URL
response = sqs.get_queue_url(QueueName=QUEUE_NAME)
queue_url = response['QueueUrl']

print("Polling SQS...")

while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])
    for msg in messages:
        body = msg["Body"]
        process_message(body)

        # Delete after processing
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])

    time.sleep(1)
