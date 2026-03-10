import streamlit as st

# ----------------------------------------------
# Try to import whisper (may not be available
# on Streamlit Cloud due to size / ffmpeg)
# ----------------------------------------------

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


# ----------------------------------------------
# Load model once (important for latency)
# ----------------------------------------------

@st.cache_resource
def load_whisper_model():

    if not WHISPER_AVAILABLE:
        return None

    # smaller model for faster inference
    model = whisper.load_model("tiny")

    return model


# ----------------------------------------------
# Speech → Text
# ----------------------------------------------

def audio_to_text(audio_file):

    if not WHISPER_AVAILABLE:
        return (
            "⚠️ Speech-to-text is not available in this deployment. "
            "The Whisper model requires resources that exceed "
            "Streamlit Cloud limits. Please use text input or "
            "image upload instead."
        )

    model = load_whisper_model()

    try:

        result = model.transcribe(
            audio_file,
            fp16=False
        )

        transcript = result["text"]

        return transcript.strip()

    except Exception as e:

        return f"Speech recognition error: {str(e)}"