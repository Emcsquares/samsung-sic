import streamlit as st
from db import get_all_files
from style import apply_custom_styles


def show_ocr_auto_page():
    apply_custom_styles()
    st.title("⚙️ Automatic OCR Processor")
    st.write("This page automatically retrieves and processes OCR documents from the database.")

    # Fetch all files and filter for valid automatic OCR files
    files = [
        file for file in get_all_files()
        if file.get("other_info") != "manual"  # Exclude manual files
    ]

    if not files:
        st.info("No automatic OCR documents found in the database.")
        return

    for i, file in enumerate(files[::-1]):  # Reverse to show the latest files first
        # Use filename or fallback to timestamp
        filename = f"Document_{file.get('timestamp', 'File')}"
        document_id = file.get("_id", {}).get("$oid", "Unknown ID")  # Safely extract `$oid` or fallback
        timestamp = file.get("timestamp", "Unknown Timestamp")
        
        # Safely extract `processing_time` or fallback to 0
        processing_time_raw = file.get("processing_time", {})
        if isinstance(processing_time_raw, dict) and "$numberDouble" in processing_time_raw:
            processing_time = float(processing_time_raw["$numberDouble"])
        else:
            processing_time = float(processing_time_raw) if isinstance(processing_time_raw, (int, float)) else 0

        full_text = file.get("full_text", "No full text available.")
        processed_result = file.get("processed_result", "").strip()  # Ensure processed_result is stripped of whitespace

        # Skip files with empty processed_result
        if not processed_result:
            continue

        with st.expander(f"📄 {filename}"):
            st.markdown("**Preview:**")
            # Display extracted values
            st.markdown(f"- **Document ID:** {document_id}")
            st.markdown(f"- **Timestamp:** {timestamp}")
            st.markdown(f"- **Processing Time:** {processing_time:.2f} seconds")
            st.markdown("**Full Text:**")
            st.code(full_text[:500] + ("..." if len(full_text) > 500 else ""))
            st.markdown("**Processed Result:**")
            st.code(processed_result[:500] + ("..." if len(processed_result) > 500 else ""))
