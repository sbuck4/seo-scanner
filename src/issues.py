class IssueDetector:
    def __init__(self):
        self.issues = []
    
    def detect_all_issues(self, pages_data):
        """Detect all SEO issues across all pages"""
        all_issues = []
        
        for page in pages_data:
            page_issues = self.detect_page_issues(page)
            all_issues.extend(page_issues)
        
        return all_issues
    
    def detect_page_issues(self, page_data):
        """Detect SEO issues for a single page"""
        issues = []
        url = page_data['url']
        
        # Title issues
        issues.extend(self._check_title_issues(page_data, url))
        
        # Meta description issues
        issues.extend(self._check_meta_description_issues(page_data, url))
        
        # Header issues
        issues.extend(self._check_header_issues(page_data, url))
        
        # Image issues
        issues.extend(self._check_image_issues(page_data, url))
        
        # Content issues
        issues.extend(self._check_content_issues(page_data, url))
        
        # Technical SEO issues
        issues.extend(self._check_technical_issues(page_data, url))
        
        return issues
    
    def _check_title_issues(self, page_data, url):
        """Check for title-related issues"""
        issues = []
        
        title = page_data.get('title', '')
        title_length = page_data.get('title_length', 0)
        
        if not title:
            issues.append({
                'type': 'CRITICAL',
                'category': 'Title',
                'issue': 'Missing title tag',
                'url': url,
                'recommendation': 'Add a descriptive title tag (30-60 characters) that includes your main keyword'
            })
        elif title_length < 30:
            issues.append({
                'type': 'WARNING',
                'category': 'Title',
                'issue': f'Title too short ({title_length} characters)',
                'url': url,
                'recommendation': 'Expand title to 30-60 characters for better SEO impact'
            })
        elif title_length > 60:
            issues.append({
                'type': 'WARNING',
                'category': 'Title',
                'issue': f'Title too long ({title_length} characters)',
                'url': url,
                'recommendation': 'Shorten title to 30-60 characters to prevent truncation in search results'
            })
        
        return issues
    
    def _check_meta_description_issues(self, page_data, url):
        """Check for meta description issues"""
        issues = []
        
        has_meta_desc = page_data.get('has_meta_description', False)
        meta_desc_length = page_data.get('meta_desc_length', 0)
        
        if not has_meta_desc:
            issues.append({
                'type': 'CRITICAL',
                'category': 'Meta Description',
                'issue': 'Missing meta description',
                'url': url,
                'recommendation': 'Add a compelling meta description (120-160 characters) that encourages clicks'
            })
        elif meta_desc_length < 120:
            issues.append({
                'type': 'WARNING',
                'category': 'Meta Description',
                'issue': f'Meta description too short ({meta_desc_length} characters)',
                'url': url,
                'recommendation': 'Expand meta description to 120-160 characters for better search result display'
            })
        elif meta_desc_length > 160:
            issues.append({
                'type': 'WARNING',
                'category': 'Meta Description',
                'issue': f'Meta description too long ({meta_desc_length} characters)',
                'url': url,
                'recommendation': 'Shorten meta description to 120-160 characters to prevent truncation'
            })
        
        return issues
    
    def _check_header_issues(self, page_data, url):
        """Check for header structure issues"""
        issues = []
        
        h1_count = page_data.get('h1_count', 0)
        h2_count = page_data.get('h2_count', 0)
        total_headings = page_data.get('total_headings', 0)
        
        if h1_count == 0:
            issues.append({
                'type': 'CRITICAL',
                'category': 'Headers',
                'issue': 'Missing H1 tag',
                'url': url,
                'recommendation': 'Add exactly one H1 tag that describes the main topic of the page'
            })
        elif h1_count > 1:
            issues.append({
                'type': 'WARNING',
                'category': 'Headers',
                'issue': f'Multiple H1 tags ({h1_count} found)',
                'url': url,
                'recommendation': 'Use only one H1 tag per page. Convert additional H1s to H2 or H3 tags'
            })
        
        if total_headings == 0:
            issues.append({
                'type': 'WARNING',
                'category': 'Headers',
                'issue': 'No header tags found',
                'url': url,
                'recommendation': 'Add header tags (H1, H2, H3) to structure your content and improve readability'
            })
        
        return issues
    
    def _check_image_issues(self, page_data, url):
        """Check for image optimization issues"""
        issues = []
        
        total_images = page_data.get('total_images', 0)
        images_without_alt = page_data.get('images_without_alt', 0)
        
        if total_images > 0 and images_without_alt > 0:
            issues.append({
                'type': 'WARNING',
                'category': 'Images',
                'issue': f'{images_without_alt} of {total_images} images missing alt text',
                'url': url,
                'recommendation': 'Add descriptive alt text to all images for better accessibility and SEO'
            })
        
        return issues
    
    def _check_content_issues(self, page_data, url):
        """Check for content-related issues"""
        issues = []
        
        word_count = page_data.get('word_count', 0)
        
        if word_count < 150:
            issues.append({
                'type': 'WARNING',
                'category': 'Content',
                'issue': f'Low content volume ({word_count} words)',
                'url': url,
                'recommendation': 'Add more substantive content (aim for 300+ words) to provide value to users'
            })
        elif word_count < 300:
            issues.append({
                'type': 'INFO',
                'category': 'Content',
                'issue': f'Moderate content volume ({word_count} words)',
                'url': url,
                'recommendation': 'Consider expanding content to 300+ words for better SEO performance'
            })
        
        return issues
    
    def _check_technical_issues(self, page_data, url):
        """Check for technical SEO issues"""
        issues = []
        
        has_viewport = page_data.get('has_viewport_meta', False)
        lang_attribute = page_data.get('lang_attribute', '')
        canonical_url = page_data.get('canonical_url', '')
        
        if not has_viewport:
            issues.append({
                'type': 'WARNING',
                'category': 'Technical',
                'issue': 'Missing viewport meta tag',
                'url': url,
                'recommendation': 'Add viewport meta tag: <meta name="viewport" content="width=device-width, initial-scale=1">'
            })
        
        if not lang_attribute:
            issues.append({
                'type': 'WARNING',
                'category': 'Technical',
                'issue': 'Missing language attribute',
                'url': url,
                'recommendation': 'Add lang attribute to <html> tag (e.g., <html lang="en">)'
            })
        
        if not canonical_url:
            issues.append({
                'type': 'INFO',
                'category': 'Technical',
                'issue': 'Missing canonical URL',
                'url': url,
                'recommendation': 'Consider adding canonical URL to prevent duplicate content issues'
            })
        
        return issues