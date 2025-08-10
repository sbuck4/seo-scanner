import pandas as pd
import numpy as np
from datetime import datetime
import os
from io import BytesIO
import json

class EnhancedPandasReporter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        self.domain_name = base_url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
        
        # Create reports directory structure
        self.reports_dir = "reports"
        self.backend_storage_dir = os.path.join(self.reports_dir, "backend_storage")
        self.scan_folder = os.path.join(self.backend_storage_dir, f"{self.domain_name}_{self.timestamp}")
        
        # Ensure all directories exist
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.backend_storage_dir, exist_ok=True)
        os.makedirs(self.scan_folder, exist_ok=True)
    
    def create_priority_matrix(self, issues_df):
        """Create priority scoring for issues"""
        if issues_df.empty:
            return issues_df
        
        # Priority scoring
        priority_scores = {
            'CRITICAL': 10,
            'WARNING': 5,
            'INFO': 1
        }
        
        # Category impact scoring
        category_impact = {
            'Title': 10,
            'Meta Description': 9,
            'Headers': 8,
            'Images': 4,
            'Content': 3,
            'Technical': 6
        }
        
        issues_df['priority_score'] = issues_df['type'].map(priority_scores)
        issues_df['category_impact'] = issues_df['category'].map(category_impact).fillna(1)
        issues_df['total_score'] = issues_df['priority_score'] + issues_df['category_impact']
        
        # Sort by total score descending
        issues_df = issues_df.sort_values('total_score', ascending=False)
        
        return issues_df
    
    def create_page_summary(self, pages_df):
        """Create page-level summary with SEO scores"""
        if pages_df.empty:
            return pages_df
        
        # Calculate SEO scores for each page
        def calculate_page_score(row):
            score = 0
            max_score = 100
            
            # Title (25 points)
            if row['title']:
                if 30 <= row['title_length'] <= 60:
                    score += 25
                elif row['title_length'] > 0:
                    score += 15
            
            # Meta Description (25 points)
            if row['has_meta_description']:
                if 120 <= row['meta_desc_length'] <= 160:
                    score += 25
                elif row['meta_desc_length'] > 0:
                    score += 15
            
            # H1 Tag (20 points)
            if row['h1_count'] == 1:
                score += 20
            elif row['h1_count'] > 0:
                score += 10
            
            # Images (15 points)
            if row['total_images'] > 0:
                alt_coverage = (row['total_images'] - row['images_without_alt']) / row['total_images']
                score += alt_coverage * 15
            else:
                score += 15  # No images = perfect score
            
            # Content (15 points)
            if row['word_count'] >= 300:
                score += 15
            elif row['word_count'] >= 150:
                score += 10
            elif row['word_count'] > 0:
                score += 5
            
            return min(score, max_score)
        
        pages_df['seo_score'] = pages_df.apply(calculate_page_score, axis=1)
        pages_df['grade'] = pages_df['seo_score'].apply(
            lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C' if x >= 70 else 'D' if x >= 60 else 'F'
        )
        
        return pages_df
    
    def create_issue_summary(self, issues_df):
        """Create summary statistics by category and type"""
        if issues_df.empty:
            return pd.DataFrame()
        
        summary = issues_df.groupby(['category', 'type']).size().reset_index(name='count')
        summary_pivot = summary.pivot(index='category', columns='type', values='count').fillna(0)
        
        # Calculate totals
        summary_pivot['TOTAL'] = summary_pivot.sum(axis=1)
        
        # Add impact priority
        category_priority = {
            'Title': 1,
            'Meta Description': 2, 
            'Headers': 3,
            'Technical': 4,
            'Images': 5,
            'Content': 6
        }
        
        summary_pivot['Priority'] = summary_pivot.index.map(category_priority).fillna(99)
        summary_pivot = summary_pivot.sort_values('Priority')
        
        return summary_pivot
    
    def save_raw_data(self, pages_data, issues_data, scan_metadata=None):
        """Save raw scan data as JSON files for backend storage"""
        
        # Save pages data
        pages_file = os.path.join(self.scan_folder, f"pages_data_{self.domain_name}.json")
        with open(pages_file, 'w', encoding='utf-8') as f:
            json.dump(pages_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Save issues data  
        issues_file = os.path.join(self.scan_folder, f"issues_data_{self.domain_name}.json")
        with open(issues_file, 'w', encoding='utf-8') as f:
            json.dump(issues_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Save scan metadata
        if scan_metadata is None:
            scan_metadata = {
                'url': self.base_url,
                'domain': self.domain_name,
                'scan_timestamp': self.timestamp,
                'scan_date': datetime.now().isoformat(),
                'total_pages': len(pages_data),
                'total_issues': len(issues_data),
                'critical_issues': len([i for i in issues_data if i.get('type') == 'CRITICAL']),
                'warning_issues': len([i for i in issues_data if i.get('type') == 'WARNING'])
            }
        
        metadata_file = os.path.join(self.scan_folder, f"scan_metadata_{self.domain_name}.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(scan_metadata, f, indent=2, default=str, ensure_ascii=False)
        
        return {
            'pages_file': pages_file,
            'issues_file': issues_file,
            'metadata_file': metadata_file,
            'scan_folder': self.scan_folder
        }
    
    def save_csv_reports(self, pages_df, issues_df):
        """Save CSV versions of all data"""
        
        # Save issues CSV
        issues_csv = os.path.join(self.scan_folder, f"issues_{self.domain_name}.csv")
        issues_df.to_csv(issues_csv, index=False, encoding='utf-8')
        
        # Save pages CSV
        pages_csv = os.path.join(self.scan_folder, f"pages_{self.domain_name}.csv")
        pages_df.to_csv(pages_csv, index=False, encoding='utf-8')
        
        # Save summary CSV
        if not issues_df.empty:
            summary_df = self.create_issue_summary(issues_df)
            if not summary_df.empty:
                summary_csv = os.path.join(self.scan_folder, f"summary_{self.domain_name}.csv")
                summary_df.to_csv(summary_csv, encoding='utf-8')
        
        return {
            'issues_csv': issues_csv,
            'pages_csv': pages_csv,
            'scan_folder': self.scan_folder
        }
    
    def create_top_issues_list(self, issues_df, limit=20):
        """Create prioritized list of top issues to fix"""
        if issues_df.empty:
            return pd.DataFrame()
        
        prioritized = self.create_priority_matrix(issues_df.copy())
        
        top_issues = prioritized.head(limit)[['category', 'issue', 'url', 'recommendation', 'type', 'total_score']]
        top_issues['rank'] = range(1, len(top_issues) + 1)
        
        # Reorder columns
        top_issues = top_issues[['rank', 'category', 'type', 'issue', 'url', 'recommendation']]
        
        return top_issues
    
    def create_quick_wins(self, issues_df):
        """Identify quick wins - easy fixes with high impact"""
        if issues_df.empty:
            return pd.DataFrame()
        
        # Quick wins criteria
        quick_win_patterns = [
            'Missing meta description',
            'Missing H1 tag',
            'Missing title tag',
            'images missing alt text'
        ]
        
        quick_wins = issues_df[
            issues_df['issue'].str.contains('|'.join(quick_win_patterns), case=False, na=False)
        ].copy()
        
        if not quick_wins.empty:
            quick_wins = self.create_priority_matrix(quick_wins)
            quick_wins = quick_wins.head(10)[['category', 'issue', 'url', 'recommendation']]
        
        return quick_wins
    
    def create_excel_report(self, pages_df, issues_df):
        """Create comprehensive Excel report with multiple sheets"""
        excel_file = os.path.join(self.scan_folder, f"SEO_Analysis_{self.domain_name}.xlsx")
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            
            # Sheet 1: Executive Summary
            summary_data = self.create_executive_summary(pages_df, issues_df)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: Top Issues (Action Items)
            top_issues = self.create_top_issues_list(issues_df)
            if not top_issues.empty:
                top_issues.to_excel(writer, sheet_name='Top Issues', index=False)
            
            # Sheet 3: Quick Wins
            quick_wins = self.create_quick_wins(issues_df)
            if not quick_wins.empty:
                quick_wins.to_excel(writer, sheet_name='Quick Wins', index=False)
            
            # Sheet 4: Page Analysis
            page_summary = self.create_page_summary(pages_df.copy())
            key_columns = ['url', 'seo_score', 'grade', 'title_length', 'has_meta_description', 
                          'h1_count', 'total_images', 'images_without_alt', 'word_count']
            if all(col in page_summary.columns for col in key_columns):
                page_summary[key_columns].to_excel(writer, sheet_name='Page Analysis', index=False)
            else:
                page_summary.to_excel(writer, sheet_name='Page Analysis', index=False)
            
            # Sheet 5: Issues by Category
            issue_summary = self.create_issue_summary(issues_df)
            if not issue_summary.empty:
                issue_summary.to_excel(writer, sheet_name='Issues by Category')
            
            # Sheet 6: All Issues (Raw Data)
            if not issues_df.empty:
                issues_df.to_excel(writer, sheet_name='All Issues', index=False)
            
            # Sheet 7: All Pages (Raw Data)
            pages_df.to_excel(writer, sheet_name='All Pages', index=False)
        
        return excel_file
    
    def create_excel_download_buffer(self, pages_df, issues_df):
        """Create Excel report in memory buffer for download"""
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            
            # Sheet 1: Executive Summary
            summary_data = self.create_executive_summary(pages_df, issues_df)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: Top Issues (Action Items)
            top_issues = self.create_top_issues_list(issues_df)
            if not top_issues.empty:
                top_issues.to_excel(writer, sheet_name='Top Issues', index=False)
            
            # Sheet 3: Quick Wins
            quick_wins = self.create_quick_wins(issues_df)
            if not quick_wins.empty:
                quick_wins.to_excel(writer, sheet_name='Quick Wins', index=False)
            
            # Sheet 4: Page Analysis
            page_summary = self.create_page_summary(pages_df.copy())
            key_columns = ['url', 'seo_score', 'grade', 'title_length', 'has_meta_description', 
                          'h1_count', 'total_images', 'images_without_alt', 'word_count']
            if all(col in page_summary.columns for col in key_columns):
                page_summary[key_columns].to_excel(writer, sheet_name='Page Analysis', index=False)
            else:
                page_summary.to_excel(writer, sheet_name='Page Analysis', index=False)
            
            # Sheet 5: Issues by Category
            issue_summary = self.create_issue_summary(issues_df)
            if not issue_summary.empty:
                issue_summary.to_excel(writer, sheet_name='Issues by Category')
            
            # Sheet 6: All Issues (Raw Data)
            if not issues_df.empty:
                issues_df.to_excel(writer, sheet_name='All Issues', index=False)
            
            # Sheet 7: All Pages (Raw Data)
            pages_df.to_excel(writer, sheet_name='All Pages', index=False)
        
        buffer.seek(0)
        return buffer
    
    def create_executive_summary(self, pages_df, issues_df):
        """Create executive summary data"""
        total_pages = len(pages_df)
        critical_issues = len(issues_df[issues_df['type'] == 'CRITICAL']) if not issues_df.empty else 0
        warning_issues = len(issues_df[issues_df['type'] == 'WARNING']) if not issues_df.empty else 0
        
        # Calculate metrics
        pages_with_title = pages_df['title'].notna().sum() if not pages_df.empty else 0
        pages_with_meta = pages_df['has_meta_description'].sum() if not pages_df.empty else 0
        pages_with_h1 = (pages_df['h1_count'] > 0).sum() if not pages_df.empty else 0
        total_images = pages_df['total_images'].sum() if not pages_df.empty else 0
        images_without_alt = pages_df['images_without_alt'].sum() if not pages_df.empty else 0
        
        # Calculate scores
        avg_seo_score = pages_df['seo_score'].mean() if 'seo_score' in pages_df.columns else 0
        
        summary_data = [
            ['Metric', 'Value', 'Percentage', 'Grade'],
            ['Website', self.base_url, '', ''],
            ['Scan Date', datetime.now().strftime('%Y-%m-%d %H:%M'), '', ''],
            ['Pages Analyzed', total_pages, '', ''],
            ['', '', '', ''],
            ['CRITICAL ISSUES', critical_issues, '', 'F' if critical_issues > 5 else 'C' if critical_issues > 0 else 'A'],
            ['WARNING ISSUES', warning_issues, '', 'F' if warning_issues > 10 else 'C' if warning_issues > 5 else 'A'],
            ['', '', '', ''],
            ['Pages with Titles', f"{pages_with_title}/{total_pages}", f"{pages_with_title/total_pages*100:.1f}%" if total_pages > 0 else "0%", self._get_grade(pages_with_title/total_pages if total_pages > 0 else 0)],
            ['Pages with Meta Descriptions', f"{pages_with_meta}/{total_pages}", f"{pages_with_meta/total_pages*100:.1f}%" if total_pages > 0 else "0%", self._get_grade(pages_with_meta/total_pages if total_pages > 0 else 0)],
            ['Pages with H1 Tags', f"{pages_with_h1}/{total_pages}", f"{pages_with_h1/total_pages*100:.1f}%" if total_pages > 0 else "0%", self._get_grade(pages_with_h1/total_pages if total_pages > 0 else 0)],
            ['Image Alt Text Coverage', f"{total_images-images_without_alt}/{total_images}" if total_images > 0 else "0/0", f"{(total_images-images_without_alt)/total_images*100:.1f}%" if total_images > 0 else "100%", self._get_grade((total_images-images_without_alt)/total_images if total_images > 0 else 1)],
            ['', '', '', ''],
            ['Average SEO Score', f"{avg_seo_score:.1f}/100", '', self._get_grade(avg_seo_score/100)],
        ]
        
        return summary_data
    
    def _get_grade(self, percentage):
        """Convert percentage to letter grade"""
        if percentage >= 0.9:
            return 'A'
        elif percentage >= 0.8:
            return 'B'
        elif percentage >= 0.7:
            return 'C'
        elif percentage >= 0.6:
            return 'D'
        else:
            return 'F'
    
    def create_console_report(self, pages_df, issues_df):
        """Create enhanced console output"""
        
        print("\n" + "="*80)
        print(f"📊 ENHANCED SEO ANALYSIS - {self.domain_name.upper()}")
        print("="*80)
        
        # Quick stats
        total_pages = len(pages_df)
        critical_count = len(issues_df[issues_df['type'] == 'CRITICAL']) if not issues_df.empty else 0
        warning_count = len(issues_df[issues_df['type'] == 'WARNING']) if not issues_df.empty else 0
        
        print(f"📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📄 Pages Analyzed: {total_pages}")
        print(f"🚨 Critical Issues: {critical_count}")
        print(f"⚠️  Warning Issues: {warning_count}")
        
        # Top 5 Issues
        if not issues_df.empty:
            print(f"\n🎯 TOP 5 PRIORITY FIXES:")
            print("-" * 50)
            top_issues = self.create_top_issues_list(issues_df, limit=5)
            for _, issue in top_issues.iterrows():
                print(f"{issue['rank']}. {issue['category']}: {issue['issue']}")
                url_display = issue['url'][:60] + '...' if len(issue['url']) > 60 else issue['url']
                print(f"   🔗 {url_display}")
                print(f"   💡 {issue['recommendation']}\n")
        
        # Quick Wins
        quick_wins = self.create_quick_wins(issues_df)
        if not quick_wins.empty:
            print(f"⚡ QUICK WINS (Easy fixes with high impact):")
            print("-" * 50)
            for _, win in quick_wins.head(3).iterrows():
                print(f"• {win['category']}: {win['issue']}")
                print(f"  💡 {win['recommendation']}\n")
        
        print("="*80)
    
    def generate_reports(self, pages_data, issues_data, scan_metadata=None):
        """Main function to generate all reports with backend storage"""
        
        # Convert to DataFrames
        pages_df = pd.DataFrame(pages_data)
        issues_df = pd.DataFrame(issues_data)
        
        # Add SEO scores to pages
        pages_df = self.create_page_summary(pages_df)
        
        # Save raw data to backend storage
        raw_files = self.save_raw_data(pages_data, issues_data, scan_metadata)
        
        # Save CSV reports
        csv_files = self.save_csv_reports(pages_df, issues_df)
        
        # Create Excel report (also saved to backend)
        excel_file = self.create_excel_report(pages_df, issues_df)
        
        # Print enhanced console report
        self.create_console_report(pages_df, issues_df)
        
        print(f"\n📊 Comprehensive Excel report saved to: {excel_file}")
        print(f"💾 Backend storage folder: {self.scan_folder}")
        print("📈 Open the Excel file for detailed analysis and action items!")
        
        # Return all file paths for reference
        return {
            'excel_file': excel_file,
            'scan_folder': self.scan_folder,
            'raw_files': raw_files,
            'csv_files': csv_files,
            'backend_storage_dir': self.backend_storage_dir
        }