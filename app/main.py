"""Main application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import users, accounts, agents, onboarding, training

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Orkinosai CMS for agent management and SaaS operations"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(onboarding.router, prefix="/api/v1/onboarding", tags=["onboarding"])
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Orkinosai CMS API",
        "version": settings.APP_VERSION,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
