from supabase import create_client
import os
from dotenv import load_dotenv


def test_auth_and_challenges():
    # Load environment variables
    load_dotenv()

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Missing Supabase credentials in .env file")

    # Initialize Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    try:
        # Sign in
        auth_response = supabase.auth.sign_in_with_password({
            "email": os.getenv("TEST_USER_EMAIL"),
            "password": os.getenv("TEST_USER_PASSWORD")
        })

        print("Successfully logged in!")
        jwt_token = auth_response.session.access_token
        user_id = auth_response.user.id
        print(f"JWT Token: {jwt_token[:20]}...")
        print(f"User ID: {user_id}")

        # Test creating a challenge
        challenge_data = {
            "title": "Test Mountain Peak",
            "description": "Can you identify this famous mountain?",
            "latitude": 45.8326,
            "longitude": 6.8652,
            "difficulty": "medium",
            "creator_id": user_id  # Add the creator_id
        }

        # Create challenge using the authenticated client
        challenge_response = supabase.table('challenges').insert(challenge_data).execute()

        print("\nChallenge created successfully!")
        print("Challenge data:", challenge_response.data[0])

        # List challenges
        challenges = supabase.table('challenges').select('*').execute()
        print("\nAll challenges:")
        for challenge in challenges.data:
            print(f"- {challenge['title']} ({challenge['difficulty']})")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if hasattr(e, 'message'):
            print(f"Detailed error: {e.message}")


if __name__ == "__main__":
    test_auth_and_challenges()