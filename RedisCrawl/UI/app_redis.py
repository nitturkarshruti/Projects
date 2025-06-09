from flask import Flask, render_template
import redis

app = Flask(__name__)

# Connect to the Redis server on server1
redis_client = redis.Redis(host='192.168.86.195', port=6379, password='shruti3108')

@app.route('/')
def index():
    # Retrieve URLs and their corresponding hash values from Redis
    url_to_id_hash = redis_client.hgetall('url_to_id_hash')
    
    # Render HTML template with data
    return render_template('index_redis.html', url_to_id_hash=url_to_id_hash)

@app.route('/quotes')
def quotes():
    # Retrieve all quotes and their key values from Redis
    quotes = redis_client.hgetall('quotes')
    
    # Render HTML template with data
    return render_template('quotes.html', quotes=quotes)

@app.route('/quotes/<key>')
def filter_quotes(key):
    # Retrieve quotes filtered by the specified key from Redis
    filtered_quotes = {}
    quotes = redis_client.hgetall('quotes')
    
    # Filter quotes by the specified key
    for quote, keys in quotes.items():
        if key.encode('utf-8') in keys:
            filtered_quotes[quote.decode('utf-8')] = keys.decode('utf-8')
    
    # Render HTML template with filtered quotes
    return render_template('quotes.html', quotes=filtered_quotes, selected_key=key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
