from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema
from api.auth import crud
from api.utils import cryptoUtil, jwtUtil, constantUtil
from fastapi.security import OAuth2PasswordRequestForm
import uuid

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

         
@router.post("/auth/forgot-password")
async def forgot_password(request: schema.ForgotPassword):
    # Check user existed
    result = await crud.get_user(request.email)
    if not result:
        raise HTTPException(status_code=404,
                            detail="User not found.")
    
    # Create reset code and save in the database
    reset_code = str(uuid.uuid1())
    await crud.create_reset_code(request.email, reset_code)
    
    # Sending Mail
    subject = "Hello Coder"
    recipient = [request.email]
    
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {0:}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """.format(request.email, reset_code)
    
    
    
    
    
    
    return reset_code










