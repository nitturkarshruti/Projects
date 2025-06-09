import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import redis
import os
import csv

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'shruti3108'
PROJECT_NAME = 'test'
HOMEPAGE = 'https://quotes.toscrape.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
NUMBER_OF_THREADS = 8
MAX_URLS_TO_CRAWL = 50  # Maximum number of URLs to crawl
queue = Queue()

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Function to create CSV files if they don't exist
def create_csv_files():
    # Create project directory if it doesn't exist
    if not os.path.exists(PROJECT_NAME):
        os.makedirs(PROJECT_NAME)

    if not os.path.isfile(PROJECT_NAME + '/queue.csv'):
        with open(PROJECT_NAME + '/queue.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL'])  # Write header
    if not os.path.isfile(PROJECT_NAME + '/crawled.csv'):
        with open(PROJECT_NAME + '/crawled.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL'])  # Write header


# Function to store URL in the specified CSV file
def store_url_to_csv(url, file_path):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url])


# Create CSV files if they don't exist
create_csv_files()


# Worker function to crawl URLs
def crawl_url():
    while True:
        # Get a tuple containing the URL ID and URL from the queue
        url_info = queue.get()
        # If the queue is empty, break out of the loop
        if url_info is None:
            break
        # Check if url_info is a tuple with exactly 2 elements
        if len(url_info) != 2:
            print("Invalid URL info:", url_info)
            # Mark the task as done
            queue.task_done()
            continue
        # Unpack the tuple
        url_id, url = url_info
        # Crawl the page and store data
        Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME).crawl_page(threading.current_thread().name, url)
        # Mark the task as done
        queue.task_done()


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=crawl_url)
        t.daemon = True
        t.start()


# Add URLs to the queue
def create_jobs():
    for link in file_to_set(PROJECT_NAME + '/queue.csv'):
        queue.put(link)
    queue.join()


# Check if there are URLs in the queue and crawl them
def crawl():
    queued_links = file_to_set(PROJECT_NAME + '/queue.csv')
    print("Queued Links:", queued_links)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        # Limit the number of URLs to crawl to MAX_URLS_TO_CRAWL
        urls_to_crawl = list(queued_links)[:MAX_URLS_TO_CRAWL]
        for url_id, url in enumerate(urls_to_crawl, start=1):
            queue.put((url_id, url))  # Pass URL ID and URL to the queue
        create_jobs()


# Start the crawling process
create_workers()
crawl()
