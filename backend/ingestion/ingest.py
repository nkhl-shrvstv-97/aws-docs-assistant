import os
import glob
from langchain_text_splitters import MarkdownTextSplitter
from backend.app.db.session import SessionLocal
from backend.app.db.models import DocumentChunk
from backend.app.tools.vector_store import get_embedding
from backend.ingestion.parser import parse_markdown_with_frontmatter

def ingest_local_docs():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    
    if not md_files:
        print(f"No markdown files found in {data_dir}. Run download_docs.py first.")
        return

    # Configure Markdown text splitter
    splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
    db = SessionLocal()

    print(f"Found {len(md_files)} files for ingestion.")

    try:
        for filepath in md_files:
            print(f"Ingesting: {os.path.basename(filepath)}...")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            metadata, body = parse_markdown_with_frontmatter(content)
            title = metadata.get("title", "Unknown Title")
            url = metadata.get("url", "")
            service = metadata.get("service", "Unknown Service")

            # Split the markdown body text
            chunks = splitter.split_text(body)
            print(f"Split into {len(chunks)} chunks.")

            for idx, chunk_text in enumerate(chunks):
                # We skip embedding empty chunks
                if not chunk_text.strip():
                    continue
                
                print(f"  Embedding chunk {idx+1}/{len(chunks)}...")
                embedding = get_embedding(chunk_text)

                doc_chunk = DocumentChunk(
                    content=chunk_text,
                    embedding=embedding,
                    source_url=url,
                    title=title,
                    service_name=service
                )
                db.add(doc_chunk)
            
            db.commit()
            print(f"Successfully committed all chunks for: {title}")

    except Exception as e:
        print(f"Error during ingestion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    ingest_local_docs()
