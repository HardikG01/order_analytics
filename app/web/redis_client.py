import redis
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host='redis', port=REDIS_PORT, decode_responses=False)
