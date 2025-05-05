# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gnazhpo",
    version="0.1.0",
    author="",  # Add author name if desired
    author_email="", # Add author email if desired
    description="A general-purpose utility for processing items and managing space.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # Add project URL if available (e.g., GitHub repo)
    packages=find_packages(where=".", include=["gnapo", "gnapo.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming MIT, change if needed
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["pyTelegramBotAPI"], # Added dependency for dispatch feature
    include_package_data=True, # To include files specified in MANIFEST.in
)

