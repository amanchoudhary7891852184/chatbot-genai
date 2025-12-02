import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models import Users
import schemas.user_schemas as user_schemas
from utils.security import verify_password
from utils.jwt import create_access_token
from utils.security import hash_password
from sqlalchemy import select

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def authenticate_user(email: str, password: str, db: AsyncSession):
    try:
        result = await db.execute(select(Users).where(Users.email == email))
        user = result.scalars().first()
        if not user or not verify_password(password, user.password):
            return None
        return user
    except SQLAlchemyError as e:
        print("Error during authentication:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def login(email: str, password: str, db: AsyncSession):
    try:
        user = await authenticate_user(email, password, db)
        print("Authenticated User:", user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        return {
            "user": user_schemas.User.model_validate(user),  # Pydantic v2
            "access_token": access_token,
            "token_type": "bearer",
        }
    except SQLAlchemyError as e:
        print("Error during login:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def register(user: user_schemas.UserCreate, db: AsyncSession):
    try:

        result = await db.execute(select(Users).where(Users.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user_data = user.model_dump()
        user_data["password"] = hash_password(user_data["password"])

        db_user = Users(**user_data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
        
        # Generate reset token
        reset_token = generate_reset_token()
        
        # Store token and expiry in database (1 hour expiry)
        user.reset_token = reset_token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        
        await db.commit()
        
        # Send email only to registered users
        send_reset_password_email(email, reset_token)
        
        return {
            "message": "Password reset link has been sent to your email.",
            "success": True
        }
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        print("Error during password reset request:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


async def reset_password(token: str, new_password: str, confirm_password: str, db: AsyncSession):
    """Reset password using the reset token"""
    try:
        # Validate that passwords match
        if new_password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Find user by reset token
        result = await db.execute(
            select(Users).where(Users.reset_token == token)
        )
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if token is expired
        if not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Update password and clear reset token
        user.password = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        
        await db.commit()
        
        return {
            "message": "Password has been reset successfully",
            "success": True
        }
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        print("Error during password reset:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resetting your password"
        )


async def validate_reset_token(token: str, db: AsyncSession):
    """Validate if reset token is valid and not expired"""
    try:
        # Find user by reset token
        result = await db.execute(
            select(Users).where(Users.reset_token == token)
        )
        user = result.scalars().first()
        
        # Token not found
        if not user:
            return {
                "valid": False,
                "message": "Invalid reset token"
            }
        
        # Check if token is expired
        if not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
            return {
                "valid": False,
                "message": "Reset token has expired"
            }
        
        # Token is valid
        return {
            "valid": True,
            "message": "Token is valid"
        }
        
    except SQLAlchemyError as e:
        print("Error during token validation:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while validating the token"
        )
