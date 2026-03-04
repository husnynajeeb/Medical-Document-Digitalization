from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime
from database import users_collection
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterModel(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(user: RegisterModel):
    existing = await users_collection.find_one({"email": user.email})

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    await users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    })

    return {"message": "User registered successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await users_collection.find_one({"email": form_data.username})
    
    if not db_user or not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Include 'name' in JWT
    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "name": db_user["name"]
    })
    
    return {"access_token": token, "token_type": "bearer"}