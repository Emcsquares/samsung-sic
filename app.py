# app.py
import streamlit as st
from documents_page import show_documents_page
from dashboard_page import show_dashboard_page
from ocr_auto_page import show_ocr_auto_page
from db import save_file
from PIL import Image
import time


st.set_page_config(page_title="OCR Document Manager", layout="wide")

PAGES = {
    "📊 Dashboard": show_dashboard_page,
    "📄 Documents": show_documents_page,
    "⚙️ Automatic OCR": show_ocr_auto_page
}

st.sidebar.title("Navigation")

# Sidebar CSS for button style
st.sidebar.markdown("""
<style>
.stButton > button {
    background-color: transparent;
    color: #ccc;
    border: none;
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 500;
    width: 100%;
    border-radius: 0.5rem;
    transition: background 0.3s, color 0.3s;
}
.stButton > button:hover {
    background-color: #4B4B4B;
    color: white;
}
.stButton > button:focus {
    outline: none;
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state["current_page"] = list(PAGES.keys())[0]

for page_name in PAGES:
    if st.sidebar.button(page_name):
        st.session_state["current_page"] = page_name

# Optional timer for long-running tasks (OCR simulation)
if st.session_state["current_page"] == "📊 Dashboard":
    st.header("🕒 OCR + Summary Timer")

    uploaded_image = st.file_uploader("Upload an image (JPG/PNG) for OCR", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Add a fake OCR function to simulate text extraction without tesseract.
        def fake_ocr(img):
            # Simulated OCR extraction logic.
            return "Simulated OCR text from image. Tesseract is not used."

        if st.button("Preview Extracted Text"):
            with st.spinner("🔍 Extracting text..."):
                # Replace tesseract call with fake_ocr function call.
                extracted_text = fake_ocr(img)
                st.session_state["extracted_text_preview"] = extracted_text

        if "extracted_text_preview" in st.session_state:
            st.subheader("📄 Extracted Text Preview")
            st.code(st.session_state["extracted_text_preview"][:2000] + ("..." if len(st.session_state["extracted_text_preview"]) > 2000 else ""))
            if st.button("Save OCR Result"):
                save_file(f"{uploaded_image.name}.txt", st.session_state["extracted_text_preview"])
                st.success(f"✅ OCR text saved as '{uploaded_image.name}.txt'")
                del st.session_state["extracted_text_preview"]

    if "ocr_running" not in st.session_state:
        st.session_state.ocr_running = False
    if "ocr_stop" not in st.session_state:
        st.session_state.ocr_stop = False

    progress_bar = st.empty()
    status_text = st.empty()

    if not st.session_state.ocr_running:
        if st.button("Start OCR Process"):
            st.session_state.ocr_running = True
            st.session_state.ocr_stop = False

    if st.session_state.ocr_running:
        stop_btn = st.button("Stop Process", key="stop")
        start = time.time()

        for i in range(100):
            if stop_btn:
                st.session_state.ocr_stop = True

            if st.session_state.ocr_stop:
                status_text.warning("⚠️ OCR process manually stopped.")
                st.session_state.ocr_running = False
                break

            if time.time() - start > 10:
                status_text.error("❌ OCR process timed out.")
                st.session_state.ocr_running = False
                break

            time.sleep(0.05)
            progress_bar.progress((i + 1) / 100)
            status_text.info(f"🔄 Processing... {i + 1}%")

        else:
            end = time.time()
            status_text.success(f"✅ Completed in {end - start:.2f} seconds")
            st.balloons()
            st.session_state.ocr_running = False
            st.session_state.ocr_stop = False

# Load selected page
page = PAGES[st.session_state["current_page"]]
page()
