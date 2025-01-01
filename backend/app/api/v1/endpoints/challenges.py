from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.db.base import get_db
from app.core.auth import get_current_user
from typing import List, Optional
from uuid import UUID

router = APIRouter()

@router.post("/")
async def create_challenge(
    title: str,
    description: str,
    latitude: float,
    longitude: float,
    difficulty: str,
    current_user = Depends(get_current_user),
    db: Client = Depends(get_db)
) -> dict:
    try:
        challenge_data = {
            "title": title,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
            "difficulty": difficulty,
            "creator_id": current_user.id
        }

        response = db.table('challenges').insert(challenge_data).execute()
        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_challenges(
    difficulty: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Client = Depends(get_db)  # No auth required for listing
) -> List[dict]:
    try:
        query = db.table('challenges')\
            .select('*, creator:users(username)')\
            .order('created_at', desc=True)\
            .limit(limit)\
            .offset(offset)

        if difficulty:
            query = query.eq('difficulty', difficulty)

        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))