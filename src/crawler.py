import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from .utils import is_valid_url, setup_session

class WebCrawler:
    def __init__(self, base_url, max_pages=50, delay=1):
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.session = setup_session()
        self.visited_urls = set()
        self.domain = urlparse(base_url).netloc
        
    def crawl_site(self):
        """Crawl the entire site starting from base_url"""
        pages_to_crawl = [self.base_url]
        crawled_pages = []
        
        while pages_to_crawl and len(crawled_pages) < self.max_pages:
            current_url = pages_to_crawl.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            print(f"Crawling: {current_url}")
            
            try:
                # Add delay to be respectful
                time.sleep(self.delay)
                
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                
                self.visited_urls.add(current_url)
                crawled_pages.append((current_url, response.text))
                
                # Find more pages to crawl
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    
                    # Only crawl pages from same domain
                    if (is_valid_url(full_url, self.domain) and 
                        full_url not in self.visited_urls and 
                        full_url not in pages_to_crawl):
                        pages_to_crawl.append(full_url)
                        
            except Exception as e:
                print(f"Error crawling {current_url}: {e}")
                continue
        
        print(f"Crawled {len(crawled_pages)} pages")
        return crawled_pages