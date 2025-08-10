#!/usr/bin/env python3
"""
Basic functionality test for SEO Scanner
Run this locally before deploying to Streamlit Cloud
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from src.crawler import WebCrawler
        from src.analyzer import PageAnalyzer
        from src.issues import IssueDetector
        from src.enhanced_pandas_reporter import EnhancedPandasReporter
        print("[OK] All core modules import successfully")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic URL parsing and component initialization"""
    try:
        from urllib.parse import urlparse
        
        # Test URL parsing
        test_url = "https://example.com"
        parsed = urlparse(test_url)
        assert parsed.netloc == "example.com"
        
        # Test component initialization
        from src.analyzer import PageAnalyzer
        analyzer = PageAnalyzer("example.com")
        
        print("[OK] Basic functionality works")
        return True
    except Exception as e:
        print(f"[ERROR] Basic functionality error: {e}")
        return False

def test_dependencies():
    """Test that all dependencies are available"""
    required_packages = [
        'requests',
        'beautifulsoup4',
        'pandas',
        'openpyxl',
        'numpy',
        'streamlit'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"[ERROR] Missing dependencies: {missing}")
        return False
    else:
        print("[OK] All dependencies available")
        return True

if __name__ == "__main__":
    print("Testing SEO Scanner before deployment...\n")
    
    tests = [
        test_dependencies,
        test_imports,
        test_basic_functionality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("SUCCESS: All tests passed! Ready for Streamlit Cloud deployment.")
        sys.exit(0)
    else:
        print("FAILURE: Some tests failed. Fix issues before deploying.")
        sys.exit(1)