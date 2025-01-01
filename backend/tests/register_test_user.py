from supabase import create_client, Client
import os
from dotenv import load_dotenv
import re


class UserRegistration:
    def __init__(self):
        load_dotenv()

        # Get environment variables
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.test_email = os.getenv("TEST_USER_EMAIL")
        self.test_password = os.getenv("TEST_USER_PASSWORD")

        # Validate environment variables
        self.validate_env_vars()

        # Initialize Supabase client
        self.supabase: Client = create_client(self.supabase_url, self.supabase_anon_key)

    def validate_env_vars(self):
        """Validate all required environment variables"""
        missing_vars = []

        if not self.supabase_url:
            missing_vars.append("SUPABASE_URL")
        if not self.supabase_anon_key:
            missing_vars.append("SUPABASE_ANON_KEY")
        if not self.test_email:
            missing_vars.append("TEST_USER_EMAIL")
        if not self.test_password:
            missing_vars.append("TEST_USER_PASSWORD")

        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

        # Validate email format
        if not self.is_valid_email(self.test_email):
            raise ValueError(f"Invalid email format: {self.test_email}")

        # Validate password length
        if len(self.test_password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))

    def register_user(self):
        """Register a new test user"""
        try:
            print(f"Attempting to register user: {self.test_email}")

            auth_response = self.supabase.auth.sign_up({
                "email": self.test_email,
                "password": self.test_password,
                "options": {
                    "data": {
                        "username": self.test_email.split('@')[0]
                    }
                }
            })

            print("Registration successful!")
            print(f"User ID: {auth_response.user.id}")
            return auth_response.user

        except Exception as e:
            error_message = str(e)
            if "User already registered" in error_message:
                print("User already exists. Try logging in instead.")
            elif "invalid email" in error_message.lower():
                print(f"Invalid email format: {self.test_email}")
                print("Please use a valid email address in your .env file")
            elif "password" in error_message.lower():
                print("Password error:", error_message)
                print("Make sure your password meets the minimum requirements")
            else:
                print(f"Registration failed: {error_message}")
            return None


def main():
    try:
        print("\n=== Starting User Registration ===\n")

        registration = UserRegistration()
        user = registration.register_user()

        if user:
            print("\n=== Registration Completed Successfully ===")
        else:
            print("\n=== Registration Failed ===")

    except ValueError as e:
        print(f"\nConfiguration Error: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")


if __name__ == "__main__":
    main()