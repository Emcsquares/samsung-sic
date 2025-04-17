import streamlit as st
from db import get_all_files
from style import apply_custom_styles
import json  # Import JSON for parsing


def show_ocr_auto_page():
    st.title("⚙️ Automatic OCR Processor")
    st.write("This page automatically retrieves and processes OCR documents from the database.")

    files = get_all_files()
    if not files:
        st.info("No OCR documents found in the database.")
        return

    for i, file in enumerate(files[::-1]):
        filename = file.get("filename", "File")  # Fallback to "Unknown" if filename is missing
        content = file.get("content", "")
        if not content.strip():  # Skip files with empty or whitespace-only content
            continue

        with st.expander(f"📄 {filename}"):
            st.markdown("**Preview:**")
            try:
                # Attempt to parse content as JSON
                parsed_content = json.loads(content)
                # Extract specific keys for display
                document_id = parsed_content.get("_id", "N/A")
                timestamp = parsed_content.get("timestamp", "N/A")
                processing_time = parsed_content.get("processing_time", "N/A")
                full_text = parsed_content.get("full_text", "N/A")
                processed_result = parsed_content.get("processed_result", "N/A")

                # Display extracted values
                st.markdown(f"- **Document ID:** {document_id}")
                st.markdown(f"- **Timestamp:** {timestamp}")
                st.markdown(f"- **Processing Time:** {processing_time:.2f} seconds" if isinstance(processing_time, (int, float)) else f"- **Processing Time:** {processing_time}")
                st.markdown("**Full Text:**")
                st.code(full_text[:500] + ("..." if len(full_text) > 500 else ""))
                st.markdown("**Processed Result:**")
                st.code(processed_result[:500] + ("..." if len(processed_result) > 500 else ""))

            except json.JSONDecodeError:
                # If content is not valid JSON, display it as plain text
                st.warning("Content is not valid JSON. Displaying raw content.")
                st.code(content[:500] + ("..." if len(content) > 500 else ""))

            # Simulated summary logic
            word_count = len(content.split())
            st.markdown(f"**Summary:** This file contains approximately `{word_count}` words.")
