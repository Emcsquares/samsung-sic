import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #111;
            color: #eee;
        }

        .stApp {
            background-color: #121212;
        }

        section[data-testid="stSidebar"] {
            background-color: #1f1f1f;
        }

        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p {
            color: #eee;
        }

        .title {
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #fff;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #aaa;
            margin-bottom: 1rem;
        }

        .stButton > button {
            background-color: #4f46e5;
            color: white;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #6366f1;
            transform: scale(1.03);
        }

        .stMarkdown ul {
            padding-left: 1.5rem;
        }

        .stMarkdown li {
            margin-bottom: 0.4rem;
        }

        hr {
            border: none;
            height: 1px;
            background: #333;
            margin: 1.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
