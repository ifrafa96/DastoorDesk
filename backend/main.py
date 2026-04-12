import uvicorn
import shutil
import os  # Added missing import
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Local Modular Imports
from logger_config import logger
from tools_library import LegalTools
from graph_engine import create_dastoor_graph

# 1. Initialize FastAPI with metadata
app = FastAPI(
    title="Dastoor Desk Enterprise API",
    description="Professional Agentic Legal System for Pakistan",
    version="1.0.0"
)

# 2. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Professional Department Dropdown
class LegalSector(str, Enum):
    PROPERTY = "property"
    CYBERCRIME = "cybercrime"
    TRAFFIC = "traffic"
    CONSUMER = "consumer"
    FAMILY = "family"
    LABOUR = "labour"
    CRIMINAL = "criminal"
    CONSTITUTIONAL = "constitutional"

class UserQuery(BaseModel):
    question: str
    department: LegalSector

# 4. Component Initialization
logger.info("[STARTUP] Dastoor Desk Intelligence initializing...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_db = Chroma(persist_directory="./dastoor_db", embedding_function=embeddings)

legal_tools = LegalTools(vector_db)
dastoor_brain = create_dastoor_graph(vector_db, legal_tools)

# --- ROUTES ---

@app.get("/", tags=["Home"])
async def home():
    return {
        "status": "Dastoor Desk is working!",
        "message": "The Agentic Legal System is Online.",
        "api_docs": "http://127.0.0.1:8000/docs"
    }

@app.post("/ask", tags=["Core Engine"])
async def ask_legal_bot(query: UserQuery):
    """Handles text-based queries."""
    try:
        # Language detection happens inside classifier_node (fast Unicode check).
        # No LLM pre-call needed here.
        inputs = {"query": query.question, "category": query.department.value}
        result = dastoor_brain.invoke(inputs)
        return {
            "answer": result["response"],
            "domain": result["category"],
            "evidence_list": result["evidence"],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"[SYSTEM ERROR] {str(e)}")
        return {"answer": "Error processing text request.", "status": "error"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)