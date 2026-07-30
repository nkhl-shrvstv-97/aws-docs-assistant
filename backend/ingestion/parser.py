import re

def parse_markdown_with_frontmatter(file_content: str):
    """
    Parses a markdown file content that starts with a YAML frontmatter block.
    Example:
    ---
    title: "Creating S3 Bucket"
    url: "https://..."
    service: "AmazonS3"
    ---
    Markdown body...
    """
    metadata = {}
    body = file_content
    
    # Check if the content starts with frontmatter markers
    if file_content.startswith("---"):
        parts = file_content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            body = parts[2].strip()
            
            # Simple line-by-line parsing of key: "value" or key: value
            for line in frontmatter_text.strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    # Strip surrounding quotes if present
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    metadata[key] = val
                    
    return metadata, body
