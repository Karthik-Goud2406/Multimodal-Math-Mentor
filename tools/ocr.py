import cv2
import easyocr
import streamlit as st


# -------------------------------------------------
# Load OCR model once (important for latency)
# -------------------------------------------------

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(["en"], gpu=False)

# -------------------------------------------------
# Image preprocessing (faster OCR)
# -------------------------------------------------

def preprocess_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # resize large images (reduces OCR time)
    h, w = gray.shape

    if w > 1200:
        scale = 1200 / w
        gray = cv2.resize(gray, None, fx=scale, fy=scale)

    return gray


# -------------------------------------------------
# OCR Extraction
# -------------------------------------------------

def extract_text_from_image(image_path):

    reader = load_ocr_reader()

    image = cv2.imread(image_path)

    if image is None:
        return "", 0.0

    image = preprocess_image(image)

    results = reader.readtext(image)

    if not results:
        return "", 0.0

    texts = []
    confidences = []

    for box, text, conf in results:
        texts.append(text)
        confidences.append(conf)

    extracted_text = " ".join(texts)

    confidence = sum(confidences) / len(confidences)

    return extracted_text, confidence