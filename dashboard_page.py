import streamlit as st
from style import apply_custom_styles

def show_dashboard_page():
    apply_custom_styles()

    st.markdown("""
    <div class="title">Welcome to OCR Dashboard</div>
    <div class="subtitle">Explore tools, animations, and how OCR works</div>
    """, unsafe_allow_html=True)

    st.subheader("🛠 Tools Used")
    st.markdown("""
    - **Streamlit** for web UI
    - **MongoDB** for database
    - **Python** for logic
    - (Optional) **Tesseract OCR**, **OpenCV**, etc.
    """)

    st.subheader("🎞 How It Works")
    st.markdown("""
    1. Upload a `.json` or `.txt` file containing OCR data.
    2. Files are saved securely in MongoDB.
    3. View, preview, and download stored documents anytime.
    """)

    st.subheader("💡 Future Ideas")
    st.markdown("""
    - Visualize text positions from OCR
    - Convert scanned images to structured data
    - Export to PDF or Excel
    """)
