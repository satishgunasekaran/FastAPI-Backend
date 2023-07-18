from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema
from api.auth import crud
from api.utils import cryptoUtil, jwtUtil, constantUtil
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    
    prefix="/api/v1",
)

@router.post("/auth/register", response_model=schema.UserList)
async def register(user: schema.UserCreate):
    # Check if user already exists
    result = await crud.get_user(user.email)
    
    if result:
        raise HTTPException(status_code=400, detail="User already exists") 
    
    # Create new user
    
    user.password = cryptoUtil.hash_password(user.password)
    
    await crud.create_user(user)
    return {**user.dict()}

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check user existed
    result = await crud.get_user(form_data.username)
    
    if not result:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    # Verify password
    user = schema.UserCreate(**result)
    verified_password = cryptoUtil.verify_password(form_data.password, user.password)
    
    if not verified_password:
        raise HTTPException(status_code=400, detail="Incorrect User or Password")
    
    # Create TOKEN
    access_token_expires = jwtUtil.timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = await jwtUtil.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_info" : schema.UserList(**result)   
    }

         
    