from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from supabase import Client
from app.db.base import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the location-based guessing game",
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to GeoLock API"}

@app.get("/health")
async def health_check(db: Client = Depends(get_db)):
    try:
        # Test database connection
        response = db.table('users').select('count', count='exact').execute()
        return {
            "status": "healthy",
            "database": "connected",
            "user_count": response.count if hasattr(response, 'count') else 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }