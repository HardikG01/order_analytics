import boto3
import json

# Connect to Localstack SQS
sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

QUEUE_NAME = "order-queue"

# Create the queue if not exists (idempotent in SQS)
sqs.create_queue(QueueName=QUEUE_NAME)

# Get the queue URL
response = sqs.get_queue_url(QueueName=QUEUE_NAME)
queue_url = response['QueueUrl']

# Sample order message
sample_order = {
    "order_id": "ORD1234",
    "user_id": "U5678",
    "order_timestamp": "2024-12-13T10:00:00Z",
    "order_value": 99.99,
    "items": [
        {"product_id": "P001", "quantity": 2, "price_per_unit": 20.00},
        {"product_id": "P002", "quantity": 1, "price_per_unit": 59.99}
    ],
    "shipping_address": "123 Main St, Springfield",
    "payment_method": "CreditCard"
}

# Send 5 sample messages
for i in range(5):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(sample_order)
    )
    print(f"Message {i+1} sent. MessageId: {response['MessageId']}")

print("All sample messages sent to SQS.")
