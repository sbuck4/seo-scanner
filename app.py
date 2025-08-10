import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from urllib.parse import urlparse
import sys

# Import logging configuration
from src.logging_config import setup_logging, get_logger

# Initialize logging (handle Streamlit Cloud environment)
try:
    logger = setup_logging()
    app_logger = get_logger("app")
except Exception:
    # Fallback for Streamlit Cloud - use basic logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("seo_scanner")
    app_logger = logger

# Import your existing scanner modules
try:
    from src.crawler import WebCrawler
    from src.analyzer import PageAnalyzer
    from src.issues import IssueDetector
    from src.enhanced_pandas_reporter import EnhancedPandasReporter
    app_logger.info("All modules imported successfully")
except ImportError as e:
    app_logger.error(f"Failed to import required modules: {e}")
    st.error("Application initialization failed. Please check your installation.")
    sys.exit(1)

# Page config
st.set_page_config(
    page_title="SEO Scanner Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Global styling */
    .stApp {
        background: #f8fafc;
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Cards and sections */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    .metric-card p {
        margin: 0;
        color: #64748b;
        font-weight: 500;
    }
    
    .critical { color: #dc2626; }
    .warning { color: #ea580c; }
    .good { color: #059669; }
    
    /* Issue cards */
    .issue-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #dc2626;
        margin-bottom: 1rem;
    }
    
    .issue-card.warning {
        border-left-color: #ea580c;
    }
    
    .issue-card h4 {
        margin: 0 0 0.5rem 0;
        color: #1a202c;
        font-size: 1.1rem;
    }
    
    .issue-card .url {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .issue-card .recommendation {
        color: #059669;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'scanned_websites' not in st.session_state:
    st.session_state.scanned_websites = set()
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'saved_scans' not in st.session_state:
    st.session_state.saved_scans = {}  # Store full scan data by ID

def check_user_limits(url):
    """All features available - no limitations"""
    return True, "✅ All features unlocked - unlimited scans available!"

def load_previous_scan(scan_id):
    """Load a previous scan by ID"""
    if scan_id in st.session_state.saved_scans:
        st.session_state.scan_results = st.session_state.saved_scans[scan_id]
        return True
    return False

def run_seo_scan(url, max_pages=10):
    """Run the SEO scan using existing code"""
    scan_logger = get_logger("scan")
    scan_logger.info(f"Starting SEO scan for {url} with max_pages={max_pages}")
    
    try:
        domain = urlparse(url).netloc
        if not domain:
            scan_logger.error(f"Invalid URL format: {url}")
            return None, "Invalid URL format"
        
        # Initialize components
        try:
            crawler = WebCrawler(url, max_pages=max_pages)
            analyzer = PageAnalyzer(domain)
            issue_detector = IssueDetector()
            scan_logger.info("Scanner components initialized successfully")
        except Exception as e:
            scan_logger.error(f"Failed to initialize scanner components: {e}")
            return None, f"Initialization error: {str(e)}"
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Crawl
        status_text.text("🌐 Crawling website...")
        progress_bar.progress(25)
        
        try:
            crawled_pages = crawler.crawl_site()
            scan_logger.info(f"Crawling completed. Found {len(crawled_pages) if crawled_pages else 0} pages")
        except Exception as e:
            scan_logger.error(f"Crawling failed: {e}")
            progress_bar.empty()
            status_text.empty()
            return None, f"Crawling failed: {str(e)}"
        
        if not crawled_pages:
            scan_logger.warning("No pages found to analyze")
            progress_bar.empty()
            status_text.empty()
            return None, "No pages found to analyze. The website may be blocking crawlers or have connection issues."
        
        # Step 2: Analyze
        status_text.text("📊 Analyzing pages...")
        progress_bar.progress(50)
        pages_data = []
        
        try:
            for i, (page_url, html_content) in enumerate(crawled_pages):
                page_analysis = analyzer.analyze_page(page_url, html_content)
                pages_data.append(page_analysis)
                # Update progress for each page
                current_progress = 50 + (i + 1) * 15 // len(crawled_pages)
                progress_bar.progress(min(current_progress, 65))
            scan_logger.info(f"Page analysis completed for {len(pages_data)} pages")
        except Exception as e:
            scan_logger.error(f"Page analysis failed: {e}")
            progress_bar.empty()
            status_text.empty()
            return None, f"Analysis failed: {str(e)}"
        
        # Step 3: Detect issues
        status_text.text("🔍 Detecting SEO issues...")
        progress_bar.progress(75)
        
        try:
            all_issues = issue_detector.detect_all_issues(pages_data)
            scan_logger.info(f"Issue detection completed. Found {len(all_issues)} issues")
        except Exception as e:
            scan_logger.error(f"Issue detection failed: {e}")
            progress_bar.empty()
            status_text.empty()
            return None, f"Issue detection failed: {str(e)}"
        
        # Step 4: Generate report
        status_text.text("📈 Generating reports...")
        progress_bar.progress(100)
        
        # Store results
        scan_id = f"{urlparse(url).netloc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = {
            'id': scan_id,
            'url': url,
            'pages_data': pages_data,
            'issues': all_issues,
            'scan_date': datetime.now(),
            'pages_found': len(pages_data)
        }
        
        # Add to history and save full scan data
        domain = urlparse(url).netloc.replace('www.', '')
        st.session_state.scanned_websites.add(domain)
        
        # Save full scan data
        st.session_state.saved_scans[scan_id] = results
        
        # Add to history list for sidebar display
        st.session_state.scan_history.append({
            'id': scan_id,
            'url': url,
            'domain': domain,
            'date': datetime.now(),
            'pages': len(pages_data),
            'issues': len(all_issues)
        })
        
        status_text.text("✅ Scan complete!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        scan_logger.info(f"SEO scan completed successfully for {url}")
        return results, None
        
    except Exception as e:
        scan_logger.error(f"Unexpected error during scan: {e}", exc_info=True)
        return None, f"Unexpected error: {str(e)}"

def display_results(results):
    """Display scan results in a professional dashboard format"""
    pages_data = results['pages_data']
    issues = results['issues']
    
    # Calculate metrics
    total_pages = len(pages_data)
    critical_issues = len([i for i in issues if i['type'] == 'CRITICAL'])
    warning_issues = len([i for i in issues if i['type'] == 'WARNING'])
    
    # Calculate average SEO score
    scores = []
    for page in pages_data:
        score = calculate_seo_score(page)
        scores.append(score)
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Metrics dashboard
    st.markdown("### 📊 SEO Analysis Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_pages}</h3>
            <p>Pages Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color_class = "critical" if critical_issues > 5 else "warning" if critical_issues > 0 else "good"
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="{color_class}">{critical_issues}</h3>
            <p>Critical Issues</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color_class = "warning" if warning_issues > 10 else "good"
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="{color_class}">{warning_issues}</h3>
            <p>Warning Issues</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        grade = get_grade(avg_score)
        color_class = "good" if avg_score >= 80 else "warning" if avg_score >= 60 else "critical"
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="{color_class}">{avg_score:.0f}/100</h3>
            <p>Average SEO Score ({grade})</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Issues Section
    if issues:
        st.markdown("### 🎯 Top Priority Issues")
        
        # Sort issues by priority
        critical_issues_list = [i for i in issues if i['type'] == 'CRITICAL'][:5]
        warning_issues_list = [i for i in issues if i['type'] == 'WARNING'][:3]
        
        for issue in critical_issues_list:
            st.markdown(f"""
            <div class="issue-card">
                <h4>🚨 {issue['category']}: {issue['issue']}</h4>
                <div class="url">{issue['url']}</div>
                <div class="recommendation">💡 {issue['recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        for issue in warning_issues_list:
            st.markdown(f"""
            <div class="issue-card warning">
                <h4>⚠️ {issue['category']}: {issue['issue']}</h4>
                <div class="url">{issue['url']}</div>
                <div class="recommendation">💡 {issue['recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Page Performance Table
    st.markdown("### 📄 Page Performance")
    
    # Create DataFrame for page summary
    page_summary = []
    for page in pages_data:
        score = calculate_seo_score(page)
        page_summary.append({
            'URL': page['url'],
            'SEO Score': score,
            'Grade': get_grade(score),
            'Title Length': page.get('title_length', 0),
            'Has Meta Desc': '✅' if page.get('has_meta_description', False) else '❌',
            'H1 Count': page.get('h1_count', 0),
            'Images w/o Alt': page.get('images_without_alt', 0),
            'Word Count': page.get('word_count', 0)
        })
    
    df = pd.DataFrame(page_summary)
    st.dataframe(df, use_container_width=True)
    
    # Download section - All features available
    st.markdown("### 📥 Download Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Download Excel Report"):
            try:
                reporter = EnhancedPandasReporter(results['url'])
                excel_file = reporter.generate_reports(pages_data, issues)
                st.success(f"Excel report generated: {excel_file}")
                st.info(f"📁 File saved to: {excel_file}")
            except Exception as e:
                st.error(f"Error generating report: {e}")
    
    with col2:
        if st.button("📋 Download CSV Data"):
            csv_data = pd.DataFrame(issues).to_csv(index=False)
            st.download_button(
                label="Download Issues CSV",
                data=csv_data,
                file_name=f"seo_issues_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

def calculate_seo_score(page):
    """Calculate SEO score for a page"""
    score = 0
    
    # Title (25 points)
    if page.get('title'):
        title_len = page.get('title_length', 0)
        if 30 <= title_len <= 60:
            score += 25
        elif title_len > 0:
            score += 15
    
    # Meta Description (25 points)
    if page.get('has_meta_description'):
        meta_len = page.get('meta_desc_length', 0)
        if 120 <= meta_len <= 160:
            score += 25
        elif meta_len > 0:
            score += 15
    
    # H1 Tag (20 points)
    h1_count = page.get('h1_count', 0)
    if h1_count == 1:
        score += 20
    elif h1_count > 0:
        score += 10
    
    # Images (15 points)
    total_images = page.get('total_images', 0)
    if total_images > 0:
        images_without_alt = page.get('images_without_alt', 0)
        alt_coverage = (total_images - images_without_alt) / total_images
        score += alt_coverage * 15
    else:
        score += 15  # No images = perfect score
    
    # Content (15 points)
    word_count = page.get('word_count', 0)
    if word_count >= 300:
        score += 15
    elif word_count >= 150:
        score += 10
    elif word_count > 0:
        score += 5
    
    return min(score, 100)

def get_grade(score):
    """Convert score to letter grade"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# Health check endpoint
@st.cache_data(ttl=60)
def health_check():
    """Health check for monitoring"""
    try:
        # Test basic functionality
        test_url = "https://example.com"
        parsed = urlparse(test_url)
        
        # Basic component initialization test
        test_domain = "example.com"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "url_parsing": bool(parsed.netloc),
                "logging": logger is not None,
                "streamlit": True
            }
        }
    except Exception as e:
        app_logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Main App Layout
def main():
    # Check for health endpoint query parameter
    try:
        query_params = st.query_params
        if "health" in query_params:
            health_status = health_check()
            st.json(health_status)
            return
    except Exception:
        # Handle if query params not available in some Streamlit versions
        pass
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>🔍 SEO Scanner Pro</h1>
        <p>Professional SEO analysis and actionable insights to boost your rankings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔍 SEO Scanner Pro")
        
        # App info
        st.markdown("**Status:** All features unlocked")
        websites_scanned = len(st.session_state.scanned_websites)
        total_scans = len(st.session_state.scan_history)
        st.markdown(f"**Websites Scanned:** {websites_scanned}")
        st.markdown(f"**Total Scans:** {total_scans}")
        
        # Scan History
        st.markdown("## 📈 Recent Scans")
        if st.session_state.scan_history:
            for i, scan in enumerate(reversed(st.session_state.scan_history[-10:])):  # Show last 10, newest first
                # Create a clickable button for each scan
                scan_date = scan['date'].strftime('%m/%d %H:%M')
                button_label = f"**{scan['domain']}**\n{scan_date} - {scan['pages']} pages, {scan['issues']} issues"
                
                # Use scan ID if available, otherwise create a fallback key
                scan_id = scan.get('id', f"{scan['domain']}_{scan['date'].strftime('%Y%m%d_%H%M%S')}")
                
                if st.button(
                    button_label,
                    key=f"scan_btn_{i}_{scan_id}",
                    help="Click to view this scan",
                    use_container_width=True
                ):
                    # Load the previous scan if ID exists in saved scans
                    if scan_id in st.session_state.saved_scans:
                        if load_previous_scan(scan_id):
                            st.rerun()
                        else:
                            st.error("Scan data not found")
                    else:
                        st.warning("This scan was from before the update. Please run a new scan.")
        else:
            st.markdown("*No scans yet*")
    
    # Main Content
    if st.session_state.scan_results is None:
        # Input Section
        st.markdown("### 🌐 Enter Website URL")
        
        with st.form("seo_scan_form"):
            url = st.text_input(
                "Website URL",
                placeholder="https://example.com",
                help="Enter the full URL including https://"
            )
            
            col1, col2 = st.columns([3, 1])
            with col2:
                max_pages = st.selectbox("Max Pages", [5, 10, 25, 50], index=1)
            
            submitted = st.form_submit_button("🔍 Start SEO Analysis")
            
            if submitted and url:
                # Validate URL
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # Check user limits
                can_scan, message = check_user_limits(url)
                
                if can_scan:
                    st.success(message)
                    
                    # Run scan
                    with st.spinner("Running SEO analysis..."):
                        results, error = run_seo_scan(url, max_pages)
                    
                    if results:
                        st.session_state.scan_results = results
                        st.rerun()
                    else:
                        st.error(f"Scan failed: {error}")
                else:
                    st.error(message)
            elif submitted:
                st.error("Please enter a valid website URL")
        
        # Features Section
        st.markdown("### ✨ What You Get")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **⚡ Lightning Fast**  
            Get comprehensive SEO analysis in under 60 seconds
            """)
        
        with col2:
            st.markdown("""
            **🎯 Actionable Insights**  
            Prioritized recommendations you can implement immediately
            """)
        
        with col3:
            st.markdown("""
            **📊 Professional Reports**  
            Excel and summary reports perfect for clients
            """)
    
    else:
        # Display Results
        st.markdown(f"### 📊 Results for: {st.session_state.scan_results['url']}")
        
        # Add breadcrumb navigation
        col1, col2 = st.columns([3, 1])
        with col1:
            scan_date = st.session_state.scan_results['scan_date'].strftime('%B %d, %Y at %I:%M %p')
            st.markdown(f"*Scanned on {scan_date}*")
        with col2:
            if st.button("🔄 New Scan"):
                st.session_state.scan_results = None
                st.rerun()
        
        display_results(st.session_state.scan_results)

if __name__ == "__main__":
    main()