import os
import json
import urllib.parse
import boto3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain_text_splitters import MarkdownTextSplitter
from backend.ingestion.parser import parse_markdown_with_frontmatter

# Initialize clients
s3_client = boto3.client("s3")
bedrock_client = boto3.client(service_name="bedrock-runtime")
secrets_client = boto3.client(service_name="secretsmanager")

# Environment variables (configured in Terraform)
DB_SECRET_ARN = os.environ.get("DB_SECRET_ARN")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME", "us-east-1")
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"

def get_db_connection_url():
    """
    Fetch DB credentials from AWS Secrets Manager and construct SQLAlchemy URL.
    """
    if not DB_SECRET_ARN:
        raise ValueError("DB_SECRET_ARN environment variable is not set")
    
    try:
        response = secrets_client.get_secret_value(SecretId=DB_SECRET_ARN)
        secret = json.loads(response["SecretString"])
        
        username = secret["username"]
        password = secret["password"]
        host = secret["host"]
        port = secret.get("port", 5432)
        dbname = secret.get("dbInstanceIdentifier", secret.get("dbname", "aws_docs"))
        
        # Escape credentials properly
        password_escaped = urllib.parse.quote_plus(password)
        
        return f"postgresql://{username}:{password_escaped}@{host}:{port}/{dbname}"
    except Exception as e:
        print(f"Failed to retrieve database secret: {e}")
        raise e

# Setup Database connection lazily
engine = None
SessionLocal = None

def get_db_session():
    global engine, SessionLocal
    if SessionLocal is None:
        db_url = get_db_connection_url()
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_embedding(text_content: str) -> list:
    """
    Invoke Bedrock to get the embedding vector.
    """
    payload = {
        "inputText": text_content,
        "dimensions": 1536,
        "normalize": True
    }
    
    response = bedrock_client.invoke_model(
        modelId=EMBED_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")

def lambda_handler(event, context):
    """
    SQS Event triggered Lambda function.
    Reads records, downloads target files from S3, chunks, embeds and saves to RDS Postgres.
    """
    print(f"Received event: {json.dumps(event)}")
    
    db = None
    try:
        db = get_db_session()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return {"statusCode": 500, "body": "DB Connection Error"}
        
    splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    # Process SQS batch records
    for record in event.get("Records", []):
        try:
            # SQS event body contains S3 event JSON
            sqs_body = json.loads(record["body"])
            
            # SQS Test messages or other notifications may not contain Records
            if "Records" not in sqs_body:
                print("Skipping non-S3 event notification in SQS body.")
                continue
                
            for s3_record in sqs_body["Records"]:
                bucket_name = s3_record["s3"]["bucket"]["name"]
                object_key = urllib.parse.unquote_plus(s3_record["s3"]["object"]["key"])
                
                print(f"Processing file from S3: s3://{bucket_name}/{object_key}")
                
                # Download file from S3
                s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                file_content = s3_response["Body"].read().decode("utf-8")
                
                # Parse markdown frontmatter and body
                metadata, body = parse_markdown_with_frontmatter(file_content)
                title = metadata.get("title", os.path.basename(object_key))
                url = metadata.get("url", "")
                service = metadata.get("service", "Unknown")
                
                # Chunk the markdown body
                chunks = splitter.split_text(body)
                print(f"Splitting '{title}' into {len(chunks)} chunks.")
                
                # Generate embeddings and save to DB
                for idx, chunk_text in enumerate(chunks):
                    if not chunk_text.strip():
                        continue
                    
                    embedding = get_embedding(chunk_text)
                    
                    # Convert embedding list to standard pgvector format
                    emb_str = f"[{','.join(map(str, embedding))}]"
                    
                    sql = text("""
                        INSERT INTO document_chunks (content, embedding, source_url, title, service_name)
                        VALUES (:content, :embedding::vector, :source_url, :title, :service_name)
                    """)
                    
                    db.execute(sql, {
                        "content": chunk_text,
                        "embedding": emb_str,
                        "source_url": url,
                        "title": title,
                        "service_name": service
                    })
                    
                db.commit()
                print(f"Successfully indexed all chunks for: {title}")
                
        except Exception as record_err:
            print(f"Error processing record: {record_err}")
            if db:
                db.rollback()
            continue
            
    if db:
        db.close()
        
    return {"statusCode": 200, "body": "Processed batch successfully"}
