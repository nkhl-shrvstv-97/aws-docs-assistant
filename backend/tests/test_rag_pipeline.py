import pytest
from backend.ingestion.parser import parse_markdown_with_frontmatter
from langchain_text_splitters import MarkdownTextSplitter

def test_parse_markdown_with_frontmatter():
    markdown_content = """---
title: "Creating an Amazon S3 Bucket"
url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html"
service: "AmazonS3"
---
# Creating an Amazon S3 Bucket
This is some content about Amazon S3.
"""
    metadata, body = parse_markdown_with_frontmatter(markdown_content)
    
    assert metadata["title"] == "Creating an Amazon S3 Bucket"
    assert metadata["url"] == "https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html"
    assert metadata["service"] == "AmazonS3"
    assert "# Creating an Amazon S3 Bucket" in body

def test_markdown_splitter():
    text = """# Header 1
Content under header 1.
## Header 2
Content under header 2 with some long text to make sure splitting works correctly.
"""
    splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = splitter.split_text(text)
    
    assert len(chunks) > 0
    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk) <= 100
