"""
Modern setup configuration for Snake Game

Uses setuptools instead of deprecated distutils for Python 3.12+ compatibility.
"""

from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else ""

setup(
    name="snake-game",
    version="2.0.0",
    description="A modernized Snake game implementation using pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Snake Game Developer",
    author_email="developer@example.com",
    url="https://github.com/sandraslalom/snake-game",
    
    # Classifiers help users find your project by categorizing it
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Arcade",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    
    keywords="game, snake, pygame, arcade",
    
    # Package discovery
    packages=find_packages(where="."),
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "pygame>=2.0.0",
    ],
    
    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "build": [
            "pyinstaller>=4.0",
            "cx_Freeze>=6.0",
        ],
    },
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "snake-game=game_modernized:main",
        ],
    },
    
    # Additional files to include in the package
    package_data={
        "": ["*.md", "*.txt", "*.cfg"],
    },
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/sandraslalom/snake-game/issues",
        "Source": "https://github.com/sandraslalom/snake-game",
        "Documentation": "https://github.com/sandraslalom/snake-game/blob/main/README.md",
    },
)