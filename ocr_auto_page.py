import streamlit as st
from db import get_all_files
from style import apply_custom_styles



def show_ocr_auto_page():
    st.title("⚙️ Automatic OCR Processor")
    st.write("This page automatically retrieves and processes OCR documents from the database.")

    files = get_all_files()
    if not files:
        st.info("No OCR documents found in the database.")
        return

    for i, file in enumerate(files[::-1]):
        with st.expander(f"📄 {file['filename']}"):
            st.markdown("**Preview:**")
            st.code(file['content'][:500] + ("..." if len(file['content']) > 500 else ""))

            # Simulated summary logic
            word_count = len(file['content'].split())
            st.markdown(f"**Summary:** This file contains approximately `{word_count}` words.")
