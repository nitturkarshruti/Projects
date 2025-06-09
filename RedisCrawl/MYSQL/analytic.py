import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shruti3108",
    database="cool"
)

def analyze_urls():
    cursor = db.cursor()

    # Get the count of URLs by status
    cursor.execute("SELECT status, COUNT(*) AS count FROM urls GROUP BY status")
    status_counts = {status: count for status, count in cursor}

    # Get the distribution of URLs across different domains
    cursor.execute("SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', 3), '://', -1) AS domain, COUNT(*) AS count FROM urls GROUP BY domain")
    domain_counts = {domain: count for domain, count in cursor}

    cursor.close()

    return status_counts, domain_counts

if __name__ == "__main__":
    status_counts, domain_counts = analyze_urls()

    print("Status Counts:")
    for status, count in status_counts.items():
        print(f"{status}: {count}")

    print("\nDomain Distribution:")
    for domain, count in domain_counts.items():
        print(f"{domain}: {count}")
