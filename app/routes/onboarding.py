"""Onboarding routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.core.database import get_db
from app.models.user import User
from app.models.account import Account
from app.models.agent import Agent

router = APIRouter()


class OnboardingStepRequest(BaseModel):
    """Schema for onboarding step completion"""
    step: int
    data: Optional[Dict[str, Any]] = None


class OnboardingComplete(BaseModel):
    """Schema for completing onboarding"""
    account_name: str
    account_slug: str
    agent_name: Optional[str] = None
    agent_description: Optional[str] = None


@router.get("/status/{user_id}")
def get_onboarding_status(user_id: int, db: Session = Depends(get_db)):
    """Get user's onboarding status"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "onboarding_completed": user.onboarding_completed,
        "current_step": user.onboarding_step,
        "total_steps": 3,  # Define total onboarding steps
        "steps": [
            {"step": 1, "name": "Create Account", "completed": user.onboarding_step >= 1},
            {"step": 2, "name": "Create First Agent", "completed": user.onboarding_step >= 2},
            {"step": 3, "name": "Complete Profile", "completed": user.onboarding_step >= 3}
        ]
    }


@router.post("/step/{user_id}")
def complete_onboarding_step(
    user_id: int, 
    step_data: OnboardingStepRequest, 
    db: Session = Depends(get_db)
):
    """Mark an onboarding step as complete"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.onboarding_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding already completed"
        )
    
    # Update onboarding step
    user.onboarding_step = step_data.step
    
    # Check if all steps are complete
    if step_data.step >= 3:
        user.onboarding_completed = True
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"Step {step_data.step} completed",
        "onboarding_completed": user.onboarding_completed,
        "current_step": user.onboarding_step
    }


@router.post("/complete/{user_id}")
def complete_onboarding(
    user_id: int,
    onboarding_data: OnboardingComplete,
    db: Session = Depends(get_db)
):
    """Complete the full onboarding process"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.onboarding_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding already completed"
        )
    
    # Create account for user
    account = Account(
        name=onboarding_data.account_name,
        slug=onboarding_data.account_slug,
        subscription_tier="free"
    )
    db.add(account)
    db.flush()
    
    # Associate user with account
    user.account_id = account.id
    
    # Create initial agent if provided
    if onboarding_data.agent_name:
        agent = Agent(
            name=onboarding_data.agent_name,
            description=onboarding_data.agent_description,
            owner_id=user.id,
            account_id=account.id
        )
        db.add(agent)
    
    # Mark onboarding as complete
    user.onboarding_completed = True
    user.onboarding_step = 3
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Onboarding completed successfully",
        "user_id": user.id,
        "account_id": account.id,
        "onboarding_completed": True
    }


@router.post("/skip/{user_id}")
def skip_onboarding(user_id: int, db: Session = Depends(get_db)):
    """Skip the onboarding process"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.onboarding_completed = True
    user.onboarding_step = 3
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Onboarding skipped",
        "user_id": user.id,
        "onboarding_completed": True
    }
