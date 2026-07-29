import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "us-east-1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aws_docs"
    BEDROCK_EMBED_MODEL_ID: str = "amazon.titan-embed-text-v2:0"
    BEDROCK_CLASSIFY_MODEL_ID: str = "anthropic.claude-3-haiku-20240307-v1:0"
    BEDROCK_GENERATE_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    TAVILY_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
