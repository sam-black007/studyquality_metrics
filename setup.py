"""
AI Study Focus Monitor - Setup Configuration

This file allows the package to be installed via pip:
    pip install -e .
or
    pip install git+https://github.com/yourusername/study-focus-monitor.git
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="study-focus-monitor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered study focus monitoring system using webcam and screen analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/study-focus-monitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "opencv-python>=4.9.0",
        "mediapipe>=0.10.9",
        "numpy>=1.26.0",
        "pillow>=10.2.0",
        "mss>=9.0.0",
        "tensorflow-cpu>=2.13.0",
        "pandas>=2.1.0",
        "matplotlib>=3.8.0",
        "plotly>=5.18.0",
        "pynput>=1.7.6",
        "pyyaml>=6.0",
        "scikit-learn>=1.4.0",
        "scipy>=1.11.0",
    ],
    entry_points={
        'console_scripts': [
            'study-monitor=main:main',
            'study-report=modules.report_generator:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config/*.yaml'],
    },
)
