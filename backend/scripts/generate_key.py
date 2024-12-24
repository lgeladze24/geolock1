import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    print("Generated Secret Key:", generate_secret_key())