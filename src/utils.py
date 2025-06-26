import requests
from urllib.parse import urlparse
import re

def is_valid_url(url, allowed_domain=None):
    """
    Validate if URL is valid and optionally check domain
    
    Args:
        url (str): URL to validate
        allowed_domain (str): If provided, only allow URLs from this domain
    
    Returns:
        bool: True if URL is valid
    """
    try:
        parsed = urlparse(url)
        
        # Basic URL validation
        if not parsed.netloc or not parsed.scheme:
            return False
        
        # Check if it's HTTP/HTTPS
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check domain if specified
        if allowed_domain and parsed.netloc != allowed_domain:
            return False
        
        # Skip common file extensions that aren't pages
        skip_extensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.tar', '.gz', '.exe', '.dmg',
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.mp3', '.mp4', '.avi', '.mov', '.wmv',
            '.css', '.js', '.xml', '.rss'
        ]
        
        url_lower = url.lower()
        if any(url_lower.endswith(ext) for ext in skip_extensions):
            return False
        
        # Skip common non-page patterns
        skip_patterns = [
            '/wp-admin/', '/admin/', '/login/', '/logout/',
            '/wp-content/', '/wp-includes/',
            'mailto:', 'tel:', 'ftp:', 'file:',
            '#', 'javascript:'
        ]
        
        if any(pattern in url_lower for pattern in skip_patterns):
            return False
        
        return True
        
    except Exception:
        return False

def setup_session():
    """
    Setup a requests session with appropriate headers and settings
    
    Returns:
        requests.Session: Configured session object
    """
    session = requests.Session()
    
    # Set user agent to identify as a legitimate crawler
    session.headers.update({
        'User-Agent': 'SEO-Scanner/1.0 (SEO Analysis Tool; +https://github.com/yourusername/seo-scanner)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Set timeout and retry strategy
    session.timeout = 10
    
    return session

def clean_text(text):
    """
    Clean and normalize text content
    
    Args:
        text (str): Raw text to clean
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ''
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
    
    return text

def extract_domain(url):
    """
    Extract domain name from URL
    
    Args:
        url (str): URL to extract domain from
    
    Returns:
        str: Domain name
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ''

def validate_title_length(title):
    """
    Validate title length for SEO best practices
    
    Args:
        title (str): Title to validate
    
    Returns:
        dict: Validation result with status and message
    """
    if not title:
        return {'status': 'error', 'message': 'Title is missing'}
    
    length = len(title)
    
    if length < 30:
        return {'status': 'warning', 'message': f'Title too short ({length} chars). Aim for 30-60 characters.'}
    elif length > 60:
        return {'status': 'warning', 'message': f'Title too long ({length} chars). Aim for 30-60 characters.'}
    else:
        return {'status': 'good', 'message': f'Title length is optimal ({length} chars)'}

def validate_meta_description_length(description):
    """
    Validate meta description length for SEO best practices
    
    Args:
        description (str): Meta description to validate
    
    Returns:
        dict: Validation result with status and message
    """
    if not description:
        return {'status': 'error', 'message': 'Meta description is missing'}
    
    length = len(description)
    
    if length < 120:
        return {'status': 'warning', 'message': f'Meta description too short ({length} chars). Aim for 120-160 characters.'}
    elif length > 160:
        return {'status': 'warning', 'message': f'Meta description too long ({length} chars). Aim for 120-160 characters.'}
    else:
        return {'status': 'good', 'message': f'Meta description length is optimal ({length} chars)'}

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
    
    Returns:
        str: Formatted size (e.g., "1.2 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"