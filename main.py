import sys
import os
from urllib.parse import urlparse
import argparse

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.crawler import WebCrawler
from src.analyzer import PageAnalyzer
from src.issues import IssueDetector
from src.reporter import SEOReporter
from src.enhanced_pandas_reporter import EnhancedPandasReporter

def get_user_input():
    """Get website URL from user with validation"""
    while True:
        website_url = input("Enter website URL (e.g., https://example.com): ").strip()
        
        if not website_url:
            print("❌ Please provide a valid URL")
            continue
            
        # Add https:// if missing
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
            
        # Validate URL
        try:
            parsed = urlparse(website_url)
            if not parsed.netloc:
                print("❌ Invalid URL format. Please try again.")
                continue
            return website_url
        except Exception:
            print("❌ Invalid URL format. Please try again.")
            continue

def print_banner():
    """Print welcome banner"""
    print("🔍" + "="*60 + "🔍")
    print("    SEO SCANNER - Free Website Analysis Tool")
    print("    Generate professional SEO reports in minutes!")
    print("🔍" + "="*60 + "🔍")
    print()

def main():
    """Main function to run SEO analysis"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SEO Scanner - Analyze website SEO health')
    parser.add_argument('--url', '-u', help='Website URL to analyze')
    parser.add_argument('--output', '-o', help='Output directory for reports', default='reports')
    parser.add_argument('--max-pages', '-m', type=int, help='Maximum pages to crawl', default=100)
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - minimal output')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    # Get website URL
    if args.url:
        website_url = args.url
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
    else:
        website_url = get_user_input()
    
    # Validate URL
    try:
        domain = urlparse(website_url).netloc
        if not domain:
            print("❌ Invalid URL format")
            return 1
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return 1
    
    try:
        # Initialize components
        if not args.quiet:
            print("🚀 Initializing SEO Scanner...")
        
        crawler = WebCrawler(website_url, max_pages=args.max_pages)
        analyzer = PageAnalyzer(domain)
        issue_detector = IssueDetector()
        reporter = SEOReporter(website_url)
        enhanced_reporter = EnhancedPandasReporter(website_url)
        
        # Step 1: Crawl the website
        if not args.quiet:
            print("\n=== STEP 1: CRAWLING WEBSITE ===")
            print(f"🌐 Analyzing: {website_url}")
        
        crawled_pages = crawler.crawl_site()
        
        if not crawled_pages:
            print("❌ No pages found to analyze. Please check your URL and try again.")
            return 1
        
        if not args.quiet:
            print(f"✅ Found {len(crawled_pages)} pages to analyze")
        
        # Step 2: Analyze each page
        if not args.quiet:
            print("\n=== STEP 2: ANALYZING PAGES ===")
        
        pages_data = []
        for i, (url, html_content) in enumerate(crawled_pages, 1):
            if not args.quiet:
                print(f"📄 Analyzing ({i}/{len(crawled_pages)}): {url}")
            page_analysis = analyzer.analyze_page(url, html_content)
            pages_data.append(page_analysis)
        
        # Step 3: Detect issues
        if not args.quiet:
            print("\n=== STEP 3: DETECTING ISSUES ===")
        
        all_issues = issue_detector.detect_all_issues(pages_data)
        
        if not args.quiet:
            print(f"🔍 Found {len(all_issues)} issues to address")
        
        # Step 4: Generate reports
        if not args.quiet:
            print("\n=== STEP 4: GENERATING REPORTS ===")
        
        # Generate comprehensive pandas reports
        excel_file = enhanced_reporter.generate_reports(pages_data, all_issues)
        
        # Also save the HTML report
        if not args.quiet:
            print("\n=== SAVING ADDITIONAL REPORTS ===")
        reporter.save_results(pages_data, all_issues)
        
        print("\n✅ SEO scan complete!")
        print("🎯 Check the Excel file for prioritized action items!")
        print(f"📊 Reports saved to: {os.path.dirname(excel_file)}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during scan: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)