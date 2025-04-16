import streamlit as st
from db import save_file, get_all_files, download_all_files

def show_documents_page():
    st.markdown("""
        <style>
        .metric-card {
            background: #1e1e1e;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            text-align: center;
        }
        .metric-label {
            color: #aaa;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🗂️ OCR Documents")

    stats = get_all_files()
    last_upload = stats[-1]['filename'] if stats else "N/A"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Uploaded Files</div><div class='metric-value'>{len(stats)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Last Upload</div><div class='metric-value'>{last_upload}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='metric-label'>File Format</div><div class='metric-value'>json / txt</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><div class='metric-label'>⬇ Download All Files</div>", unsafe_allow_html=True)
        st.download_button("Download", download_all_files(), file_name="all_files.txt", use_container_width=True)

    st.divider()

    with st.expander("📤 Upload OCR File", expanded=True):
        uploaded_file = st.file_uploader("Choose a .json or .txt file", type=["json", "txt"])
        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8")
            save_file(uploaded_file.name, content)
            st.success(f"File '{uploaded_file.name}' saved to database")

    st.subheader("📚 Stored Files")
    stored_files = get_all_files()
    if stored_files:
        for f in stored_files[::-1]:
            with st.container():
                st.markdown(f"**📝 {f['filename']}**")
                st.code(f['content'][:500] + ("..." if len(f['content']) > 500 else ""))

    st.title("📄 Documents")
    st.write("List of OCR documents generated from manual processing:")
    files = get_all_files()
    if not files:
        st.info("No OCR documents found. Please run manual OCR from the Dashboard.")
        return
    for file in files:
        with st.expander(file["filename"]):
            st.code(file["content"])

