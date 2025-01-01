from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.db.base import get_db
from typing import List
from uuid import UUID
from math import radians, cos, sin, asin, sqrt

router = APIRouter()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def calculate_score(distance: float) -> int:
    """
    Calculate score based on distance
    """
    if distance < 1:  # Less than 1km
        return 100
    elif distance < 5:  # Less than 5km
        return 75
    elif distance < 10:  # Less than 10km
        return 50
    elif distance < 50:  # Less than 50km
        return 25
    else:
        return max(0, int(100 - (distance / 10)))


@router.post("/{challenge_id}")
async def submit_guess(
        challenge_id: UUID,
        latitude: float,
        longitude: float,
        db: Client = Depends(get_db)
) -> dict:
    try:
        # Get challenge details
        challenge = db.table('challenges') \
            .select('*') \
            .eq('id', str(challenge_id)) \
            .execute()

        if not challenge.data:
            raise HTTPException(status_code=404, detail="Challenge not found")

        challenge = challenge.data[0]

        # Calculate distance and score
        distance = calculate_distance(
            latitude, longitude,
            challenge['latitude'], challenge['longitude']
        )

        score = calculate_score(distance)

        # Record the guess
        guess_data = {
            "user_id": db.auth.get_user().id,
            "challenge_id": str(challenge_id),
            "guessed_latitude": latitude,
            "guessed_longitude": longitude,
            "distance": distance,
            "score": score
        }

        response = db.table('guesses').insert(guess_data).execute()
        return {
            **response.data[0],
            "actual_location": {
                "latitude": challenge['latitude'],
                "longitude": challenge['longitude']
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/challenge/{challenge_id}")
async def get_challenge_guesses(
        challenge_id: UUID,
        db: Client = Depends(get_db)
) -> List[dict]:
    try:
        response = db.table('guesses') \
            .select('*, user:users(username)') \
            .eq('challenge_id', str(challenge_id)) \
            .order('score', desc=True) \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}")
async def get_user_guesses(
        user_id: UUID,
        db: Client = Depends(get_db)
) -> List[dict]:
    try:
        response = db.table('guesses') \
            .select('*, challenge:challenges(title)') \
            .eq('user_id', str(user_id)) \
            .order('created_at', desc=True) \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))