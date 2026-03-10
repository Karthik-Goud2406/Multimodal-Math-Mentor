import whisper
import streamlit as st


# ----------------------------------------------
# Load model once (important for latency)
# ----------------------------------------------

@st.cache_resource
def load_whisper_model():

    # smaller model for faster inference
    model = whisper.load_model("tiny")

    return model


# ----------------------------------------------
# Speech → Text
# ----------------------------------------------

def audio_to_text(audio_file):

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