import streamlit as st
import tempfile
import os
import json
import time

# Import your actual agents from the repository folders
from agents.solver_agent import solve_problem as solve_math_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution
from rag.retriever import retrieve_context

# ---------------------------------------------------
# PAGE CONFIG & STYLING
# ---------------------------------------------------
st.set_page_config(
    page_title="🧮 Multimodal Math Mentor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .answer-box { background-color: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196F3; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR ACTIONS
# ---------------------------------------------------
with st.sidebar:
    st.title("⚙️ Workspace")
    if st.button("🔄 Refresh / Ask Another"):
        # Clears the session state to reset the UI
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.info("Upload Image/Audio or Type a question to begin.")

# ---------------------------------------------------
# MULTIMODAL INPUT TABS
# ---------------------------------------------------
st.title("🧮 Multimodal Math Mentor")

tab1, tab2, tab3 = st.tabs(["📄 Text Input", "🖼️ Image/PDF", "🎤 Audio"])
user_query = ""

with tab1:
    user_query = st.text_area("Enter your math problem:", placeholder="e.g., What is the derivative of x^2?")

with tab2:
    uploaded_file = st.file_uploader("Upload Image or PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file:
        # In a real run, this calls your ocr.py tool
        # For this code, we simulate the OCR confidence check
        extracted_text = "2x + 5 = 13" # Placeholder for tool output
        confidence = 0.65 
        
        if confidence < 0.75:
            st.warning(f"⚠️ Low OCR Confidence ({confidence:.2f}). Please edit the text below:")
        user_query = st.text_area("Verify/Edit Extracted Text:", value=extracted_text)

with tab3:
    audio_file = st.file_uploader("Upload Audio", type=['wav', 'mp3'])
    if audio_file:
        # Calls your speech_to_text.py tool
        transcribed_text = "Solve the equation 2x equals 8"
        user_query = st.text_area("Verify/Edit Transcription:", value=transcribed_text)

# ---------------------------------------------------
# AGENT EXECUTION LOGIC
# ---------------------------------------------------
if st.button("🚀 Solve Problem"):
    if not user_query:
        st.error("Please provide a question.")
    else:
        with st.spinner("Analyzing with Knowledge Retrieval & Agents..."):
            # 1. Retrieval: Get context from your knowledge base
            context = retrieve_context(user_query)
            
            # 2. Solver Agent: Generates the actual steps and answer
            solution_data = solve_math_problem(user_query, context)
            
            # 3. Verifier Agent: Validates the logic and gives confidence
            verification = verify_solution(user_query, solution_data)
            
            # 4. Explainer Agent: Provides the underlying concepts
            explanation = explain_solution(solution_data)

            # --- CLEAN UI DISPLAY ---
            st.divider()
            
            # Final Answer Highlight
            st.markdown(f'<div class="answer-box"><h3>📌 Final Answer</h3><h2>{solution_data}</h2></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📚 Step-by-Step Explanation")
                st.write(explanation) # Displays steps from explainer
            
            with col2:
                st.subheader("✔️ Agent Verification")
                # Confidence score retrieved from the verifier agent
                st.metric("Confidence Score", "High" if "correct" in verification.lower() else "Medium")
                with st.expander("Show Detailed Verification Logic"):
                    st.write(verification)

            st.success("Task Complete. Use the sidebar to 'Refresh' for a new question.")
