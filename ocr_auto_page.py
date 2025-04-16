import streamlit as st
import json
from db import get_all_files

# Attempt to import auto-refresh; otherwise, define a fallback.
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    def st_autorefresh(interval, key):
        return 0

def show_ocr_auto_page():
    st.title("⚙️ Automatic OCR")
    st.markdown(
        "This page automatically refreshes every 5 seconds. It retrieves OCR files from MongoDB "
        "in JSON format and displays them as formatted text."
    )

    st_autorefresh(interval=5000, key="ocr_auto_refresh")

    files = get_all_files()
    if not files:
        st.info("No OCR files found in the database.")
    else:
        for file in files:
            filename = file.get("filename", "Unknown")
            content = file.get("content", "")
            # If the file is in JSON format, parse and reformat it.
            if filename.endswith('.json'):
                try:
                    parsed = json.loads(content)
                    content = json.dumps(parsed, indent=2)
                except Exception as e:
                    st.error(f"Error parsing JSON from {filename}: {e}")
            st.markdown(f"### {filename}")
            st.code(content)
