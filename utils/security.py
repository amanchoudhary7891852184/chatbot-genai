import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import logging

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash a password (sync)"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password (sync)"""
    return pwd_context.verify(plain_password, hashed_password)
