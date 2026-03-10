<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY_THRESHOLD=os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH="vector_store"
MEMORY_FILE="memory/memory.json"
OCR_CONFIDENCE_THRESHOLD=0.8
ASR_CONFIDENCE_THRESHOLD=0.8
VERIFIER_CONFIDENCE_THRESHOLD=0.75

=======
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY_THRESHOLD=os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH="vector_store"
MEMORY_FILE="memory/memory.json"
OCR_CONFIDENCE_THRESHOLD=0.8
ASR_CONFIDENCE_THRESHOLD=0.8
VERIFIER_CONFIDENCE_THRESHOLD=0.75

>>>>>>> f67757f31ab44a651e38f5373c7b21bc1ba10434
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")