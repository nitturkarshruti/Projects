import redis

# Connect to Redis with authentication
r = redis.StrictRedis(host='localhost', port=6379, db=0, password='shruti3108', decode_responses=True)

# Retrieve all keys (URL IDs)
keys = r.keys('*')

# Iterate through each key (URL ID) and fetch its corresponding value (URL)
for key in keys:
    # Fetch the value (URL) associated with the key
    url = r.get(key)
    print("URL ID:", key, "| URL:", url)
