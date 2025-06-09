import hashlib
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
import re
import redis

r = redis.StrictRedis(host='localhost', port=6379, password='shruti3108', decode_responses=True)

class Spider:
    def __init__(self, project_name, base_url, domain_name):
        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = f'{project_name}/queue.csv'
        self.crawled_file = f'{project_name}/crawled.csv'
        self.boot()
        self.crawl_page('First spider', self.base_url)

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    def crawl_page(self, thread_name, page_url):
        url_id = hashlib.md5(page_url.encode()).hexdigest()
        html_content = ''
        if page_url not in self.crawled:
            print(f'{thread_name} now crawling {page_url}')
            print(f'Queue {len(self.queue)} | Crawled {len(self.crawled)}')
            html_content = self.fetch_html_content(page_url)
            self.add_links_to_queue(html_content, page_url)
            self.queue.remove(page_url)
            self.crawled.add(page_url)
            self.update_files()
            self.parse_and_store_quotes(html_content, page_url)
        return url_id, html_content

    def fetch_html_content(self, page_url):
        try:
            with urlopen(page_url) as response:
                if 'text/html' in response.getheader('Content-Type'):
                    html_bytes = response.read()
                    return html_bytes.decode('utf-8')
        except Exception as e:
            print(f'Error while fetching HTML content from {page_url}: {e}')
        return ''

    def add_links_to_queue(self, html_content, page_url):
        finder = LinkFinder(self.base_url, page_url)
        finder.feed(html_content)
        for url in finder.page_links():
            if url not in self.queue and url not in self.crawled and self.domain_name == get_domain_name(url):
                self.queue.add(url)

    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)

    def parse_and_store_quotes(self, html_content, page_url):
        match = re.search(r'/tag/(\w+)/', page_url)
        if match:
            tag = match.group(1)
            quote_elements = re.findall(r'<span class="text" itemprop="text">(.*?)</span>', html_content)
            for quote in quote_elements:
                print(f"Quote: {quote} | Tag: {tag}")
                # Store quotes and tags in Redis
                quote_key = f"{page_url}:{quote}"
                r.hset('quotes', quote_key, tag)  # Store quote along with tag in Redis hash
                # Also store URL-to-ID mappings
                url_id = hashlib.md5(page_url.encode()).hexdigest()
                r.hset('url_to_id_hash', page_url, url_id)  # Store URL-to-ID mapping in Redis hash
        else:
            print("No tag found in URL:", page_url)
