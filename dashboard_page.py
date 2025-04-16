import streamlit as st
from style import apply_custom_styles
from PIL import Image

def show_dashboard_page():
    apply_custom_styles()



    st.title("👁️‍🗨️ BSD_OCR: Kacamata Pintar untuk Penyandang Tunanetra")
    st.markdown("""
    Solusi wearable berbasis **IoT & AI** yang membantu penyandang tunanetra:
    - Mendeteksi objek sekitar dengan **kamera + computer vision**
    - Memberikan informasi via **suara (text-to-speech)**
    - Menyediakan **navigasi GPS** untuk perjalanan lebih aman
    """)
    st.image("animationAAM.gif")

    st.divider()

    # Tujuan Utama
    st.subheader("🎯 Tujuan Utama")
    st.markdown("""
    - Meningkatkan **kemandirian & keselamatan** pengguna
    - Mengurangi ketergantungan pada alat bantu tradisional
    - Solusi **portabel & terjangkau** untuk semua kalangan
    """)

    st.divider()

    # Komponen Hardware
    st.subheader("🧠 Komponen Hardware")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("sketch.jpeg", caption="Desain Kacamata Pintar", use_container_width=True)
    with col2:
        st.markdown("""
        - **ESP32**: Otak dari sistem
        - **Kamera (OV2640/OV5640)**: Penglihatan digital
        - **GPS Module**: Penentuan posisi
        - **Speaker + DFPlayer Mini**: Output suara
        - **Sensor Ultrasonik / LiDAR**: Deteksi rintangan
        - **Battery + Modul Charger**: Daya portabel
        """)

    st.divider()

    # Komponen Software
    st.subheader("💻 Komponen Software")
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown("""
        - **OpenCV / TensorFlow Lite**: Computer vision
        - **Tesseract OCR**: Ekstraksi teks dari gambar
        - **Text-to-Speech (TTS)**: Umpan balik suara
        - **Algoritma Navigasi (A\*/Dijkstra)**: Jalur teraman
        - **WiFi/Bluetooth + MQTT**: Komunikasi data
        - **Maps API (Google / OSM)**: Navigasi tujuan
        """)
    with col4:
        st.image("flowchart.jpeg", caption="Alur Sistem BSD_OCR", use_container_width=True)

    st.divider()

    # Alur Kerja
    st.subheader("📈 Alur Kerja Sistem BSD_OCR")
    st.markdown("""
    Berikut adalah alur dari sistem wearable yang terhubung dengan AI dan Streamlit:
    """)
    st.success("📌 Sistem ini dirancang untuk mendukung aksesibilitas dan inklusi digital bagi penyandang tunanetra.")
    st.markdown("""
    1. **ESP32 CAM** menangkap gambar secara real-time.
    2. Gambar dikirim ke **OCR Model**:
       - **OpenCV** + **Tesseract** memproses & ekstrak teks.
    3. Jika teks panjang:
       - Disederhanakan dengan **Transformer Bart (ftb)** menggunakan **Huggingface + PyTorch**.
       - Dirangkum oleh modul **Summarizer**.
    4. Teks dikemas dalam format **JSON**.
    5. JSON dikirim ke:
       - **Database** untuk penyimpanan
       - **Ubidots (REST API)** untuk monitoring
       - **Streamlit** untuk ditampilkan secara interaktif
    """)

    st.markdown("---")
