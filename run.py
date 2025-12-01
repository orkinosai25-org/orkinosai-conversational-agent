"""Run the application"""
import uvicorn
from app.main import app
from app.core.database import init_db

if __name__ == "__main__":
    # Initialize database
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    # Run the application
    print("Starting Orkinosai CMS...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
