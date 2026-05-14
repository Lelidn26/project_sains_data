import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="CarValue - Prediksi Harga Mobil",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ---- VARIABEL WARNA ---- */
    :root {
        --bg-primary:    #0b0b13;
        --bg-secondary:  #10101a;
        --bg-card:       #14141f;
        --bg-input:      #0e0e1a;
        --accent:        #7b68ee;
        --accent-2:      #a99df5;
        --accent-glow:   rgba(123, 104, 238, 0.25);
        --green:         #3ecf8e;
        --yellow:        #f5a623;
        --orange:        #f07740;
        --purple-light:  #c4b5fd;
        --text-primary:  #f0eeff;
        --text-secondary:#a89fc8;
        --text-muted:    #5c5478;
        --text-value:    #ffffff;
        --border:        rgba(123, 104, 238, 0.16);
        --border-strong: rgba(123, 104, 238, 0.35);
        --radius-sm:     8px;
        --radius-md:     13px;
        --radius-lg:     18px;
    }

    /* ---- GLOBAL ---- */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-primary);
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="block-container"] {
        padding: 1.2rem 2rem 3rem 2rem;
        max-width: 1380px;
    }

    /* ============================================
       SIDEBAR
    ============================================ */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-secondary) !important;
        font-size: 0.875rem;
        line-height: 1.75;
    }
    [data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary) !important;
        font-size: 0.875rem;
        line-height: 1.85;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        color: var(--accent-2) !important;
        margin-top: 4px !important;
        margin-bottom: 10px !important;
    }
    [data-testid="stSidebar"] strong {
        color: var(--accent-2) !important;
    }
    [data-testid="stExpander"] {
        background: rgba(123, 104, 238, 0.05) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        margin-bottom: 4px;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }

    /* ---- Logo sidebar ---- */
    .sidebar-logo {
        text-align: center;
        padding: 24px 0 22px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 20px;
    }
    .sidebar-logo .logo-icon {
        font-size: 2.4rem;
        display: block;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 12px var(--accent-glow));
    }
    .sidebar-logo .logo-name {
        font-size: 1.3rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .sidebar-logo .logo-name span {
        background: linear-gradient(135deg, #7b68ee, #b8a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-logo .logo-sub {
        font-size: 0.68rem;
        color: var(--text-muted);
        font-weight: 600;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* ---- Badge sidebar ---- */
    .sb-badge {
        background: rgba(123, 104, 238, 0.09);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.82rem;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sb-badge strong { color: var(--accent-2) !important; }

    /* ---- Segmen harga sidebar ---- */
    .seg-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 2px;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 0.83rem;
        color: var(--text-secondary);
    }
    .seg-row:last-child { border-bottom: none; }
    .seg-row .seg-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: var(--accent-2);
        font-weight: 600;
    }

    /* ============================================
       HERO HEADER
    ============================================ */
    .hero-wrap {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0d0c1c 0%, #111028 60%, #0c101a 100%);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-lg);
        padding: 36px 48px 32px 48px;
        margin-bottom: 24px;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -100px; right: -80px;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(123,104,238,0.18) 0%, transparent 70%);
        border-radius: 50%;
        animation: hero-pulse 5s ease-in-out infinite alternate;
    }
    @keyframes hero-pulse {
        from { opacity: 0.5; transform: scale(1); }
        to   { opacity: 1;   transform: scale(1.1); }
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--text-primary);
        line-height: 1.1;
        margin: 0 0 10px 0;
        letter-spacing: -1px;
    }
    .hero-title span {
        background: linear-gradient(135deg, #7b68ee, #b8a8ff, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-desc {
        font-size: 0.97rem;
        color: var(--text-secondary);
        max-width: 500px;
        line-height: 1.65;
        margin: 0 0 22px 0;
    }
    .hero-stats {
        display: flex;
        gap: 0;
        flex-wrap: wrap;
    }
    .hero-stat {
        padding: 0 24px 0 0;
        margin-right: 24px;
        border-right: 1px solid var(--border-strong);
    }
    .hero-stat:last-child {
        border-right: none;
        margin-right: 0;
    }
    .hero-stat .sn {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
    }
    .hero-stat .sl {
        font-size: 0.66rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-top: 2px;
    }

    /* ============================================
       PANEL INPUT - SECTION HEADER
    ============================================ */
    .panel-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 22px 24px 24px 24px;
        margin-bottom: 14px;
        transition: border-color 0.3s;
    }
    .panel-section:hover {
        border-color: var(--border-strong);
    }
    .section-head {
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .section-head .sh-icon {
        font-size: 0.95rem;
    }

    /* ============================================
       INPUT FIELDS - KONTRAS TINGGI
    ============================================ */
    /* Label input */
    .stNumberInput label,
    .stSlider label {
        color: var(--text-secondary) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
    }

    /* Kotak input number */
    [data-testid="stNumberInput"] div[data-baseweb="input"] {
        background: #181825 !important;
        border: 1.5px solid rgba(123, 104, 238, 0.30) !important;
        border-radius: var(--radius-sm) !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(123, 104, 238, 0.18) !important;
    }
    /* Angka di dalam input - PUTIH TEGAS */
    [data-testid="stNumberInput"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.96rem !important;
    font-weight: 700 !important;
    background: transparent !important;
    caret-color: #ffffff !important;
    }
    /* Tombol plus / minus */
    [data-testid="stNumberInput"] button {
    color: #ffffff !important;
    opacity: 1 !important;
    background: rgba(123, 104, 238, 0.18) !important;
    border: none !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    }
    [data-testid="stNumberInput"] button:hover {
        background: rgba(123, 104, 238, 0.30) !important;
        color: #ffffff !important;
    }

    /* Slider nilai teks */
    [data-testid="stSlider"] p {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    /* Slider thumb */
    [data-testid="stSlider"] div[role="slider"] {
        background: var(--accent) !important;
        border: 2px solid #c4b5fd !important;
        box-shadow: 0 0 10px var(--accent-glow) !important;
    }

    /* ============================================
       TOMBOL PREDIKSI
    ============================================ */
    div.stButton > button {
        background: linear-gradient(135deg, #6c5ce7 0%, #8b78ff 100%) !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 14px 0 !important;
        border-radius: var(--radius-md) !important;
        border: none !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(108, 92, 231, 0.40) !important;
        transition: all 0.22s ease !important;
        margin-top: 4px !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #7d6ff0 0%, #9d8dff 100%) !important;
        box-shadow: 0 6px 28px rgba(108, 92, 231, 0.60) !important;
        transform: translateY(-2px) !important;
    }
    div.stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 10px rgba(108, 92, 231, 0.30) !important;
    }

    /* ============================================
       PANEL HASIL - PLACEHOLDER
    ============================================ */
    .result-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 28px 26px;
        min-height: 520px;
        display: flex;
        flex-direction: column;
        transition: border-color 0.3s;
    }
    .result-panel:hover {
        border-color: var(--border-strong);
    }

    /* Placeholder sebelum klik prediksi */
    .ph-wrap {
    flex: 1;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 30px;
    }
    .ph-icon {
        font-size: 3.5rem;
        margin-bottom: 18px;
        animation: float 3.5s ease-in-out infinite;
        filter: drop-shadow(0 0 18px var(--accent-glow));
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%       { transform: translateY(-10px); }
    }
    .ph-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    .ph-desc {
        font-size: 0.86rem;
        color: var(--text-muted);
        line-height: 1.7;
        max-width: 240px;
    }
    .ph-desc strong { color: var(--accent-2); }

    /* ============================================
       TAMPILAN HASIL PREDIKSI
    ============================================ */
    .price-eyebrow {
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--accent-2);
        text-align: center;
        margin-bottom: 12px;
    }
    .price-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        line-height: 1;
        margin-bottom: 6px;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(180, 165, 255, 0.40);
        animation: fadein 0.45s ease-out;
    }
    .price-sub {
        font-size: 0.82rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
        text-align: center;
        margin-bottom: 20px;
    }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .divider-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-strong), transparent);
        margin: 18px 0;
    }

    /* Badge kategori */
    .cat-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 9px 20px;
        border-radius: 50px;
        font-size: 0.88rem;
        font-weight: 700;
        margin: 0 auto 8px auto;
        width: fit-content;
        animation: pop 0.35s ease-out 0.1s both;
    }
    @keyframes pop {
        from { opacity: 0; transform: scale(0.88); }
        to   { opacity: 1; transform: scale(1); }
    }
    .cat-ekonomi  { background: rgba(62, 207, 142, 0.13); border: 1px solid rgba(62, 207, 142, 0.35); color: #3ecf8e; }
    .cat-menengah { background: rgba(245, 166, 35, 0.13);  border: 1px solid rgba(245, 166, 35, 0.35);  color: #f5a623; }
    .cat-premium  { background: rgba(240, 119, 64, 0.13);  border: 1px solid rgba(240, 119, 64, 0.35);  color: #f07740; }
    .cat-luxury   { background: rgba(196, 181, 253, 0.13); border: 1px solid rgba(196, 181, 253, 0.38); color: #c4b5fd; }

    .cat-desc {
        font-size: 0.82rem;
        color: var(--text-secondary);
        text-align: center;
        line-height: 1.55;
        margin-bottom: 20px;
    }

    /* Label bagian ringkasan */
    .sub-label {
        font-size: 0.66rem;
        font-weight: 700;
        color: var(--accent-2);
        letter-spacing: 2.2px;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sub-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* Grid ringkasan spesifikasi */
    .spec-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .spec-cell {
        background: rgba(123, 104, 238, 0.07);
        border: 1px solid rgba(123, 104, 238, 0.13);
        border-radius: var(--radius-sm);
        padding: 10px 13px;
        transition: background 0.2s;
    }
    .spec-cell:hover {
        background: rgba(123, 104, 238, 0.13);
    }
    .spec-cell .sc-label {
        font-size: 0.64rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.1px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .spec-cell .sc-val {
        font-size: 0.94rem;
        font-weight: 700;
        color: #f0eeff;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ============================================
       ALERT / ERROR
    ============================================ */
    [data-testid="stAlert"] {
        background: rgba(123, 104, 238, 0.08) !important;
        border: 1px solid rgba(123, 104, 238, 0.22) !important;
        border-radius: var(--radius-md) !important;
    }
    [data-testid="stAlert"] p {
        color: var(--text-secondary) !important;
    }

    /* ---- Lain-lain ---- */
    hr { border-color: var(--border) !important; }
    .stCaption { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# MUAT MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model, True
    except FileNotFoundError:
        return None, False

model, model_loaded = load_model()


# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">Car<span>Value</span></h1>
    <p class="hero-desc">
        Sistem prediksi harga mobil berbasis kecerdasan buatan.
        Masukkan spesifikasi kendaraan dan dapatkan estimasi harga pasar secara instan.
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="sn">157</div>
            <div class="sl">Data Latih</div>
        </div>
        <div class="hero-stat">
            <div class="sn">9</div>
            <div class="sl">Fitur Prediktor</div>
        </div>
        <div class="hero-stat">
            <div class="sn">Linear</div>
            <div class="sl">Algoritma</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Pesan error jika model tidak ditemukan
if not model_loaded:
    st.error("""
    **File `model.pkl` tidak ditemukan.**

    Pastikan file `model.pkl` berada di folder yang sama dengan `app.py`:
    ```
    project/
    ├── app.py
    ├── model.pkl   <- letakkan di sini
    └── ...
    ```
    """)
    st.stop()


# ============================================================
# LAYOUT UTAMA
# ============================================================
col_input, col_result = st.columns([1.15, 0.95], gap="medium")


# ============================================================
# KOLOM KIRI - INPUT SPESIFIKASI
# ============================================================
with col_input:

    # --- MESIN & PERFORMA ---
    with st.container():
        st.markdown("""
        <div style="
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 22px 24px 0px;
            margin-bottom: 14px;
        ">
            <div class="section-head">
                <span>⚙️</span> Mesin &amp; Performa
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            engine_size = st.number_input(
                "Ukuran Mesin (liter)",
                min_value=0.5, max_value=8.0, value=2.5, step=0.1,
                help="Volume silinder mesin dalam liter. Contoh: 1.6, 2.0, 3.5"
            )
            horsepower = st.number_input(
                "Horsepower (HP)",
                min_value=50.0, max_value=600.0, value=150.0, step=5.0,
                help="Output tenaga mesin dalam satuan horsepower (HP)"
            )
        with c2:
            power_perf_factor = st.number_input(
                "Power Perf Factor",
                min_value=10.0, max_value=300.0, value=60.0, step=1.0,
                help="Indeks gabungan performa dan daya kendaraan"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DIMENSI KENDARAAN ---
    with st.container():
        st.markdown("""
        <div style="
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 22px 24px 0px;
            margin-bottom: 14px;
        ">
            <div class="section-head">
                <span>📐</span> Dimensi Kendaraan
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            wheelbase = st.number_input(
                "Wheelbase (inci)",
                min_value=80.0, max_value=160.0, value=107.0, step=0.5,
                help="Jarak antara sumbu roda depan dan belakang dalam inci"
            )
            width = st.number_input(
                "Lebar Kendaraan (inci)",
                min_value=55.0, max_value=90.0, value=70.0, step=0.5,
                help="Lebar total kendaraan dalam satuan inci"
            )
        with c4:
            length = st.number_input(
                "Panjang Kendaraan (inci)",
                min_value=130.0, max_value=250.0, value=185.0, step=1.0,
                help="Panjang total kendaraan dalam satuan inci"
            )
            curb_weight = st.number_input(
                "Berat Kosong (ribu pon)",
                min_value=1.0, max_value=7.0, value=3.2, step=0.1,
                help="Berat kendaraan tanpa penumpang dalam ribuan pon"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BAHAN BAKAR ---
    with st.container():
        st.markdown("""
        <div style="
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 22px 24px 0px;
            margin-bottom: 14px;
        ">
            <div class="section-head">
                <span>⛽</span> Efisiensi Bahan Bakar
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        fuel_capacity = st.number_input(
            "Kapasitas Tangki (galon)",
            min_value=5.0, max_value=40.0, value=16.0, step=0.5,
            help="Kapasitas tangki bahan bakar dalam satuan galon"
        )
        st.markdown("""
            <div style="
                height:1px;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(123,104,238,0.35),
                    transparent
                );
                margin: 18px 0 18px 0;
            "></div>
            """, unsafe_allow_html=True)
        fuel_efficiency = st.slider(
            "Efisiensi BBM (mil per galon / mpg)",
            min_value=10.0, max_value=60.0, value=26.0, step=1.0,
            help="Jarak tempuh per galon bahan bakar dalam satuan mpg"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Tombol prediksi
    predict_button = st.button("🔮  Hitung Prediksi Harga", use_container_width=True)


# ============================================================
# KOLOM KANAN - HASIL PREDIKSI
# ============================================================
with col_result:

    if predict_button:
        input_data = pd.DataFrame({
            'Engine_size'      : [engine_size],
            'Horsepower'       : [horsepower],
            'Wheelbase'        : [wheelbase],
            'Width'            : [width],
            'Length'           : [length],
            'Curb_weight'      : [curb_weight],
            'Fuel_capacity'    : [fuel_capacity],
            'Fuel_efficiency'  : [fuel_efficiency],
            'Power_perf_factor': [power_perf_factor]
        })

        predicted_thousands = model.predict(input_data)[0]
        predicted_usd = predicted_thousands * 1000

        # Kategori
        if predicted_usd < 15000:
            cat_cls, cat_label, cat_desc = (
                "cat-ekonomi", "Kelas Ekonomi",
                "Kendaraan segmen ekonomi - pilihan hemat untuk kebutuhan harian."
            )
        elif predicted_usd < 30000:
            cat_cls, cat_label, cat_desc = (
                "cat-menengah", "Kelas Menengah",
                "Kendaraan segmen menengah - fitur lengkap dengan kenyamanan optimal."
            )
        elif predicted_usd < 50000:
            cat_cls, cat_label, cat_desc = (
                "cat-premium", "Kelas Premium",
                "Kendaraan segmen premium - performa tinggi dengan teknologi terkini."
            )
        else:
            cat_cls, cat_label, cat_desc = (
                "cat-luxury", "Kelas Mewah",
                "Kendaraan segmen mewah - spesifikasi kelas atas dan kemewahan penuh."
            )

        st.markdown(f"""
        <div class="price-eyebrow">Estimasi Harga Pasar</div>
        <div class="price-number">${predicted_usd:,.0f}</div>
        <div class="price-sub">setara ${predicted_thousands:.2f} ribu USD</div>
        <div style="text-align:center;">
            <div class="cat-badge {cat_cls}">&#9679; &nbsp;{cat_label}</div>
        </div>
        <div class="cat-desc">{cat_desc}</div>
        <div class="divider-line"></div>
        <div class="sub-label">Ringkasan Spesifikasi</div>
        <div class="spec-grid">
            <div class="spec-cell">
                <div class="sc-label">Ukuran Mesin</div>
                <div class="sc-val">{engine_size} L</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Horsepower</div>
                <div class="sc-val">{int(horsepower)} HP</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Wheelbase</div>
                <div class="sc-val">{wheelbase} in</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Lebar Kendaraan</div>
                <div class="sc-val">{width} in</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Panjang Kendaraan</div>
                <div class="sc-val">{int(length)} in</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Berat Kosong</div>
                <div class="sc-val">{curb_weight}k lbs</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Kapasitas Tangki</div>
                <div class="sc-val">{fuel_capacity} gal</div>
            </div>
            <div class="spec-cell">
                <div class="sc-label">Efisiensi BBM</div>
                <div class="sc-val">{int(fuel_efficiency)} mpg</div>
            </div>
            <div class="spec-cell" style="grid-column:1/-1;">
                <div class="sc-label">Power Perf Factor</div>
                <div class="sc-val">{power_perf_factor}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            background: rgba(123,104,238,0.05);
            border: 1px solid rgba(123,104,238,0.18);
            border-radius: 18px;
            padding: 30px 24px;
        ">
        <div class="ph-wrap">
            <div class="ph-icon">🚘</div>
            <div class="ph-title">Siap Menghitung Harga</div>
            <div class="ph-desc">
                Isi spesifikasi kendaraan di panel kiri,
                lalu klik <strong>Hitung Prediksi Harga</strong>
                untuk mendapatkan estimasi harga instan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🚘</span>
        <div class="logo-name">Car<span>Value</span></div>
        <div class="logo-sub">Prediksi Harga Mobil</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Cara Penggunaan")
    st.markdown("""
    1. Isi spesifikasi kendaraan pada panel input di kiri.
    2. Klik tombol **Hitung Prediksi Harga**.
    3. Hasil estimasi harga tampil di panel kanan.
    """)

    st.markdown("---")
    st.markdown("## Informasi Model")
    st.markdown("""
    <div class="sb-badge">🧠 <span><strong>Algoritma:</strong> Linear Regression</span></div>
    <div class="sb-badge">📦 <span><strong>Dataset:</strong> Data Penjualan Mobil</span></div>
    <div class="sb-badge">🔢 <span><strong>Jumlah Data:</strong> 157 kendaraan</span></div>
    <div class="sb-badge">📊 <span><strong>Prediktor:</strong> 9 variabel</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Segmen Harga")
    st.markdown("""
    <div class="seg-row"><span>🟢 Ekonomi</span><span class="seg-val">&lt; $15.000</span></div>
    <div class="seg-row"><span>🟡 Menengah</span><span class="seg-val">$15k - $30k</span></div>
    <div class="seg-row"><span>🟠 Premium</span><span class="seg-val">$30k - $50k</span></div>
    <div class="seg-row"><span>🔵 Mewah</span><span class="seg-val">&gt; $50.000</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Panduan Fitur Input")
    with st.expander("Mesin & Performa", expanded=False):
        st.markdown("""
        - **Ukuran Mesin** - Volume silinder dalam liter (0.5 - 8.0 L)
        - **Horsepower** - Output daya mesin dalam HP (50 - 600)
        - **Power Perf Factor** - Indeks gabungan performa kendaraan
        """)
    with st.expander("Dimensi Kendaraan", expanded=False):
        st.markdown("""
        - **Wheelbase** - Jarak antar sumbu roda dalam inci
        - **Lebar Kendaraan** - Lebar total kendaraan dalam inci
        - **Panjang Kendaraan** - Panjang total kendaraan dalam inci
        - **Berat Kosong** - Berat kendaraan tanpa penumpang (ribu pon)
        """)
    with st.expander("Bahan Bakar", expanded=False):
        st.markdown("""
        - **Kapasitas Tangki** - Volume tangki dalam satuan galon
        - **Efisiensi BBM** - Jarak tempuh per galon bahan bakar (mpg)
        """)