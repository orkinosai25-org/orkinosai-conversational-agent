"""Account model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Account(Base):
    """Account model for SaaS tenant/organization management"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    
    # Subscription and limits
    subscription_tier = Column(String, default="free")  # free, basic, premium, enterprise
    is_active = Column(Boolean, default=True)
    max_agents = Column(Integer, default=1)
    max_users = Column(Integer, default=1)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    # Relationships
    users = relationship("User", back_populates="account")
    agents = relationship("Agent", back_populates="account", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Account(id={self.id}, name={self.name}, slug={self.slug})>"
