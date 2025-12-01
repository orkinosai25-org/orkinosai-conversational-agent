"""Agent routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(agent_data: AgentCreate, owner_id: int, db: Session = Depends(get_db)):
    """Create a new agent"""
    agent_dict = agent_data.dict()
    
    # Ensure configuration and knowledge_sources are initialized
    if 'configuration' not in agent_dict or agent_dict['configuration'] is None:
        agent_dict['configuration'] = {}
    
    db_agent = Agent(
        **agent_dict,
        owner_id=owner_id,
        knowledge_sources=[]
    )
    
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return db_agent


@router.get("/", response_model=List[AgentResponse])
def list_agents(
    skip: int = 0, 
    limit: int = 100, 
    owner_id: int = None,
    account_id: int = None,
    db: Session = Depends(get_db)
):
    """List agents with optional filters"""
    query = db.query(Agent)
    
    if owner_id:
        query = query.filter(Agent.owner_id == owner_id)
    
    if account_id:
        query = query.filter(Agent.account_id == account_id)
    
    agents = query.offset(skip).limit(limit).all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get a specific agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, agent_data: AgentUpdate, db: Session = Depends(get_db)):
    """Update an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(agent)
    db.commit()
    return None


@router.post("/{agent_id}/activate", response_model=AgentResponse)
def activate_agent(agent_id: int, db: Session = Depends(get_db)):
    """Activate an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.is_active = True
    db.commit()
    db.refresh(agent)
    return agent


@router.post("/{agent_id}/deactivate", response_model=AgentResponse)
def deactivate_agent(agent_id: int, db: Session = Depends(get_db)):
    """Deactivate an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.is_active = False
    db.commit()
    db.refresh(agent)
    return agent
