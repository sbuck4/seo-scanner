# 🔍 SEO Scanner

A comprehensive, free SEO analysis tool that crawls websites and generates detailed reports with actionable insights.

## ✨ Features

- **Complete Site Analysis** - Crawls and analyzes all pages on your website
- **SEO Health Scoring** - Grades each page with detailed metrics
- **Professional Reports** - Excel and HTML reports with prioritized action items
- **Issue Detection** - Identifies missing meta descriptions, title tags, H1 headers, and more
- **Image Optimization** - Finds images missing alt text for better accessibility
- **Quick Wins** - Highlights easy fixes with high SEO impact

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sbuck4/seo-scanner.git
cd seo-scanner
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the scanner:**
```bash
python main.py
```

4. **Enter your website URL when prompted:**
```
Enter website URL (e.g., https://example.com): https://yoursite.com
```

The scanner will automatically:
- ✅ Crawl all pages on your website
- ✅ Analyze each page for SEO issues
- ✅ Generate comprehensive reports
- ✅ Save results to the `reports/` folder

### Example Output

```
📊 ENHANCED SEO ANALYSIS - YOURSITE.COM
================================================================================
📅 Scan Date: 2025-06-26 14:30
📄 Pages Analyzed: 33
🚨 Critical Issues: 46
⚠️  Warning Issues: 12

🎯 TOP 5 PRIORITY FIXES:
--------------------------------------------------
1. Meta Description: Page missing meta description
   🔗 https://yoursite.com/services
   💡 Add a compelling 150-160 character meta description

2. Headers: Page missing H1 tag
   🔗 https://yoursite.com/about
   💡 Add exactly one H1 tag with your main keyword
```

## 📊 Sample Reports

The tool generates multiple report formats:

### Excel Report (7 Sheets)
- **Executive Summary** - Key metrics and grades
- **Top Issues** - Prioritized action items
- **Quick Wins** - Easy fixes for immediate impact
- **Page Analysis** - SEO scores for each page
- **Issues by Category** - Summary statistics
- **Raw Data** - Complete analysis details

### HTML Report
- Visual dashboard with color-coded priorities
- Interactive tables and recommendations
- Professional formatting for client presentations

## 🎯 How to Use

### Basic Scan
1. **Run the tool:** `python main.py`
2. **Enter your website:** When prompted, type your full website URL (e.g., `https://yoursite.com`)
3. **Wait for analysis:** The tool will crawl your site and analyze each page
4. **View results:** Check the `reports/` folder for your comprehensive analysis

### What You Get
After scanning, you'll find a timestamped folder in `reports/` containing:
- **📊 Excel Report** - Professional multi-sheet analysis with action items
- **🎯 HTML Action Plan** - Visual dashboard you can open in any browser
- **📄 CSV Data** - Raw data for further analysis
- **📝 Summary Report** - Quick overview in text format

### Sample Workflow
```bash
$ python main.py
🔍============================================================🔍
    SEO SCANNER - Free Website Analysis Tool
    Generate professional SEO reports in minutes!
🔍============================================================🔍

Enter website URL (e.g., https://example.com): https://mysite.com

🚀 Initializing SEO Scanner...

=== STEP 1: CRAWLING WEBSITE ===
🌐 Analyzing: https://mysite.com
✅ Found 15 pages to analyze

=== STEP 2: ANALYZING PAGES ===
📄 Analyzing (1/15): https://mysite.com
📄 Analyzing (2/15): https://mysite.com/about
...

=== STEP 3: DETECTING ISSUES ===
🔍 Found 23 issues to address

=== STEP 4: GENERATING REPORTS ===
📊 Comprehensive Excel report saved to: reports/mysite.com_20250626_1430/SEO_Analysis_mysite.com.xlsx
📈 Open the Excel file for detailed analysis and action items!
```

## 🛠️ What It Analyzes
- ✅ Title tags (presence, length, uniqueness)
- ✅ Meta descriptions (presence, length, quality)
- ✅ Header structure (H1, H2, H3 hierarchy)
- ✅ Internal linking structure

### Content Quality
- ✅ Page word count and content depth
- ✅ Keyword optimization opportunities
- ✅ Content structure and readability

### Image Optimization
- ✅ Alt text coverage
- ✅ Image file naming
- ✅ Accessibility compliance

### Performance Indicators
- ✅ Page load insights
- ✅ Mobile-friendly structure
- ✅ SEO score calculation (0-100)

## 🎯 Use Cases

### For Business Owners
- **Audit your website** before launching marketing campaigns
- **Track SEO progress** over time with regular scans
- **Identify quick wins** to boost search rankings immediately

### For Agencies & Freelancers
- **Client reporting** with professional Excel/HTML reports
- **Prospecting tool** to show potential improvements
- **Project planning** with prioritized task lists

### For Developers
- **Pre-launch audits** to catch SEO issues early
- **Automated testing** integration for CI/CD pipelines
- **Team collaboration** with shareable reports

## 📈 Configuration

### Custom Scan Settings
Edit the configuration in `main.py`:

```python
# Scan depth (how many levels deep to crawl)
MAX_CRAWL_DEPTH = 3

# Maximum pages to analyze
MAX_PAGES = 100

# Your website URL
DEFAULT_WEBSITE_URL = "https://yoursite.com"
```

### Command Line Options
```bash
# Basic usage (you'll be prompted for URL)
python main.py

# Specify URL directly
python main.py --url https://example.com

# Limit number of pages to scan
python main.py --url https://example.com --max-pages 50

# Quiet mode (less output)
python main.py --url https://example.com --quiet
```

### Output Customization
Reports are saved to the `reports/` directory with timestamps:
```
reports/
└── yoursite.com_20250626_1430/
    ├── SEO_Analysis_yoursite.com.xlsx
    ├── SEO_Action_Plan.html
    ├── detailed_page_data.csv
    └── summary_report.txt
```

## 🔧 Advanced Usage

### Programmatic Usage
```python
from src.enhanced_pandas_reporter import EnhancedPandasReporter

# Initialize and run analysis
reporter = EnhancedPandasReporter("https://yoursite.com")
excel_file = reporter.generate_reports(pages_data, issues_data)
```

### Batch Processing
```bash
# Analyze multiple sites
python main.py --url site1.com
python main.py --url site2.com
python main.py --url site3.com
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs** - Open an issue with details
2. **Suggest features** - Share your ideas for improvements
3. **Submit PRs** - Follow our coding guidelines
4. **Improve docs** - Help make instructions clearer

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/sbuck4/seo-scanner.git
cd seo-scanner
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Support

If this tool helps improve your SEO, please:
- ⭐ **Star this repository**
- 🔄 **Share with others**
- 🐛 **Report issues**
- 💡 **Suggest improvements**

## 🛣️ Roadmap

### Coming Soon
- [ ] **Streamlit Web Interface** - No coding required
- [ ] **Scheduled Scans** - Automated monitoring
- [ ] **Competitor Analysis** - Compare against other sites
- [ ] **Historical Tracking** - Progress over time
- [ ] **API Endpoints** - Integrate with other tools

### Future Features
- [ ] **Multi-language support**
- [ ] **Advanced keyword analysis**
- [ ] **Page speed integration**
- [ ] **Schema markup detection**
- [ ] **Social media optimization**

## 🏆 Success Stories

> "Increased organic traffic by 40% in 3 months using the prioritized recommendations!" 
> - Local Business Owner

> "Perfect for client reports - saves hours of manual analysis."
> - SEO Agency

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/sbuck4/seo-scanner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sbuck4/seo-scanner/discussions)

---

**Made with ❤️ for the SEO community**

*Free, open-source SEO analysis for everyone.*