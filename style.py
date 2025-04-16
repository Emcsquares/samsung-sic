import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .card {
            padding: 1.5rem;
            border-radius: 1rem;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
        .title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1rem;
            color: #888;
        }
        </style>
    """, unsafe_allow_html=True)
