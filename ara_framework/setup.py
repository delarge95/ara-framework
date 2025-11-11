"""
Setup script for ARA Framework.

Install:
    pip install -e .

Then use CLI:
    ara run "Rust WASM for audio"
    ara budget
    ara test
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ara-framework",
    version="1.0.0",
    description="🔬 Automated Research & Analysis Framework - Multi-agent system for niche analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ARA Framework Team",
    author_email="ara@example.com",
    url="https://github.com/yourusername/ara-framework",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    python_requires=">=3.11",
    install_requires=[
        "crewai>=0.80.0",
        "crewai-tools>=0.12.0",
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "openai>=1.10.0",
        "anthropic>=0.18.0",
        "google-generativeai>=0.3.0",
        "mcp>=0.9.0",
        "playwright>=1.42.0",
        "httpx>=0.26.0",
        "aiofiles>=23.2.1",
        "semanticscholar>=0.8.0",
        "arxiv>=2.1.0",
        "unstructured[pdf]>=0.12.0",
        "pymupdf>=1.23.0",
        "markitdown>=0.0.1",
        "beautifulsoup4>=4.12.0",
        "lxml>=5.0.0",
        "redis>=5.0.0",
        "hiredis>=2.3.0",
        "supabase>=2.3.0",
        "opentelemetry-api>=1.22.0",
        "opentelemetry-sdk>=1.22.0",
        "typer>=0.9.0",
        "rich>=13.7.0",
        "structlog>=24.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pybreaker>=1.0.0",
            "black>=23.12.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ara=cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ai agents crewai research analysis automation mcp",
    project_urls={
        "Documentation": "https://github.com/yourusername/ara-framework#readme",
        "Source": "https://github.com/yourusername/ara-framework",
        "Issues": "https://github.com/yourusername/ara-framework/issues",
    },
)
