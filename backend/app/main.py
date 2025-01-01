from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import users, challenges, guesses

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the location-based guessing game",
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["challenges"])
app.include_router(guesses.router, prefix=f"{settings.API_V1_STR}/guesses", tags=["guesses"])

@app.get("/")
async def root():
    return {"message": "Welcome to GeoLock API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}