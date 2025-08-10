#!/usr/bin/env python3
"""
Backend Admin Tool for SEO Scanner
Provides command-line access to all stored scans and reports
"""

import os
import json
import pandas as pd
from datetime import datetime
import argparse
import sys

class BackendAdmin:
    def __init__(self):
        self.backend_path = os.path.join("reports", "backend_storage")
        
    def list_all_scans(self):
        """List all scans in backend storage"""
        if not os.path.exists(self.backend_path):
            print("ERROR: Backend storage directory not found")
            return
        
        scan_folders = [f for f in os.listdir(self.backend_path) if os.path.isdir(os.path.join(self.backend_path, f))]
        scan_folders.sort(reverse=True)  # Most recent first
        
        print(f"\nBACKEND STORAGE REPORT")
        print(f"{'='*60}")
        print(f"Storage Path: {os.path.abspath(self.backend_path)}")
        print(f"Total Scans: {len(scan_folders)}")
        print(f"{'='*60}\n")
        
        if not scan_folders:
            print("No scans found in backend storage")
            return
        
        print(f"{'Domain':<20} {'Date':<12} {'Pages':<6} {'Issues':<7} {'Folder'}")
        print(f"{'-'*60}")
        
        for folder in scan_folders:
            folder_path = os.path.join(self.backend_path, folder)
            try:
                # Find metadata file
                metadata_file = None
                for file in os.listdir(folder_path):
                    if file.startswith("scan_metadata_"):
                        metadata_file = os.path.join(folder_path, file)
                        break
                
                if metadata_file and os.path.exists(metadata_file):
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    domain = metadata.get('domain', folder.split('_')[0])[:19]
                    scan_date = metadata.get('scan_date', 'Unknown')[:10]
                    pages = metadata.get('total_pages', 0)
                    issues = metadata.get('total_issues', 0)
                    
                    print(f"{domain:<20} {scan_date:<12} {pages:<6} {issues:<7} {folder}")
                else:
                    print(f"{folder.split('_')[0]:<20} {'Unknown':<12} {'?':<6} {'?':<7} {folder}")
                    
            except Exception as e:
                print(f"{folder.split('_')[0]:<20} {'Error':<12} {'?':<6} {'?':<7} {folder}")
    
    def scan_details(self, scan_folder):
        """Show detailed information about a specific scan"""
        folder_path = os.path.join(self.backend_path, scan_folder)
        
        if not os.path.exists(folder_path):
            print(f"ERROR: Scan folder not found: {scan_folder}")
            return
        
        print(f"\nSCAN DETAILS: SCAN DETAILS: {scan_folder}")
        print(f"{'='*60}")
        
        # List all files in the folder
        files = os.listdir(folder_path)
        print(f"Folder: Folder: {os.path.abspath(folder_path)}")
        print(f"File: Files: {len(files)}")
        
        # Show metadata if available
        metadata_file = None
        for file in files:
            if file.startswith("scan_metadata_"):
                metadata_file = os.path.join(folder_path, file)
                break
        
        if metadata_file:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            print(f"\nMETADATA: METADATA:")
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        
        print(f"\nFILES IN SCAN FOLDER: FILES IN SCAN FOLDER:")
        for file in sorted(files):
            file_path = os.path.join(folder_path, file)
            file_size = os.path.getsize(file_path)
            print(f"  File: {file} ({file_size:,} bytes)")
    
    def export_scan_data(self, scan_folder, output_dir="exported_scans"):
        """Export a scan's data to a new directory"""
        source_path = os.path.join(self.backend_path, scan_folder)
        
        if not os.path.exists(source_path):
            print(f"ERROR: Scan folder not found: {scan_folder}")
            return
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        export_path = os.path.join(output_dir, scan_folder)
        
        # Copy files
        import shutil
        shutil.copytree(source_path, export_path, dirs_exist_ok=True)
        
        print(f"SUCCESS: Scan data exported to: {os.path.abspath(export_path)}")
    
    def cleanup_old_scans(self, keep_days=30):
        """Remove scans older than specified days"""
        if not os.path.exists(self.backend_path):
            print("ERROR: Backend storage directory not found")
            return
        
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        removed_count = 0
        
        scan_folders = [f for f in os.listdir(self.backend_path) if os.path.isdir(os.path.join(self.backend_path, f))]
        
        for folder in scan_folders:
            folder_path = os.path.join(self.backend_path, folder)
            folder_modified = os.path.getmtime(folder_path)
            
            if folder_modified < cutoff_date:
                import shutil
                shutil.rmtree(folder_path)
                removed_count += 1
                print(f"REMOVED:  Removed old scan: {folder}")
        
        print(f"SUCCESS: Cleanup complete. Removed {removed_count} old scans (older than {keep_days} days)")

def main():
    parser = argparse.ArgumentParser(description="SEO Scanner Backend Admin Tool")
    parser.add_argument("command", choices=["list", "details", "export", "cleanup"], 
                       help="Command to execute")
    parser.add_argument("--folder", help="Scan folder name (for details/export commands)")
    parser.add_argument("--days", type=int, default=30, help="Days to keep for cleanup (default: 30)")
    parser.add_argument("--output", default="exported_scans", help="Output directory for exports")
    
    args = parser.parse_args()
    admin = BackendAdmin()
    
    if args.command == "list":
        admin.list_all_scans()
    
    elif args.command == "details":
        if not args.folder:
            print("ERROR: --folder argument required for details command")
            sys.exit(1)
        admin.scan_details(args.folder)
    
    elif args.command == "export":
        if not args.folder:
            print("ERROR: --folder argument required for export command")
            sys.exit(1)
        admin.export_scan_data(args.folder, args.output)
    
    elif args.command == "cleanup":
        admin.cleanup_old_scans(args.days)

if __name__ == "__main__":
    main()