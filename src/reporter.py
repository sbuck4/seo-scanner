#!/usr/bin/env python3
"""
Report generation for SEO Scanner
Creates organized, readable reports in dedicated folder
"""

import pandas as pd
from datetime import datetime
import os

class SEOReporter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        self.domain_name = base_url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
        
        # Create reports directory
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def save_results(self, pages_data, issues):
        """Save basic results - simplified version"""
        scan_folder = os.path.join(self.reports_dir, f"{self.domain_name}_{self.timestamp}")
        os.makedirs(scan_folder, exist_ok=True)
        
        # Save page data
        df_pages = pd.DataFrame(pages_data)
        pages_file = os.path.join(scan_folder, "detailed_page_data.csv")
        df_pages.to_csv(pages_file, index=False)
        
        # Save issues
        df_issues = pd.DataFrame(issues)
        issues_file = os.path.join(scan_folder, "issues_list.csv")
        df_issues.to_csv(issues_file, index=False)
        
        print(f"Reports saved in: {scan_folder}")
        return scan_folder