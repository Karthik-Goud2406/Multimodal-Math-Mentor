import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# Load embeddings only once (important)
# --------------------------------------------------

@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# --------------------------------------------------
# Load vector database only once
# --------------------------------------------------

@st.cache_resource
def load_vector_db():

    embeddings = load_embeddings()

    db = FAISS.load_local(
        "rag/vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


# --------------------------------------------------
# Retrieve relevant context
# --------------------------------------------------

def retrieve_context(query, k=1):

    db = load_vector_db()

    docs = db.similarity_search(query, k=k)

    results = []

    for d in docs:
        results.append(d.page_content)

    return results