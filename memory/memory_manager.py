import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import streamlit as st

MEMORY_FILE = "memory/memory.json"

@st.cache_resource
def _get_embedding_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def _cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def save_memory(record):
    data = _load_memory()
    data.append(record)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def retrieve_past_solutions(query, threshold=0.8):
    """
    Search past solved memory items to find similar problems.
    Returns previous solutions/human corrections if a match is found.
    """
    memory_data = _load_memory()
    if not memory_data:
        return None

    model = _get_embedding_model()
    query_emb = model.encode(query)

    best_match = None
    highest_score = 0.0

    for item in memory_data:
        past_q = item.get("question", "")
        if past_q:
            past_emb = model.encode(past_q)
            score = _cosine_similarity(query_emb, past_emb)
            
            if score > highest_score and score > threshold:
                highest_score = score
                best_match = item

    if best_match is not None:
        past_solution = best_match.get("ai_answer", best_match.get("solution", ""))
        human_correction = best_match.get("human_correction", "")
        
        # If human corrected it, prioritize the correction!
        if human_correction:
            return f"PAST HUMAN CORRECTION to similar problem: {human_correction}"
        else:
            return f"PAST AI SOLUTION to similar problem: {past_solution}"
            
    return None