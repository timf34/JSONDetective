from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="jsondetective",
    version="1.0.2",
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
    author="Tim Farrelly",
    author_email="timf34@gmail.com",
    description="Instantly understand JSON structure through automatic schema inference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timf34/jsondetective",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)