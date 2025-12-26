from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
from app.services.auth import (
  create_access_token,
  get_current_user,
  get_password_hash,
  verify_password,
  ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.db.crud import create_user, get_user_by_username

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
  username: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class UserResponse(BaseModel):
  username: str
  id: int

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
  db_user = await get_user_by_username(user.username)
  if db_user:
    raise HTTPException(status_code=400, detail="Username already registered")
    
  hashed_password = get_password_hash(user.password)
  user_dict = {"username": user.username, "hashed_password": hashed_password}
  user_id = await create_user(user_dict)
  return {"username": user.username, "id": user_id}

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  user = await get_user_by_username(form_data.username)
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    return {"username": current_user.username, "id": current_user.id}
