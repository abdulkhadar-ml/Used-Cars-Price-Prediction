import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import streamlit_antd_components as sac
import base64
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RideRepublic · Smart Car Pricing",
    page_icon="riderepublic_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Logo Helper ───────────────────────────────────────────────────────────────
def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

# ── Theme Toggle ──────────────────────────────────────────────────────────────
with st.sidebar:
    mode = sac.switch(label='Theme', align='start', size='md', on_label='🌙', off_label='☀️')

# ── CSS ───────────────────────────────────────────────────────────────────────
DARK_BG   = "#0A0A0F"
DARK_CARD = "#13131A"
DARK_BORDER = "#2A2A3A"
ACCENT    = "#E8B84B"
ACCENT2   = "#FF6B6B"
LIGHT_BG  = "#F4F1EC"
LIGHT_CARD = "#FFFFFF"
LIGHT_BORDER = "#E0D9CF"

if mode:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background-color: {DARK_BG};
        background-image: radial-gradient(ellipse at 20% 0%, rgba(232,184,75,0.07) 0%, transparent 60%),
                          radial-gradient(ellipse at 80% 100%, rgba(255,107,107,0.05) 0%, transparent 60%);
        color: #E8E8F0;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {DARK_CARD} !important;
        border-right: 1px solid {DARK_BORDER} !important;
    }}

    [data-testid="stSidebarNav"] {{ display: none !important; }}

    div.stButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, #D4A43A 100%) !important;
        color: #0A0A0F !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.5rem !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(232,184,75,0.3) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(232,184,75,0.45) !important;
    }}

    [data-testid="stDownloadButton"] button {{
        background: linear-gradient(135deg, #1E1E2E 0%, #2A2A3A 100%) !important;
        color: {ACCENT} !important;
        border: 1px solid {ACCENT} !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: linear-gradient(135deg, {ACCENT} 0%, #D4A43A 100%) !important;
        color: #0A0A0F !important;
    }}

    .hero-section {{
        background: linear-gradient(135deg, {DARK_CARD} 0%, #1A1A2E 100%);
        border: 1px solid {DARK_BORDER};
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(232,184,75,0.08) 0%, transparent 70%);
        pointer-events: none;
    }}

    .hero-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }}
    .hero-accent {{
        color: {ACCENT};
    }}
    .hero-sub {{
        font-size: 1.05rem;
        color: #8888AA;
        margin-top: 0.5rem;
        font-weight: 300;
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(232,184,75,0.12);
        border: 1px solid rgba(232,184,75,0.3);
        color: {ACCENT};
        border-radius: 50px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }}

    .kpi-card {{
        background: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        transition: border-color 0.2s;
    }}
    .kpi-card:hover {{ border-color: {ACCENT}; }}
    .kpi-icon {{ font-size: 1.8rem; margin-bottom: 0.4rem; }}
    .kpi-value {{
        font-family: 'Syne', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: {ACCENT};
    }}
    .kpi-label {{
        font-size: 0.78rem;
        color: #8888AA;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }}

    .result-card {{
        background: linear-gradient(135deg, #13131A 0%, #1A1A2E 100%);
        border: 1px solid rgba(232,184,75,0.4);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(232,184,75,0.1);
    }}
    .result-label {{
        font-size: 0.85rem;
        color: #8888AA;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    .result-price {{
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: {ACCENT};
        line-height: 1;
    }}
    .result-range {{
        font-size: 0.9rem;
        color: #8888AA;
        margin-top: 0.5rem;
    }}
    .result-range span {{
        color: #71ef99;
        font-weight: 600;
    }}

    .section-header {{
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .section-header::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, {DARK_BORDER}, transparent);
    }}

    .tip-card {{
        background: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-left: 3px solid {ACCENT};
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        font-size: 0.9rem;
        color: #C8C8D8;
        line-height: 1.5;
    }}
    .tip-card strong {{ color: {ACCENT}; }}

    .about-card {{
        background: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 20px;
        padding: 2rem;
    }}
    .about-tag {{
        display: inline-block;
        background: rgba(232,184,75,0.1);
        border: 1px solid rgba(232,184,75,0.25);
        color: {ACCENT};
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 4px;
    }}

    .footer-bar {{
        background: {DARK_CARD};
        border-top: 1px solid {DARK_BORDER};
        border-radius: 16px;
        padding: 1rem 2rem;
        text-align: center;
        color: #555570;
        font-size: 0.8rem;
        margin-top: 2rem;
    }}

    [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-family: 'Syne', sans-serif !important; }}
    [data-testid="stMetricLabel"] {{ color: #8888AA !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}

    .sidebar-label {{
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        color: #8888AA;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background-color: {LIGHT_BG};
        background-image: radial-gradient(ellipse at 20% 0%, rgba(180,140,40,0.06) 0%, transparent 60%);
        color: #1A1A2E;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {LIGHT_CARD} !important;
        border-right: 1px solid {LIGHT_BORDER} !important;
    }}

    [data-testid="stSidebarNav"] {{ display: none !important; }}

    div.stButton > button {{
        background: linear-gradient(135deg, #1A1A2E 0%, #2A2A4E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(26,26,46,0.2) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(26,26,46,0.3) !important;
    }}

    [data-testid="stDownloadButton"] button {{
        background: {LIGHT_CARD} !important;
        color: #1A1A2E !important;
        border: 1.5px solid #1A1A2E !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        width: 100% !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: #1A1A2E !important;
        color: white !important;
    }}

    .hero-section {{
        background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(232,184,75,0.1) 0%, transparent 70%);
        pointer-events: none;
    }}

    .hero-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }}
    .hero-accent {{ color: {ACCENT}; }}
    .hero-sub {{
        font-size: 1.05rem;
        color: rgba(255,255,255,0.6);
        margin-top: 0.5rem;
        font-weight: 300;
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(232,184,75,0.15);
        border: 1px solid rgba(232,184,75,0.4);
        color: {ACCENT};
        border-radius: 50px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }}

    .kpi-card {{
        background: {LIGHT_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .kpi-card:hover {{
        border-color: #1A1A2E;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    .kpi-icon {{ font-size: 1.8rem; margin-bottom: 0.4rem; }}
    .kpi-value {{
        font-family: 'Syne', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #1A1A2E;
    }}
    .kpi-label {{
        font-size: 0.78rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }}

    .result-card {{
        background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(26,26,46,0.2);
    }}
    .result-label {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    .result-price {{
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: {ACCENT};
        line-height: 1;
    }}
    .result-range {{
        font-size: 0.9rem;
        color: rgba(255,255,255,0.5);
        margin-top: 0.5rem;
    }}
    .result-range span {{ color: #71ef99; font-weight: 600; }}

    .section-header {{
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #1A1A2E;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .section-header::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, {LIGHT_BORDER}, transparent);
    }}

    .tip-card {{
        background: {LIGHT_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-left: 3px solid #1A1A2E;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        font-size: 0.9rem;
        color: #444;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .tip-card strong {{ color: #1A1A2E; }}

    .about-card {{
        background: {LIGHT_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .about-tag {{
        display: inline-block;
        background: #F0EDE8;
        border: 1px solid {LIGHT_BORDER};
        color: #1A1A2E;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 4px;
    }}

    .footer-bar {{
        background: {LIGHT_CARD};
        border-top: 1px solid {LIGHT_BORDER};
        border-radius: 16px;
        padding: 1rem 2rem;
        text-align: center;
        color: #AAA;
        font-size: 0.8rem;
        margin-top: 2rem;
    }}

    [data-testid="stMetricValue"] {{ color: #1A1A2E !important; font-family: 'Syne', sans-serif !important; }}
    [data-testid="stMetricLabel"] {{ color: #888 !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# ── Brand Logos ───────────────────────────────────────────────────────────────
brand_logos = {
    "BMW":"bmw.png", "Audi":"audi.png", "Chevrolet":"chevrolet.webp",
    "Ford":"ford.jpeg", "Honda":"honda.png", "Hyundai":"hyundai.png",
    "Mahindra":"mahindra1.jpeg", "Maruti":"maruti.jpeg",
    "Mercedes-Benz":"mercedes-benz.png", "Nissan":"nissan.png",
    "Renault":"renault.png", "Skoda":"skoda.jpg",
    "Tata":"tata.webp", "Toyota":"toyota.png"
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
if logo_b64:
    st.sidebar.markdown(
        f"""<div style="text-align:center; padding: 1rem 0 0.5rem 0;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:70px; height:70px; border-radius:50%; object-fit:cover;
                        box-shadow:0 4px 15px rgba(232,184,75,0.3);" />
            <p style="margin:8px 0 0 0; font-family:'Syne',sans-serif; font-weight:700;
                      font-size:1rem; {'color:#E8B84B' if mode else 'color:#1A1A2E'};">RideRepublic</p>
        </div>""",
        unsafe_allow_html=True
    )

st.sidebar.markdown("<hr style='border-color: rgba(128,128,128,0.2); margin: 0.5rem 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.7rem; font-weight:700; letter-spacing:1px; opacity:0.5; text-transform:uppercase; margin:0.8rem 0 0.3rem 0;'>Car Details</p>", unsafe_allow_html=True)

brands = [
    "Nissan","Audi","Chevrolet","Ford","Honda","Hyundai",
    "Mahindra","Maruti","Mercedes-Benz","BMW",
    "Renault","Skoda","Tata","Toyota","Other"
]

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0
rc = st.session_state.reset_counter

brand        = st.sidebar.selectbox("🚘 Brand", brands, index=0, key=f"brand_{rc}")
year         = st.sidebar.number_input("📅 Year", 2000, 2026, 2018, key=f"year_{rc}")
km_driven    = st.sidebar.number_input("🛣️ KM Driven", 0, 300000, 40000, key=f"km_{rc}")
mileage      = st.sidebar.number_input("⛽ Mileage (km/l)", 5.0, 40.0, 18.0, key=f"mileage_{rc}")
engine       = st.sidebar.number_input("🔧 Engine (CC)", 800, 5000, 1500, key=f"engine_{rc}")
seats        = st.sidebar.number_input("💺 Seats", 2, 10, 5, key=f"seats_{rc}")
owner_label  = st.sidebar.selectbox("👤 Owner Type", ["First Owner","Second Owner","Third Owner","Fourth & Above Owner"], index=0, key=f"owner_{rc}")
fuel         = st.sidebar.selectbox("🔥 Fuel", ["Diesel","Petrol","LPG"], index=0, key=f"fuel_{rc}")
transmission = st.sidebar.selectbox("⚙️ Transmission", ["Manual","Automatic"], index=0, key=f"transmission_{rc}")
seller_type  = st.sidebar.selectbox("🏪 Seller Type", ["Individual","Trustmark Dealer"], index=0, key=f"seller_{rc}")

owner_mapping = {"First Owner":0,"Second Owner":1,"Third Owner":2,"Fourth & Above Owner":3}
owner = owner_mapping[owner_label]

st.sidebar.markdown("<hr style='border-color: rgba(128,128,128,0.2); margin: 1rem 0 0.5rem 0;'>", unsafe_allow_html=True)
if st.sidebar.button("🔄 Reset Inputs"):
    st.session_state.reset_counter += 1
    st.rerun()

# ── Hero Section ──────────────────────────────────────────────────────────────
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:64px;height:64px;border-radius:50%;object-fit:cover;box-shadow:0 4px 20px rgba(232,184,75,0.4);" />' if logo_b64 else "🚗"

st.markdown(f"""
<div class="hero-section">
    <div style="display:flex; align-items:center; gap:20px;">
        <div>{logo_html}</div>
        <div>
            <div class="hero-badge">✦ AI-POWERED VALUATION</div>
            <h1 class="hero-title">Ride<span class="hero-accent">Republic</span></h1>
            <p class="hero-sub">Know your car's true market value in seconds — powered by Machine Learning</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
kpis = [
    ("🤖", "82%", "Model Accuracy"),
    ("🚗", "14+", "Car Brands"),
    ("📊", "8K+", "Cars Trained On"),
    ("⚡", "<1s", "Prediction Time"),
]
for col, (icon, val, label) in zip([col1,col2,col3,col4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Brand Logo Display ────────────────────────────────────────────────────────
if brand in brand_logos:
    bcol1, bcol2 = st.columns([1, 5])
    with bcol1:
        st.image(brand_logos[brand], width=100)
    with bcol2:
        st.markdown(f""")
        <div style="padding: 1rem 0;">
            <p style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; margin:0;">
                {brand}
            </p>
            <p style="opacity:0.5; margin:2px 0 0 0; font-size:0.85rem;">
                {year} · {fuel} · {transmission} · {owner_label}
