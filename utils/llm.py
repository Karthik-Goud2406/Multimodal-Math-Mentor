import os
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

MODEL_NAME = "llama-3.3-70b-versatile"


def _get_client():
    """Create a Groq client using the API key from Streamlit secrets or env."""

    api_key = None

    # 1) Streamlit Cloud secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # 2) Environment variable fallback
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Add it in Streamlit Cloud → Settings → Secrets, "
            "or set it as an environment variable."
        )

    return Groq(api_key=api_key)


# --------------------------------------------------
# NORMAL LLM CALL (used by agents)
# --------------------------------------------------

def call_llm(prompt):

    if Groq is None:
        return "Error: 'groq' package is not installed. Run: pip install groq"

    try:
        client = _get_client()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=500,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"


# --------------------------------------------------
# STREAMING LLM CALL (used by UI)
# --------------------------------------------------

def stream_llm(prompt):

    if Groq is None:
        yield "Error: 'groq' package is not installed. Run: pip install groq"
        return

    try:
        client = _get_client()

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=500,
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except Exception as e:
        yield f"\nLLM Error: {str(e)}"