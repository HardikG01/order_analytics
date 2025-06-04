# 📦 Order Analytics System

A real-time order analytics system using FastAPI, Redis, and SQS (LocalStack), with leaderboard and user statistics APIs.

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/order-analytics
cd order-analytics
```

### 2. Start the services using Docker Compose
```bash
docker-compose up
```
### 3. Populate the SQS queue with sample data
Use the provided Python script in the scripts folder to send messages to the Localstack SQS queue:
```bash 
python scripts/populate_sqs.py
```
### 4. Verify the worker processes the messages
The worker service will read messages from the SQS queue, process them, and update Redis.


### 5. Test the API endpoints
Use curl or a browser to hit the following endpoints:
```bash
curl http://localhost:8000/users/U5678/stats
curl http://localhost:8000/stats/global
```