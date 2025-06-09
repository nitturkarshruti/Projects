import redis

# Redis connection details
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'himani'  # Replace 'your_password_here' with your actual password

# Connect to Redis
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# Clear all keys from the currently selected database
r.flushdb()

# If you want to clear all keys from all databases (use with caution):
# r.flushall()
