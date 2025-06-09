import threading
import mysql.connector
import csv
from queue import Queue
import requests
from spider import Spider
from domain import get_domain_name

PROJECT_NAME = 'test'
HOMEPAGE = 'https://quotes.toscrape.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = f"{PROJECT_NAME}/queue.csv"
CRAWLED_FILE = f"{PROJECT_NAME}/crawled.csv"
NUMBER_OF_THREADS = 8

# Function to establish connection to MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shruti3108",
            database="cool",
            pool_size=10 # Example pool size, adjust as needed
        )
        print("Connected to MySQL database.")
        return db
    except mysql.connector.Error as err:
        print("Error: ", err)
        return None

# Function to create database and table if they don't exist
def create_database_and_table():
    db = connect_to_database()
    if db:
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cool")
        cursor.execute("USE cool")
        cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(1024) NOT NULL, status VARCHAR(50) NOT NULL)")
        cursor.close()
        db.commit()
        db.close()

# Call the function to create database and table
create_database_and_table()

# Connect to the MySQL database
db = connect_to_database()

# Create a thread-safe queue
queue = Queue()

# Initialize Spider
spider = Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Lock for database operations
db_lock = threading.Lock()

# Function to read data from a CSV file and store it in MySQL
def store_csv_data_to_mysql(file_path):
    if not db.is_connected():
        db.reconnect()
    cursor = db.cursor()
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0]  # Assuming URL is in the first column of the CSV
            insert_query = "INSERT INTO urls (url, status) VALUES (%s, 'queued')"
            cursor.execute(insert_query, (url,))
    db.commit()
    cursor.close()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                spider.crawl_page(threading.current_thread().name, url)
                with db_lock:
                    cursor = db.cursor()
                    update_query = "UPDATE urls SET status = 'crawled' WHERE url = %s"
                    cursor.execute(update_query, (url,))
                    db.commit()
                    cursor.close()
            else:
                print(f"Error: Failed to fetch {url}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error: Failed to fetch {url}, {str(e)}")
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT url FROM urls WHERE status = 'queued'")
        queued_urls = [url[0] for url in cursor.fetchall()]
        cursor.close()
    for url in queued_urls:
        queue.put(url)
    queue.join()
    crawl()

# Check if there are items in the queue, if so crawl them
def crawl():
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls WHERE status = 'queued'")
        queued_count = cursor.fetchone()[0]
        cursor.close()
    if queued_count > 0:
        print(str(queued_count) + ' links in the queue')
        create_jobs()

# Store data from CSV files to MySQL
store_csv_data_to_mysql(QUEUE_FILE)
store_csv_data_to_mysql(CRAWLED_FILE)

create_workers()
crawl()

# Close the database connection when done
db.close()
