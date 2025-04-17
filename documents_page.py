import streamlit as st
from db import save_file, get_all_files, download_all_files
# Add auto-refresh function (requires streamlit_autorefresh)
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    def st_autorefresh(interval, key):
        # Fallback: no auto-refresh; returns 0 or any default value.
        return 0

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
        .last-upload {
            font-size: 1rem; /* Adjusted font size for Last Upload */
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🗂️ OCR Documents")

    stats = get_all_files()
    last_upload = stats[-1].get('filename', "N/A") if stats else "N/A"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Uploaded Files</div><div class='metric-value'>{len(stats)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Last Upload</div><div class='last-upload'>{last_upload}</div></div>", unsafe_allow_html=True)
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

    # Divide page into two tabs
    tabs = st.tabs(["Manual OCR Files"])
    with tabs[0]:
        st.subheader("Manual OCR Files")
        manual_files = [f for f in get_all_files() if f.get('filename', '').endswith(".txt") and f.get('content', '').strip()]
        if manual_files:
            for file in manual_files[::-1]:
                filename = file.get("filename", "Unknown")
                content = file.get("content", "")
                with st.expander(filename):
                    st.code(content)
        else:
            st.info("No manual OCR files found.")

    st.title("📄 Documents - Manual OCR Results")

    # Fetch all saved files from MongoDB
    files = [file for file in get_all_files() if file.get("other_info") == "manual"]  # Filter for manual files

    if files:
        for index, file in enumerate(files):  # Add an index to ensure unique keys
            filename = file.get("filename", "Unknown File")
            content = file.get("content", "No content available.")
            process_time = file.get("process_time", "N/A")

            st.subheader(f"📄 {filename}")
            st.text(f"Processing Time: {process_time} seconds")
            st.code(content)
            st.download_button(
                label="Download File",
                data=content,
                file_name=filename,
                mime="text/plain",
                key=f"download_button_{index}"  # Unique key for each button
            )
    else:
        st.info("No documents found. Please process and save OCR results.")

if __name__ == "__main__":
    show_documents_page()

