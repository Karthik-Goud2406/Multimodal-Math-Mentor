import streamlit as st
import tempfile
import os
import json
import time
from PIL import Image

# Mock imports for demonstration - in production, these would connect to your agent files
# from agents.solver_agent import solve_math_problem
# from agents.verifier_agent import verify_solution
# from agents.explainer_agent import explain_solution

# ---------------------------------------------------
# PAGE CONFIG & STYLING
# ---------------------------------------------------
st.set_page_config(
    page_title="🧮 Multimodal Math Mentor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .stExpander { border: 1px solid #e6e6e6; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HELPER FUNCTIONS (Logic from app.py)
# ---------------------------------------------------

def get_ocr_data(file):
    """Simulates OCR extraction with a confidence score"""
    # In a real scenario, this uses PaddleOCR
    return "2x + 5 = 13", 0.65  # Example: Low confidence to trigger edit warning

def get_audio_data(audio_file):
    """Simulates Whisper transcription"""
    return "What is the square root of 144?", 0.90

def solve_with_agents(question):
    """Simulates the agent workflow"""
    # 1. Solver Agent computes step-by-step
    # 2. Verifier Agent checks logic
    # 3. Explainer Agent retrieves knowledge
    
    solution = {
        "answer": "x = 4",
        "steps": ["Subtract 5 from both sides: 2x = 8", "Divide by 2: x = 4"],
        "confidence": "92%",
        "topic": "Basic Algebra",
        "explanation": "This problem involves isolating the variable using inverse operations."
    }
    return solution

# ---------------------------------------------------
# SIDEBAR & STATE
# ---------------------------------------------------
with st.sidebar:
    st.title("⚙️ Workspace")
    if st.button("🔄 Refresh / New Question"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    
    st.divider()
    st.info("The mentor uses OCR, Speech-to-Text, and RAG-based agents to solve problems.")

# ---------------------------------------------------
# MAIN UI - INPUT SECTION
# ---------------------------------------------------
st.title("🧮 Multimodal Math Mentor")
st.write("Upload an image, PDF, audio, or type your problem below.")

tab1, tab2, tab3 = st.tabs(["📄 Text Input", "🖼️ Image/PDF", "🎤 Audio"])

input_text = ""

with tab1:
    input_text = st.text_area("Enter your math problem:", height=100, placeholder="e.g., Solve for x: 3x - 7 = 11")

with tab2:
    uploaded_file = st.file_uploader("Upload Image or PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file:
        # Process OCR
        extracted, confidence = get_ocr_data(uploaded_file)
        
        if confidence < 0.75:
            st.warning(f"⚠️ Low OCR Confidence ({confidence*100:.0%}). Please verify the text below:")
        else:
            st.success(f"✅ Text extracted with {confidence*100:.0%} confidence.")
        
        input_text = st.text_area("Edit extracted text if needed:", value=extracted)

with tab3:
    audio_file = st.file_uploader("Upload Audio Record", type=['wav', 'mp3'])
    if audio_file:
        transcribed, aud_conf = get_audio_data(audio_file)
        st.success(f"🎤 Transcription complete ({aud_conf*100:.0%} confidence).")
        input_text = st.text_area("Edit transcript if needed:", value=transcribed)

# ---------------------------------------------------
# EXECUTION & RESULTS
# ---------------------------------------------------
if st.button("🚀 Solve Problem"):
    if not input_text:
        st.error("Please provide a question first.")
    else:
        with st.spinner("Agents are analyzing the problem..."):
            time.sleep(1) # Simulate processing
            result = solve_with_agents(input_text)
            
            st.divider()
            
            # Layout for Results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📌 Final Answer")
                st.success(f"### {result['answer']}")
                
                st.subheader("📚 Step-by-Step Explanation")
                for i, step in enumerate(result['steps'], 1):
                    st.write(f"{i}. {step}")
            
            with col2:
                st.subheader("✔️ Agent Verification")
                st.metric("Confidence Score", result['confidence'])
                st.write(f"**Topic Identified:** {result['topic']}")
                
                with st.expander("Show Detailed Logic"):
                    st.write(result['explanation'])
            
            st.divider()
            
            # Download Option
            report = f"Problem: {input_text}\nAnswer: {result['answer']}\nTopic: {result['topic']}"
            st.download_button("📥 Download Solution PDF/Text", data=report, file_name="solution.txt")
