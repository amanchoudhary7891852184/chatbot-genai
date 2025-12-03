# BOT GENAI
A powerful, privacy-focused Chat Agent built with FastAPI, MySQL, and Local AI models. This project allows users to register, upload documents (PDF/Text), and chat with them using a Retrieval-Augmented Generation (RAG) pipeline entirely on their local machine.
**GitHub Repository**: [https://github.com/amanchoudhary7891852184/chatbot-genai.git]

##  Features
-   **User Authentication**: Simplified Registration and Login using JWT and Argon2 hashing.
-   **Document Management**: Upload and Delete files (PDF, TXT).
-   **Local Vector Store**: Uses **FAISS** to index documents locally.   
-  **Local LLM**: Powered by **Google's Flan-T5 Large** running locally via HuggingFace Transformers. **No API keys required!**
- **Local Embeddings**: Uses **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) for privacy and speed.
-  **Chat Memory**: Remembers context from the current conversation and persists history in the vector store for long-term recall.
-  **Database**: **MySQL** for robust data persistence (Users, Files, Chat History).
-  **Modern Architecture**: Clean separation of concerns (Router -> Controller -> Service -> Model).

##  Tech Stack
-   **Backend**: FastAPI, Uvicorn
-   **Database**: MySQL, SQLAlchemy (Async), Alembic (Migrations)
-   **AI/ML**: LangChain, FAISS, Transformers, Torch, Accelerate, Sentence-Transformers
-   **Auth**: Python-Jose (JWT), Passlib (Argon2)

 ##  Installation & Setup
Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/amanchoudhary7891852184/chatbot-genai.git
cd Chatgenai
```
### 2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
**Using `uv` (Recommended for speed):**
```bash
uv venv
.venv\Scripts\activate
```

**Using standard Python:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate 
```
### 3. Install Dependencies
Install all required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a file named `.env` in the root directory of the project. Copy the following configuration into it:

```env
# Database Configuration
DB_HOST="localhost"
DB_PORT=3306
DB_USER="root"
DB_PASSWORD="your password"  # <--- CHANGE THIS to your actual MySQL root password
DB_NAME="db name"

# Security Configuration
SECRET_KEY="secret"  # Change this to a strong random string for production
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 5. Setup Database
This project includes a script to automatically create the database and apply migrations.

**Step 5a: Create the Database**
Run the `create_db.py` script. This connects to MySQL and creates the `Chat_Agent` database if it doesn't exist.
```bash
python create_db.py
```
*Output should be: `Database created successfully`*

**Step 5b: Run Migrations**
Use Alembic to create the necessary tables (users, files, chat_history) in the database.
```bash
alembic upgrade head
```
*You should see output indicating that tables are being created.*

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```
The API will be available  http://127.0.0.1:8000.
## 📖 Usage Guide

1.  **Open API Documentation**: Go to `http://127.0.0.1:8000/doc` in your browser.
2.  **Register**:
    -   Use the `/auth/register` endpoint.
    -   Click "Try it out", enter your details, and execute.
3.  **Login**:
    -   Use `/auth/login` to get an Access Token.
    -   Copy the `access_token` from the response.
    -   Click the **Authorize** button at the top right of the Swagger UI.
    -   Paste the token and click "Authorize".
4.  **Upload File**:
    -   Use `/upload/upload` to upload a PDF or Text file.
    -   This will index the file into the local FAISS vector store (`faiss_index/` folder will be created).
5.  **Chat**:
    -   Use `/chat/chat` to ask questions.
    -   The bot will use the uploaded documents and your chat history to answer.
6.  **Delete File**:
    -   Use `/upload/delete/{file_id}` to remove a file.

##  How It Works
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
