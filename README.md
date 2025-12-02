# Dotsy Chat Agent

A powerful, privacy-focused Chat Agent built with FastAPI, MySQL, and Local AI models. This project allows users to register, upload documents (PDF/Text), and chat with them using a Retrieval-Augmented Generation (RAG) pipeline entirely on their local machine.

## 🚀 Features

-   **User Authentication**: Simplified Registration and Login using JWT and Argon2 hashing.
-   **Document Management**: Upload and Delete files (PDF, TXT).
-   **Local Vector Store**: Uses **FAISS** to index documents locally.
-   **Local Embeddings**: Uses **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) for privacy and speed.
-   **Local LLM**: Powered by **Google's Flan-T5 Large** running locally via HuggingFace Transformers. **No API keys required!**
-   **Chat Memory**: Remembers context from the current conversation and persists history in the vector store for long-term recall.
-   **Database**: **MySQL** for robust data persistence (Users, Files, Chat History).
-   **Modern Architecture**: Clean separation of concerns (Router -> Controller -> Service -> Model).

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Uvicorn
-   **Database**: MySQL, SQLAlchemy (Async), Alembic (Migrations)
-   **AI/ML**: LangChain, FAISS, Transformers, Torch, Accelerate, Sentence-Transformers
-   **Auth**: Python-Jose (JWT), Passlib (Argon2)

## 📋 Prerequisites

-   **Python 3.10+**
-   **MySQL Server** running on `localhost:3306`
-   **Git**

## ⚙️ Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd chat-agent
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Using uv (Recommended)
    uv venv
    .venv\Scripts\activate

    # OR Standard Python
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    DB_HOST="localhost"
    DB_PORT=3306
    DB_USER="root"
    DB_PASSWORD="9256"
    DB_NAME="Chat_Agent"

    SECRET_KEY="secret"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Setup Database**
    Create the database and run migrations:
    ```bash
    # Create DB (if not exists)
    python create_db.py
    
    # Run Migrations
    alembic upgrade head
    ```

## 🏃‍♂️ Running the Application

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📖 Usage Guide

1.  **Open API Documentation**: Go to `http://127.0.0.1:8000/docs`.
2.  **Register**: Use the `/auth/register` endpoint to create an account.
3.  **Login**: Use `/auth/login` to get an Access Token.
    -   Click "Authorize" at the top right of Swagger UI and enter the token.
4.  **Upload File**: Use `/upload/upload` to upload a PDF or Text file.
    -   This will index the file into the local FAISS vector store.
5.  **Chat**: Use `/chat/chat` to ask questions.
    -   **Context Aware**: The bot remembers previous messages in the session.
    -   **Document Aware**: It uses uploaded files to answer questions.
6.  **Delete File**: Use `/upload/delete/{file_id}` to remove a file from the database and disk.

## 🧠 How It Works

### 1. Data Storage & Embeddings
-   **Files**: Uploaded files are saved to the local `uploads/` directory.
-   **Embeddings**: Text is extracted, chunked, and embedded using `all-MiniLM-L6-v2`.
-   **Vector Store**: Embeddings are stored in a local FAISS index (`faiss_index/`).

### 2. RAG Pipeline (Retrieval-Augmented Generation)
-   **Query**: When you ask a question, it's embedded and compared against the FAISS index.
-   **Retrieval**: The top 3 most relevant text chunks are retrieved.
-   **Generation**: The retrieved context + chat history + user question are sent to the local **Flan-T5** model.
-   **Response**: The model generates a natural language response.

### 3. Memory & Persistence
-   **Short-term**: Recent chat history is fetched from the MySQL `chat_history` table.
-   **Long-term**: Every interaction is also saved back to the FAISS vector store, allowing the bot to "remember" facts over time.
