import streamlit as st
import tempfile
import streamlit.components.v1 as components

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

# local LLM warmup

from utils.llm import call_llm

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(page_title="Multimodal Math Mentor", layout="wide")

st.title("Multimodal Math Mentor")

st.write("""
Upload an image, speak, or type a math question.
The AI will solve it step-by-step using a multi-agent pipeline.
""")

# -----------------------------

# SESSION STATE

# -----------------------------

if "answer" not in st.session_state:
st.session_state.answer = None

if "explanation" not in st.session_state:
st.session_state.explanation = None

if "verification" not in st.session_state:
st.session_state.verification = None

if "agent_trace" not in st.session_state:
st.session_state.agent_trace = []

if "docs" not in st.session_state:
st.session_state.docs = []

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
["Text / Voice", "Image Upload"]
)

question = ""

# -----------------------------

# TEXT + VOICE (WORKING)

# -----------------------------

if mode == "Text / Voice":

```
st.markdown("### 🎤 Speak or Type your question")

components.html("""
<script>
function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {

        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-IN";

        recognition.start();

        recognition.onresult = function(e) {
            const text = e.results[0][0].transcript;

            const inputs = window.parent.document.querySelectorAll('textarea, input');
            inputs.forEach(input => {
                if (input.placeholder && input.placeholder.includes("Enter your math question")) {
                    input.value = text;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
        };

        recognition.onerror = function(e) {
            recognition.stop();
        };
    } else {
        alert("Speech not supported in this browser");
    }
}
</script>

<button onclick="startDictation()" style="
    background:#4CAF50;
    color:white;
    padding:10px 20px;
    border:none;
    border-radius:8px;
    cursor:pointer;
    font-size:16px;">
    🎤 Speak
</button>
""", height=80)

question = st.text_input(
    "Enter your math question",
    key="text_input",
    placeholder="Enter your math question"
)
```

# -----------------------------

# IMAGE INPUT

# -----------------------------

elif mode == "Image Upload":


file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    text, _ = extract_text_from_image(path)
    question = st.text_area("Edit OCR text", text)


# -----------------------------

# SOLVE BUTTON

# -----------------------------

if st.button("Solve"):


if question.strip() == "":
    st.warning("Please enter a question")
    st.stop()

agent_trace = []

parsed = parse_question(question)
agent_trace.append({"agent": "Parser", "output": parsed})

if parsed.get("needs_clarification"):
    st.error("Problem unclear")
    st.stop()

topic = route_problem(parsed["problem_text"])
docs = retrieve_context(parsed["problem_text"])

context = "\n".join([str(d) for d in docs])

answer = solve_problem(parsed["problem_text"], context)
verification = verify_solution(parsed["problem_text"], answer)
explanation = explain_solution(parsed["problem_text"], answer, context)

agent_trace.append({"agent": "Solver", "output": answer})
agent_trace.append({"agent": "Verifier", "output": verification})
agent_trace.append({"agent": "Explainer", "output": explanation})

# STORE
st.session_state.answer = answer
st.session_state.explanation = explanation
st.session_state.verification = verification
st.session_state.agent_trace = agent_trace
st.session_state.docs = docs

save_memory({"question": question, "solution": answer})


# -----------------------------

# DISPLAY

# -----------------------------

if st.session_state.answer:


st.subheader("Final Answer")
st.write(st.session_state.answer)

st.subheader("Explanation")
st.write(st.session_state.explanation)

st.subheader("Verification")
st.write(st.session_state.verification)

st.subheader("Agent Trace")
for step in st.session_state.agent_trace:
    with st.expander(step["agent"]):
        st.write(step["output"])

