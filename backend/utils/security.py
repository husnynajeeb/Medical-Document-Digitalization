import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
print("SECRET_KEY:", SECRET_KEY)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

MAX_PASSWORD_BYTES = 72  # bcrypt limit


def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:MAX_PASSWORD_BYTES]
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    pw_bytes = password.encode("utf-8")[:MAX_PASSWORD_BYTES]
    return bcrypt.checkpw(pw_bytes, hashed.encode("utf-8"))


def create_access_token(data: dict):
    """
    Generates a JWT access token.
    Includes 'user_id' and optionally 'name' from the data dict.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Include 'name' if present
    if "name" in data:
        to_encode["name"] = data["name"]

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token