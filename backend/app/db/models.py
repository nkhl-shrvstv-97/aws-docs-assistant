import uuid
from sqlalchemy import Column, String, Text, DateTime, text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from backend.app.db.session import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    source_url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    service_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class SessionSummary(Base):
    __tablename__ = "session_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    session_id = Column(String(100), unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    topics = Column(ARRAY(String(255)), nullable=False)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
