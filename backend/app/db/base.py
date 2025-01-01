from supabase import create_client, Client
from app.core.config import settings
from typing import Generator

def get_supabase() -> Client:
    """
    Get Supabase client with anonymous key (for public operations)
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_ANON_KEY
    )

def get_supabase_admin() -> Client:
    """
    Get Supabase client with service role key (for admin operations)
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_ROLE
    )

def get_db() -> Generator[Client, None, None]:
    """
    Dependency for FastAPI endpoints
    """
    db = get_supabase()
    try:
        yield db
    finally:
        # Supabase client doesn't need explicit cleanup
        pass