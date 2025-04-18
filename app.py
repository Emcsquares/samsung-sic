import streamlit as st
import uuid  # Import the uuid module for generating unique identifiers
import torch

st.set_page_config(page_title="OCR Document Manager", layout="wide")

# app.py
from documents_page import show_documents_page
from dashboard_page import show_dashboard_page
from ocr_auto_page import show_ocr_auto_page
from db import save_file
from PIL import Image
import time
from info_page import show_info_page
from style import apply_custom_styles
import pytesseract
from transformers import pipeline

# Determine the device (use GPU if available, otherwise CPU)
device = 0 if torch.cuda.is_available() else -1

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    framework="pt",
    device=device  # Explicitly specify the device
)

PAGES = {
    "📊 Dashboard": show_dashboard_page,
    "📄 Documents": show_documents_page,
    "⚙️ Automatic OCR": show_ocr_auto_page,
    "ℹ️ Tentang Proyek": show_info_page
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
    st.header("🕒 Submit Image for Text Recognition + Summary")
    st.subheader("It works better on dekstop (We didn't recommend to use android/ios base device.)")

    uploaded_image = st.file_uploader("Upload an image (JPG/PNG) for OCR", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        try:
            # Load and process the image
            img = Image.open(uploaded_image)
            img = img.convert("RGB")  # Ensure the image is in RGB format

            if st.button("Process Image", key="process_image_button"):
                with st.spinner("🔍 Extracting text..."):
                    start_time = time.time()
                    extracted_text = pytesseract.image_to_string(img)
                    process_time = time.time() - start_time  # Measure processing time

                    if extracted_text.strip():
                        # Summarize the text if it's long
                        if len(extracted_text.split()) > 20:
                            try:
                                with st.spinner("📝 Summarizing text..."):
                                    summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
                                    summarized_text = summary[0]['summary_text']
                                st.session_state["summarized_text"] = summarized_text
                            except Exception as e:
                                st.error(f"Error summarizing the text: {e}")
                        else:
                            st.session_state["summarized_text"] = extracted_text

                        st.session_state["process_time"] = process_time  # Store processing time
                        # Generate a unique filename with a 5-character UUID
                        unique_filename = f"{uuid.uuid4().hex[:5]}_{uploaded_image.name}"
                        st.session_state["uploaded_image_name"] = unique_filename
                        st.success(f"✅ Text processing completed in {process_time:.2f} seconds!")
                    else:
                        st.warning("⚠️ No text detected in the image. Please try another image.")
        except Exception as e:
            st.error(f"Error processing the image: {e}")

    # Display extracted and summarized text
    if "summarized_text" in st.session_state:
        st.subheader("📋 Summarized Text")
        st.code(st.session_state["summarized_text"])

        # Show download button
        st.download_button(
            label="Download Summarized Text",
            data=st.session_state["summarized_text"],
            file_name=f"{st.session_state.get('uploaded_image_name', 'output')}_summary.txt",
            mime="text/plain",
        )

        # Save the result to the database
        if st.button("Save Result", key=f"save_result_button_{st.session_state.get('uploaded_image_name', 'unknown_file')}"):
            try:
                save_file(
                    st.session_state.get("uploaded_image_name", "unknown_file"),
                    st.session_state["summarized_text"],
                    process_time=st.session_state["process_time"],  # Include processing time
                )
                st.success(f"✅ Result saved for '{st.session_state.get('uploaded_image_name', 'unknown_file')}'")
            except Exception as e:
                st.error(f"Error saving the result: {e}")

# Load selected page
page = PAGES[st.session_state["current_page"]]
page()
