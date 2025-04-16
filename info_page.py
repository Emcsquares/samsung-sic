import streamlit as st
from style import apply_custom_styles




def show_info_page():
    apply_custom_styles()

    st.title("ℹ️ Tentang Proyek BSD_OCR")

    st.markdown("""
    ### 🧠 Latar Belakang Masalah
    Penyandang tunanetra di Indonesia menghadapi keterbatasan besar dalam hal navigasi dan interaksi sosial. 
    Banyak dari mereka kesulitan membaca tanda, menentukan arah, hingga menjalin komunikasi.

    > Sekitar **3,75 juta orang** mengalami gangguan penglihatan di Indonesia. Namun hanya **12%** anak disabilitas yang bersekolah. (PERTUNI)

    ### 🎯 Tujuan Proyek
    - Meningkatkan **kemandirian** penyandang tunanetra  
    - Menyediakan solusi yang **portabel**, **murah**, dan **canggih**  
    - Menggabungkan teknologi **IoT + AI** untuk deteksi objek dan navigasi  

    ### 🧩 Teknologi yang Digunakan
    - ESP32, Kamera, GPS, Speaker, Sensor  
    - OpenCV, Tesseract OCR, Text-to-Speech  
    - Google Maps API, MQTT  
    """)

    st.success("Proyek ini berfokus pada inklusi digital dan solusi nyata untuk meningkatkan kualitas hidup tunanetra.")
