from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.base import get_db
from supabase import Client

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Client = Depends(get_db)
):
    try:
        # Verify the JWT token with Supabase
        user = db.auth.get_user(credentials.credentials)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Optional: Add admin-only middleware
async def get_admin_user(
        current_user=Depends(get_current_user),
        db: Client = Depends(get_db)
):
    try:
        # Check if user has admin role (you'll need to add this field to your users table)
        response = db.table('users') \
            .select('is_admin') \
            .eq('id', current_user.id) \
            .execute()

        if not response.data or not response.data[0].get('is_admin'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )