#!/usr/bin/env python3
"""
Page Analyzer for SEO Scanner
Analyzes individual pages for SEO elements and issues
"""

from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class PageAnalyzer:
    def __init__(self, domain):
        self.domain = domain
    
    def analyze_page(self, url, html_content):
        """Analyze a single page for SEO elements"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Basic page info
        analysis = {
            'url': url,
            'domain': self.domain,
            'title': self._get_title(soup),
            'title_length': 0,
            'has_meta_description': False,
            'meta_desc_length': 0,
            'meta_description': '',
            'h1_count': 0,
            'h1_text': '',
            'h2_count': 0,
            'h3_count': 0,
            'total_headings': 0,
            'total_images': 0,
            'images_without_alt': 0,
            'total_links': 0,
            'internal_links': 0,
            'external_links': 0,
            'word_count': 0,
            'page_size': len(html_content),
            'has_viewport_meta': False,
            'lang_attribute': '',
            'canonical_url': '',
            'robots_meta': '',
            'schema_markup': False
        }
        
        # Title analysis
        if analysis['title']:
            analysis['title_length'] = len(analysis['title'])
        
        # Meta description
        meta_desc = self._get_meta_description(soup)
        if meta_desc:
            analysis['has_meta_description'] = True
            analysis['meta_desc_length'] = len(meta_desc)
            analysis['meta_description'] = meta_desc
        
        # Headers analysis
        analysis.update(self._analyze_headers(soup))
        
        # Images analysis
        analysis.update(self._analyze_images(soup))
        
        # Links analysis
        analysis.update(self._analyze_links(soup, url))
        
        # Content analysis
        analysis['word_count'] = self._count_words(soup)
        
        # Technical SEO elements
        analysis.update(self._analyze_technical_seo(soup))
        
        return analysis
    
    def _get_title(self, soup):
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ''
    
    def _get_meta_description(self, soup):
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        return ''
    
    def _analyze_headers(self, soup):
        """Analyze header tags (H1, H2, H3, etc.)"""
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        
        return {
            'h1_count': len(h1_tags),
            'h1_text': h1_tags[0].get_text().strip() if h1_tags else '',
            'h2_count': len(h2_tags),
            'h3_count': len(h3_tags),
            'total_headings': len(h1_tags) + len(h2_tags) + len(h3_tags)
        }
    
    def _analyze_images(self, soup):
        """Analyze images for alt text and optimization"""
        images = soup.find_all('img')
        images_without_alt = 0
        
        for img in images:
            alt_text = img.get('alt')
            if not alt_text or not alt_text.strip():
                images_without_alt += 1
        
        return {
            'total_images': len(images),
            'images_without_alt': images_without_alt
        }
    
    def _analyze_links(self, soup, current_url):
        """Analyze internal and external links"""
        links = soup.find_all('a', href=True)
        internal_links = 0
        external_links = 0
        current_domain = urlparse(current_url).netloc
        
        for link in links:
            href = link['href']
            
            # Skip anchor links and javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Determine if internal or external
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain == current_domain:
                    internal_links += 1
                else:
                    external_links += 1
            else:
                # Relative links are internal
                internal_links += 1
        
        return {
            'total_links': len(links),
            'internal_links': internal_links,
            'external_links': external_links
        }
    
    def _count_words(self, soup):
        """Count words in main content"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)
    
    def _analyze_technical_seo(self, soup):
        """Analyze technical SEO elements"""
        result = {
            'has_viewport_meta': False,
            'lang_attribute': '',
            'canonical_url': '',
            'robots_meta': '',
            'schema_markup': False
        }
        
        # Viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        result['has_viewport_meta'] = viewport is not None
        
        # Language attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            result['lang_attribute'] = html_tag['lang']
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and canonical.get('href'):
            result['canonical_url'] = canonical['href']
        
        # Robots meta tag
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots and robots.get('content'):
            result['robots_meta'] = robots['content']
        
        # Schema markup (JSON-LD)
        schema_scripts = soup.find_all('script', type='application/ld+json')
        result['schema_markup'] = len(schema_scripts) > 0
        
        return result