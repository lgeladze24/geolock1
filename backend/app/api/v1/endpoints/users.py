from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.db.base import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("/me")
async def read_user_me(
        db: Client = Depends(get_db)
) -> dict:
    try:
        # Get authenticated user from Supabase
        user = db.auth.get_user()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get additional user data from the database
        response = db.table('users').select('*').eq('id', user.id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")

        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/achievements")
async def read_user_achievements(
        user_id: UUID,
        db: Client = Depends(get_db)
) -> List[dict]:
    try:
        response = db.table('user_achievements') \
            .select('*, achievements(*))') \
            .eq('user_id', str(user_id)) \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))