import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

VECTOR_STORE_PATH = "faiss_index"
EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, EMBEDDINGS, allow_dangerous_deserialization=True)
    return None

def add_file_to_vector_store(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    vector_store = get_vector_store()
    if vector_store:
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, EMBEDDINGS)
    
    vector_store.save_local(VECTOR_STORE_PATH)

def add_texts_to_vector_store(texts: list, metadatas: list = None):
    vector_store = get_vector_store()
    if vector_store:
        vector_store.add_texts(texts, metadatas=metadatas)
    else:
        vector_store = FAISS.from_texts(texts, EMBEDDINGS, metadatas=metadatas)
    
    vector_store.save_local(VECTOR_STORE_PATH)

def delete_file_from_vector_store(file_path: str):
    # FAISS doesn't support easy deletion by ID without maintaining a mapping.
    # For now, we will just rebuild the index or ignore (since we are using local file path as ID effectively).
    # A better approach for production is to use a vector DB that supports deletion (Chroma, Pinecone, etc.)
    # OR, we can reload all files except the deleted one.
    
    # Simple approach: If we want to support deletion, we might need to re-index everything.
    # For this MVP, we'll assume re-indexing or just accepting it stays in index until rebuild.
    # BUT, let's try to remove the file from disk at least.
    pass
