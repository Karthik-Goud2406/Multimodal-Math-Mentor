import streamlit as st
import tempfile
import PyPDF2
import openai

# tools

from tools.ocr import extract_text_from_image

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

# OPENAI CONFIG

# -----------------------------

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def whisper_transcribe(file_path):
with open(file_path, "rb") as audio_file:
transcript = client.audio.transcriptions.create(
model="gpt-4o-mini-transcribe",
file=audio_file
)
return transcript.text

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(page_title="Multimodal Math Mentor", layout="wide")

st.title("Multimodal Math Mentor")
st.write("Solve math using text, image, PDF, or audio (Whisper).")

# -----------------------------

# SESSION STATE

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
"Choose Input",
["Text", "Image", "PDF", "Audio (Whisper)"]
)

question = ""

# -----------------------------

# TEXT

# -----------------------------

if mode == "Text":
question = st.text_input("Enter question")

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
    question = st.text_area("Edit text", text)
```

# -----------------------------

# PDF

# -----------------------------

elif mode == "PDF":

```
file = st.file_uploader("Upload PDF", type=["pdf"])

if file:
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    question = st.text_area("Extracted text", text)
```

# -----------------------------

# AUDIO (WHISPER)

# -----------------------------

elif mode == "Audio (Whisper)":

```
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        path = tmp.name

    with st.spinner("Transcribing with Whisper..."):
        question = whisper_transcribe(path)

    question = st.text_area("Transcribed text", question)
```

# -----------------------------

# SOLVE

# -----------------------------

if st.button("Solve"):

```
if not question.strip():
    st.warning("Enter a question")
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

st.session_state.answer = answer
st.session_state.explanation = explanation
st.session_state.verification = verification

save_memory({
    "question": question,
    "solution": answer
})
```

# -----------------------------

# DISPLAY

# -----------------------------

if st.session_state.answer is not None:

```
st.subheader("Answer")
st.write(st.session_state.answer)

st.subheader("Explanation")
st.write(st.session_state.explanation)

st.subheader("Verification")
st.write(st.session_state.verification)
```
