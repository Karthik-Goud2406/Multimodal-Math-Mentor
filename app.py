
import streamlit as st
import tempfile
from audiorecorder import audiorecorder

# tools
from tools.ocr import extract_text_from_image
from tools.speech_to_text import audio_to_text

# agents
from agents.parser_agent import parse_question
from agents.router_agent import route_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# rag + memory
from rag.retriever import retrieve_context
from memory.memory_manager import save_memory

# local LLM warmup
from utils.llm import call_llm# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="Multimodal Math Mentor", layout="wide")

st.title("Multimodal Math Mentor")

st.write(
"""
Upload an image, speak, or type a math question.
The AI will solve it step-by-step using a multi-agent pipeline.
"""
)

# ---------------------------------------------------
# MODEL WARMUP
# ---------------------------------------------------

if "model_loaded" not in st.session_state:

    try:
        call_llm("warmup")
    except:
        pass

    st.session_state.model_loaded = True


# ---------------------------------------------------
# INPUT MODE
# ---------------------------------------------------

mode = st.radio(
    "Choose Input Mode",
    [
        "Text Question",
        "Image Upload",
        "Audio Upload"
    ]
)

question = ""


# ---------------------------------------------------
# TEXT INPUT
# ---------------------------------------------------

if mode == "Text Question":

    question = st.text_input(
        "Enter your math question",
        key="text_input"
    )


# ---------------------------------------------------
# IMAGE INPUT
# ---------------------------------------------------

if mode == "Image Upload":

    file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if file:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:

            tmp.write(file.read())
            path = tmp.name

        text, conf = extract_text_from_image(path)

        if len(text) > 200:
            st.warning("OCR extracted large text. Keep only one problem.")

        question = st.text_area(
            "Edit OCR text",
            text
        )


# ---------------------------------------------------
# AUDIO INPUT
# ---------------------------------------------------

if mode == "Audio Upload":

    st.subheader("Record or Upload Audio")

    audio = audiorecorder("Start recording", "Stop recording")

    if len(audio) > 0:

        st.audio(audio.export().read())

        with open("temp_audio.wav", "wb") as f:
            f.write(audio.export().read())

        transcript = audio_to_text("temp_audio.wav")

        question = st.text_area(
            "Edit transcript",
            transcript
        )

    uploaded_audio = st.file_uploader(
        "Or upload audio",
        type=["wav", "mp3"]
    )

    if uploaded_audio:

        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_audio.read())

        transcript = audio_to_text("temp_audio.wav")

        question = st.text_area(
            "Edit transcript",
            transcript
        )


# ---------------------------------------------------
# SOLVE BUTTON
# ---------------------------------------------------

if st.button("Solve"):

    if question.strip() == "":
        st.warning("Please enter a question")
        st.stop()

    agent_trace = []

    # ----------------------------
    # PARSER AGENT
    # ----------------------------

    parsed = parse_question(question)

    agent_trace.append({
        "agent": "Parser Agent",
        "output": parsed
    })

    # ----------------------------
    # ROUTER AGENT
    # ----------------------------

    topic = route_problem(parsed["problem_text"])

    agent_trace.append({
        "agent": "Router Agent",
        "output": topic
    })

    # ----------------------------
    # RETRIEVER
    # ----------------------------

    with st.spinner("Retrieving knowledge..."):
        docs = retrieve_context(parsed["problem_text"])

    context = "\n".join([str(d) for d in docs])

    agent_trace.append({
        "agent": "Retriever",
        "output": docs
    })

    # ----------------------------
    # SOLVER
    # ----------------------------

    with st.spinner("Solving problem..."):
        answer = solve_problem(parsed["problem_text"], docs)

    agent_trace.append({
        "agent": "Solver",
        "output": answer
    })

    # ----------------------------
    # VERIFIER
    # ----------------------------

    verification = verify_solution(parsed["problem_text"], answer)

    agent_trace.append({
        "agent": "Verifier",
        "output": verification
    })

    # ----------------------------
    # CONFIDENCE
    # ----------------------------

    st.subheader("Confidence")

    if "correct" in verification.lower():
        st.success("High confidence")

    elif "incorrect" in verification.lower():
        st.error("Low confidence")

    else:
        st.warning("Needs human review")

    # ----------------------------
    # HUMAN IN THE LOOP
    # ----------------------------

    if "unsure" in verification.lower():

        st.warning("AI is unsure. Please review.")

        correction = st.text_area("Provide corrected answer")

        if st.button("Submit correction"):

            save_memory({
                "question": question,
                "ai_answer": answer,
                "human_correction": correction
            })

            st.success("Correction saved")

    # ----------------------------
    # EXPLAINER
    # ----------------------------

    explanation = explain_solution(
        parsed["problem_text"],
        answer,
        context
    )

    agent_trace.append({
        "agent": "Explainer Agent",
        "output": explanation
    })

    # ------------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------------

    st.subheader("Final Answer")
    st.write(answer)

    st.subheader("Explanation")
    st.write(explanation)

    st.subheader("Verification")
    st.write(verification)

    # ------------------------------------------------
    # RETRIEVED KNOWLEDGE
    # ------------------------------------------------

    st.subheader("Retrieved Knowledge")

    for d in docs:
        st.write(d)

    # ------------------------------------------------
    # AGENT TRACE
    # ------------------------------------------------

    st.subheader("Agent Trace")

    for step in agent_trace:

        with st.expander(step["agent"]):
            st.write(step["output"])

    # ------------------------------------------------
    # MEMORY
    # ------------------------------------------------

    save_memory({
    "question": str(question),
    "parsed": str(parsed),
    "topic": str(topic),
    "solution": str(answer),
    "verification": str(verification)
   })