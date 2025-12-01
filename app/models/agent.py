"""Agent model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Agent(Base):
    """Agent model for conversational AI agents"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Agent configuration
    agent_type = Column(String, default="conversational")  # conversational, task-based, etc.
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # Training and knowledge
    training_status = Column(String, default="untrained")  # untrained, training, trained, failed
    knowledge_sources = Column(JSON, default=list)  # List of URLs, documents, etc.
    configuration = Column(JSON, default=dict)  # Agent-specific configuration
    
    # Azure AI configuration (placeholder)
    azure_deployment_id = Column(String, nullable=True)
    azure_model_version = Column(String, nullable=True)
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="agents")
    
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="agents")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_trained_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name}, type={self.agent_type})>"
