import os
import json
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def sanitize_filename(name):
    # Keep only alphanumeric characters, spaces, and hyphens, then convert spaces to underscores
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    return re.sub(r'[-\s]+', '_', name)

def download_and_process_docs():
    seed_path = os.path.join(os.path.dirname(__file__), "seed_urls.json")
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(seed_path):
        print(f"Error: seed_urls.json not found at {seed_path}")
        return

    with open(seed_path, 'r') as f:
        urls_data = json.load(f)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for idx, entry in enumerate(urls_data):
        url = entry["url"]
        service = entry["service"]
        print(f"Processing ({idx+1}/{len(urls_data)}): {url} ...")

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Decompose scripts, styles, navigation, footer, header
        for tag in ["script", "style", "nav", "header", "footer", "noscript"]:
            for element in soup.find_all(tag):
                element.decompose()

        # Try to find the main content
        main_content = soup.find(id="main-content") or soup.find(id="main-col-body")
        if not main_content:
            # Fallback to article or body if not found
            main_content = soup.find("article") or soup.find("body")

        if not main_content:
            print(f"Warning: Could not find main content for {url}. Skipping.")
            continue

        # Extract title
        title_tag = main_content.find("h1") or soup.find("title")
        title = title_tag.get_text().strip() if title_tag else f"AWS Document {idx}"

        # Clean title if it contains suffixes
        title = re.sub(r'\s*-\s*AWS.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*-\s*Amazon.*$', '', title, flags=re.IGNORECASE)

        # Convert to markdown
        markdown_text = md(str(main_content), heading_style="ATX").strip()

        # Build YAML frontmatter
        frontmatter = (
            "---\n"
            f"title: \"{title}\"\n"
            f"url: \"{url}\"\n"
            f"service: \"{service}\"\n"
            "---\n\n"
        )

        full_content = frontmatter + markdown_text

        filename = f"{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f_out:
            f_out.write(full_content)

        print(f"Saved: {filename}")

if __name__ == "__main__":
    download_and_process_docs()
