"""Training routes for agent knowledge management"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from app.core.database import get_db
from app.models.agent import Agent
from app.schemas.agent import TrainingRequest

router = APIRouter()


class URLTrainingRequest(BaseModel):
    """Schema for training from URL"""
    url: HttpUrl
    metadata: dict = {}


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response"""
    filename: str
    size: int
    content_type: str
    storage_path: str


@router.post("/{agent_id}/train", status_code=status.HTTP_202_ACCEPTED)
def train_agent(
    agent_id: int,
    training_data: TrainingRequest,
    db: Session = Depends(get_db)
):
    """
    Train an agent with provided sources (URLs, documents, etc.)
    This is a placeholder that will integrate with Azure AI services
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update agent training status
    agent.training_status = "training"
    agent.knowledge_sources = training_data.sources
    
    if training_data.azure_model:
        agent.azure_model_version = training_data.azure_model
    
    if training_data.configuration:
        agent.configuration.update(training_data.configuration)
    
    db.commit()
    db.refresh(agent)
    
    # TODO: Integrate with Azure AI services for actual training
    # This would involve:
    # 1. Processing documents/URLs
    # 2. Extracting text and knowledge
    # 3. Fine-tuning the model
    # 4. Deploying to Azure
    
    return {
        "message": "Training initiated",
        "agent_id": agent_id,
        "status": "training",
        "sources_count": len(training_data.sources)
    }


@router.post("/{agent_id}/train/url")
def train_from_url(
    agent_id: int,
    url_data: URLTrainingRequest,
    db: Session = Depends(get_db)
):
    """Train agent from a URL"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Add URL to knowledge sources
    source = {
        "type": "url",
        "url": str(url_data.url),
        "metadata": url_data.metadata,
        "added_at": datetime.utcnow().isoformat()
    }
    
    if not agent.knowledge_sources:
        agent.knowledge_sources = []
    
    agent.knowledge_sources.append(source)
    agent.training_status = "pending"
    
    db.commit()
    db.refresh(agent)
    
    return {
        "message": "URL added to training queue",
        "agent_id": agent_id,
        "url": str(url_data.url),
        "sources_count": len(agent.knowledge_sources)
    }


@router.post("/{agent_id}/train/document", response_model=DocumentUploadResponse)
async def upload_training_document(
    agent_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document for training (placeholder for Azure Blob Storage integration)
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Read file content to get size
    content = await file.read()
    file_size = len(content)
    
    # TODO: Upload to Azure Blob Storage
    # For now, we'll just record the metadata
    
    storage_path = f"agents/{agent_id}/documents/{file.filename}"
    
    # Add document to knowledge sources
    source = {
        "type": "document",
        "filename": file.filename,
        "storage_path": storage_path,
        "content_type": file.content_type,
        "size": file_size,
        "added_at": datetime.utcnow().isoformat()
    }
    
    if not agent.knowledge_sources:
        agent.knowledge_sources = []
    
    agent.knowledge_sources.append(source)
    agent.training_status = "pending"
    
    db.commit()
    
    return {
        "filename": file.filename,
        "size": file_size,
        "content_type": file.content_type,
        "storage_path": storage_path
    }


@router.get("/{agent_id}/training-status")
def get_training_status(agent_id: int, db: Session = Depends(get_db)):
    """Get the training status of an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent_id,
        "training_status": agent.training_status,
        "knowledge_sources_count": len(agent.knowledge_sources) if agent.knowledge_sources else 0,
        "last_trained_at": agent.last_trained_at,
        "azure_deployment_id": agent.azure_deployment_id,
        "azure_model_version": agent.azure_model_version
    }


@router.delete("/{agent_id}/sources/{source_index}")
def remove_knowledge_source(
    agent_id: int,
    source_index: int,
    db: Session = Depends(get_db)
):
    """Remove a knowledge source from an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if not agent.knowledge_sources or source_index >= len(agent.knowledge_sources):
        raise HTTPException(status_code=404, detail="Knowledge source not found")
    
    removed_source = agent.knowledge_sources.pop(source_index)
    
    db.commit()
    db.refresh(agent)
    
    return {
        "message": "Knowledge source removed",
        "removed_source": removed_source,
        "remaining_sources": len(agent.knowledge_sources)
    }
