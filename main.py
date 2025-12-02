from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    users,
    auth,
    upload,
    chat,
)

# Define tags metadata (headings)
tags_metadata = [
    {"name": "Users", "description": "Operations related to user management"},
    {"name": "Auth", "description": "Authentication and authorization operations"},
    {"name": "Upload", "description": "File upload operations"},
    {"name": "Chat", "description": "Chatbot operations"},
]
   
app = FastAPI( 
    title="Chat Agent",  
    description="API for Chat Agent with File Upload and FAISS Vector Store",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
