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

# llm

from utils.llm import call_llm

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(page_title="Multimodal Math Mentor", layout="wide")

st.title("Multimodal Math Mentor")
st.write("Solve math using text, image, or audio.")

# -----------------------------

# SESSION STATE (FIX)

# -----------------------------

if "answer" not in st.session_state:
st.session_state.answer = None

if "explanation" not in st.session_state:
st.session_state.explanation = None

if "verification" not in st.session_state:
st.session_state.verification = None

# -----------------------------

# MODEL WARMUP

# -----------------------------

if "model_loaded" not in st.session_state:
try:
call_llm("warmup")
except:
pass
st.session_state.model_loaded = True

# -----------------------------

# INPUT MODE

# -----------------------------

mode = st.radio(
"Choose Input Mode",
["Text", "Image", "Audio"]
)

question = ""

# -----------------------------

# TEXT

# -----------------------------

if mode == "Text":
question = st.text_input("Enter your math question")

# -----------------------------

# IMAGE

# -----------------------------

elif mode == "Image":

```
file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    text, _ = extract_text_from_image(path)
    question = st.text_area("Edit OCR text", text)
```

# -----------------------------

# AUDIO

# -----------------------------

elif mode == "Audio":

```
audio = audiorecorder("Start recording", "Stop recording")

if len(audio) > 0:
    st.audio(audio.export().read())

    with open("temp_audio.wav", "wb") as f:
        f.write(audio.export().read())

    question = audio_to_text("temp_audio.wav")
    question = st.text_area("Transcribed text", question)
```

# -----------------------------

# SOLVE BUTTON

# -----------------------------

if st.button("Solve"):

```
if question.strip() == "":
    st.warning("Please enter a question")
    st.stop()

parsed = parse_question(question)

if parsed.get("needs_clarification"):
    st.error("Problem unclear")
    st.stop()

docs = retrieve_context(parsed["problem_text"])
context = "\n".join([str(d) for d in docs])

answer = solve_problem(parsed["problem_text"], context)
verification = verify_solution(parsed["problem_text"], answer)
explanation = explain_solution(parsed["problem_text"], answer, context)

# 🔥 STORE RESULTS (KEY FIX)
st.session_state.answer = answer
st.session_state.explanation = explanation
st.session_state.verification = verification

save_memory({
    "question": question,
    "solution": answer
})
```

# -----------------------------

# DISPLAY (OUTSIDE BUTTON)

# -----------------------------

if st.session_state.answer is not None:

```
st.subheader("Final Answer")
st.write(st.session_state.answer)

st.subheader("Explanation")
st.write(st.session_state.explanation)

st.subheader("Verification")
st.write(st.session_state.verification)
```
