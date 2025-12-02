from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    profile: str
    is_active: bool
    chat_bot_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    user: UserBase
    access_token: str
    token_type: str
    
    model_config = {'from_attributes': True}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str
    
    def validate_passwords(self):
        """Validate that new_password and confirm_password match"""
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class PasswordResetResponse(BaseModel):
    message: str
    success: bool

class ValidateTokenRequest(BaseModel):
    token: str

class ValidateTokenResponse(BaseModel):
    valid: bool
    message: str