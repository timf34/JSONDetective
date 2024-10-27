# setup.py
from setuptools import setup, find_packages

setup(
    name="jsondetective",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "click>=7.1.2",
    ],
    entry_points={
        "console_scripts": [
            "jsondetective=jsondetective.cli:main",
        ],
    },
    author="timf34",
    author_email="timf34@gmail.com",
    description="A tool for analyzing JSON structures and generating Python dataclasses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jsondetective",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)