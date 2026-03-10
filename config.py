
import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH="vector_store"
MEMORY_FILE="memory/memory.json"
OCR_CONFIDENCE_THRESHOLD=0.8
ASR_CONFIDENCE_THRESHOLD=0.8
VERIFIER_CONFIDENCE_THRESHOLD=0.75
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


