#!/usr/bin/env python3
"""
Setup script for SEO Scanner
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="seo-scanner",
    version="1.0.0",
    author="Spencer Buck",
    author_email="spencer.buck4@gmail.com",
    description="A comprehensive SEO analysis tool that generates detailed reports with actionable insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbuck4/seo-scanner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "seo-scanner=main:main",
        ],
    },
    keywords="seo, analysis, website, crawler, optimization, marketing",
    project_urls={
        "Bug Reports": "https://github.com/sbuck4/seo-scanner/issues",
        "Source": "https://github.com/sbuck4/seo-scanner",
        "Documentation": "https://github.com/sbuck4/seo-scanner#readme",
    },
)