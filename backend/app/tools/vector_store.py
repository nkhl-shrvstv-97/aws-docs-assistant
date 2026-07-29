import json
import boto3
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.config import settings
from backend.app.db.models import DocumentChunk

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=settings.AWS_REGION
)

def get_embedding(text_content: str) -> list:
    """
    Generate 1536-dimension normalized embedding using amazon.titan-embed-text-v2:0
    """
    payload = {
        "inputText": text_content,
        "dimensions": 1536,
        "normalize": True
    }
    
    try:
        response = bedrock_client.invoke_model(
            modelId=settings.BEDROCK_EMBED_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")
    except Exception as e:
        print(f"Error generating embedding from Bedrock: {e}")
        raise e

def similarity_search(db: Session, query: str, limit: int = 5):
    """
    Perform a similarity search in PostgreSQL using the pgvector cosine distance operator (<=>).
    """
    query_embedding = get_embedding(query)
    
    # Cast query embedding list to string representation for pgvector
    emb_str = f"[{','.join(map(str, query_embedding))}]"
    
    # Raw SQL execution using standard pgvector <=> operator
    sql = text("""
        SELECT id, content, source_url, title, service_name, (embedding <=> :query_embedding) AS distance
        FROM document_chunks
        ORDER BY distance ASC
        LIMIT :limit
    """)
    
    result = db.execute(sql, {"query_embedding": emb_str, "limit": limit})
    return [dict(row._mapping) for row in result]
