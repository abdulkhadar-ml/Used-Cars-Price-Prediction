import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import base64
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

st.set_page_config(
    page_title="RideRepublic - Smart Car Pricing",
    page_icon="riderepublic_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Cache model loading for speed ────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_models()

def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

# ── Theme Toggle - NO on_label/off_label to avoid keyboard_double bug ────────
# Custom theme toggle using session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    toggle_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
    if st.sidebar.button(toggle_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

mode = st.session_state.dark_mode

ACCENT = "#E8B84B"
ACCENT2 = "#FF6B6B"

# ── CSS ───────────────────────────────────────────────────────────────────────
if mode:
    BG = "#0D0D14"
    CARD = "#111118"
    BORDER = "#252535"
    TEXT = "#E2E2EE"
    SUBTEXT = "#6666AA"
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG};
        background-image: radial-gradient(ellipse at 15% 0%, rgba(232,184,75,0.07) 0%, transparent 55%);
        color: {TEXT};
        font-family: -apple-system, 'Segoe UI', sans-serif;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {CARD} !important;
        border-right: 1px solid {BORDER} !important;
    }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    div.stButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, #D4A43A 100%) !important;
        color: #0D0D14 !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
        font-size: 0.95rem !important; width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 18px rgba(232,184,75,0.35) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(232,184,75,0.5) !important;
    }}
    [data-testid="stDownloadButton"] button {{
        background: {CARD} !important; color: {ACCENT} !important;
        border: 1.5px solid {ACCENT} !important; border-radius: 10px !important;
        font-weight: 600 !important; width: 100% !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: {ACCENT} !important; color: #0D0D14 !important;
    }}
    .hero-section {{
        background: linear-gradient(135deg, #14142A 0%, #1C1C3A 100%);
        border: 1px solid #2A2A45; border-radius: 20px;
        padding: 2.2rem 2.8rem; margin-bottom: 1.5rem;
        position: relative; overflow: hidden;
    }}
    .hero-section::after {{
        content: ''; position: absolute; top: -40%; right: -5%;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(232,184,75,0.07) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-title {{ font-size: 2.6rem; font-weight: 800; color: #FFFFFF; margin: 0; line-height: 1.15; }}
    .hero-accent {{ color: {ACCENT}; }}
    .hero-sub {{ font-size: 1rem; color: rgba(255,255,255,0.5); margin-top: 0.4rem; }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(232,184,75,0.1); border: 1px solid rgba(232,184,75,0.25);
        color: {ACCENT}; border-radius: 50px; padding: 4px 14px;
        font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;
        margin-bottom: 0.9rem; text-transform: uppercase;
    }}
    .kpi-card {{
        background: {CARD}; border: 1px solid {BORDER};
        border-radius: 14px; padding: 1.3rem 1.4rem; text-align: center;
        transition: border-color 0.2s, transform 0.2s;
    }}
    .kpi-card:hover {{ border-color: {ACCENT}; transform: translateY(-2px); }}
    .kpi-value {{ font-size: 1.6rem; font-weight: 800; color: {ACCENT}; line-height: 1; }}
    .kpi-label {{ font-size: 0.72rem; color: {SUBTEXT}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }}
    .result-card {{
        background: linear-gradient(145deg, #14142A 0%, #1C1C3A 100%);
        border: 1px solid rgba(232,184,75,0.3); border-radius: 16px;
        padding: 1.8rem; text-align: center;
        box-shadow: 0 0 30px rgba(232,184,75,0.08);
    }}
    .result-label {{ font-size: 0.72rem; color: {SUBTEXT}; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 0.6rem; font-weight: 600; }}
    .result-price {{ font-size: 2.6rem; font-weight: 800; color: {ACCENT}; line-height: 1; }}
    .result-sub {{ font-size: 0.82rem; color: {SUBTEXT}; margin-top: 0.4rem; }}
    .result-sub span {{ color: #71ef99; font-weight: 600; }}
    .section-header {{
        font-size: 1.1rem; font-weight: 700; color: #FFFFFF;
        margin: 0 0 1rem 0; display: flex; align-items: center; gap: 8px;
    }}
    .section-header::after {{
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, {BORDER}, transparent);
    }}
    .tip-card {{
        background: {CARD}; border: 1px solid {BORDER};
        border-left: 3px solid {ACCENT}; border-radius: 10px;
        padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;
        font-size: 0.88rem; color: #AAAACC; line-height: 1.5;
    }}
    .tip-card strong {{ color: {ACCENT}; }}
    .about-card {{ background: {CARD}; border: 1px solid {BORDER}; border-radius: 16px; padding: 1.8rem; }}
    .about-tag {{
        display: inline-block; background: rgba(232,184,75,0.08);
        border: 1px solid rgba(232,184,75,0.2); color: {ACCENT};
        border-radius: 6px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600; margin: 3px;
    }}
    .perf-table {{ width: 100%; border-collapse: collapse; }}
    .perf-table th {{
        background: #1E1E32; color: {SUBTEXT}; font-size: 0.72rem;
        text-transform: uppercase; letter-spacing: 1px;
        padding: 10px 16px; text-align: left; border-bottom: 1px solid {BORDER};
    }}
    .perf-table td {{ padding: 12px 16px; border-bottom: 1px solid #1A1A28; font-size: 1rem; font-weight: 700; }}
    .perf-table .val {{ color: {ACCENT}; }}
    .perf-table .name {{ color: #AAAACC; font-weight: 500; font-size: 0.88rem; }}
    .perf-table tr:last-child td {{ border-bottom: none; }}
    .footer-bar {{
        background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
        padding: 1rem 2rem; text-align: center; color: #44445A; font-size: 0.78rem; margin-top: 2rem;
    }}
    [data-testid="stMetricValue"] {{ color: {ACCENT} !important; }}
    [data-testid="stMetricLabel"] {{ color: {SUBTEXT} !important; }}
    /* Sidebar label styling */
    .sidebar-label {{ font-size: 0.65rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: {SUBTEXT}; margin: 0.6rem 0 0.3rem 0; padding: 0 0.5rem; }}
    </style>
    """, unsafe_allow_html=True)
else:
    BG = "#F5F2ED"
    CARD = "#FFFFFF"
    BORDER = "#E8E2D9"
    TEXT = "#1A1A2E"
    SUBTEXT = "#999999"
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG}; color: {TEXT};
        font-family: -apple-system, 'Segoe UI', sans-serif;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {CARD} !important;
        border-right: 1px solid {BORDER} !important;
    }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    /* Sidebar input labels - make visible in light mode */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stNumberInput label {{
        color: #1A1A2E !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}
    div.stButton > button {{
        background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%) !important;
        color: #FFFFFF !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
        font-size: 0.95rem !important; width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(26,26,46,0.2) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(26,26,46,0.3) !important;
    }}
    [data-testid="stDownloadButton"] button {{
        background: {CARD} !important; color: {TEXT} !important;
        border: 1.5px solid {TEXT} !important; border-radius: 10px !important;
        font-weight: 600 !important; width: 100% !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: {TEXT} !important; color: white !important;
    }}
    .hero-section {{
        background: linear-gradient(135deg, #111122 0%, #1A1A3E 100%);
        border-radius: 20px; padding: 2.2rem 2.8rem; margin-bottom: 1.5rem;
        position: relative; overflow: hidden;
    }}
    .hero-section::after {{
        content: ''; position: absolute; top: -40%; right: -5%;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(232,184,75,0.1) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-title {{ font-size: 2.6rem; font-weight: 800; color: #FFFFFF; margin: 0; line-height: 1.15; }}
    .hero-accent {{ color: {ACCENT}; }}
    .hero-sub {{ font-size: 1rem; color: rgba(255,255,255,0.55); margin-top: 0.4rem; }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(232,184,75,0.15); border: 1px solid rgba(232,184,75,0.4);
        color: {ACCENT}; border-radius: 50px; padding: 4px 14px;
        font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;
        margin-bottom: 0.9rem; text-transform: uppercase;
    }}
    .kpi-card {{
        background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
        padding: 1.3rem 1.4rem; text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.2s;
    }}
    .kpi-card:hover {{ border-color: {TEXT}; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }}
    .kpi-value {{ font-size: 1.6rem; font-weight: 800; color: {TEXT}; line-height: 1; }}
    .kpi-label {{ font-size: 0.72rem; color: {SUBTEXT}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }}
    .result-card {{
        background: linear-gradient(145deg, #1A1A2E 0%, #2D2D5E 100%);
        border-radius: 16px; padding: 1.8rem; text-align: center;
        box-shadow: 0 8px 28px rgba(26,26,46,0.2);
    }}
    .result-label {{ font-size: 0.72rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 0.6rem; font-weight: 600; }}
    .result-price {{ font-size: 2.6rem; font-weight: 800; color: {ACCENT}; line-height: 1; }}
    .result-sub {{ font-size: 0.82rem; color: rgba(255,255,255,0.4); margin-top: 0.4rem; }}
    .result-sub span {{ color: #71ef99; font-weight: 600; }}
    .section-header {{
        font-size: 1.1rem; font-weight: 700; color: {TEXT};
        margin: 0 0 1rem 0; display: flex; align-items: center; gap: 8px;
    }}
    .section-header::after {{
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, {BORDER}, transparent);
    }}
    .tip-card {{
        background: {CARD}; border: 1px solid {BORDER};
        border-left: 3px solid {TEXT}; border-radius: 10px;
        padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;
        font-size: 0.88rem; color: #555; line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .tip-card strong {{ color: {TEXT}; }}
    .about-card {{
        background: {CARD}; border: 1px solid {BORDER};
        border-radius: 16px; padding: 1.8rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    .about-tag {{
        display: inline-block; background: #F0EDE8; border: 1px solid {BORDER};
        color: {TEXT}; border-radius: 6px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600; margin: 3px;
    }}
    .perf-table {{ width: 100%; border-collapse: collapse; }}
    .perf-table th {{
        background: {BG}; color: {SUBTEXT}; font-size: 0.72rem;
        text-transform: uppercase; letter-spacing: 1px;
        padding: 10px 16px; text-align: left; border-bottom: 1px solid {BORDER};
    }}
    .perf-table td {{ padding: 12px 16px; border-bottom: 1px solid #F0EDE8; font-size: 1rem; font-weight: 700; }}
    .perf-table .val {{ color: {TEXT}; }}
    .perf-table .name {{ color: #555; font-weight: 500; font-size: 0.88rem; }}
    .perf-table tr:last-child td {{ border-bottom: none; }}
    .footer-bar {{
        background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
        padding: 1rem 2rem; text-align: center; color: #BBB; font-size: 0.78rem; margin-top: 2rem;
    }}
    [data-testid="stMetricValue"] {{ color: {TEXT} !important; }}
    [data-testid="stMetricLabel"] {{ color: {SUBTEXT} !important; }}
    </style>
    """, unsafe_allow_html=True)

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
    sidebar_name_color = "#E8B84B" if mode else "#1A1A2E"
    st.sidebar.markdown(
        f"""<div style="text-align:center;padding:0.8rem 0 0.3rem 0;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:60px;height:60px;border-radius:50%;object-fit:cover;
                        box-shadow:0 4px 14px rgba(232,184,75,0.25);" />
            <p style="margin:6px 0 0 0;font-weight:800;font-size:0.9rem;color:{sidebar_name_color};">
                RideRepublic
            </p>
        </div>""",
        unsafe_allow_html=True
    )

hr_color = "#252535" if mode else "#E8E2D9"
label_color = "#6666AA" if mode else "#999999"
st.sidebar.markdown(f"<hr style='border:none;border-top:1px solid {hr_color};margin:0.4rem 0;'>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='font-size:0.65rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:{label_color};margin:0.6rem 0 0.3rem 0;padding:0 0.3rem;'>Car Details</p>", unsafe_allow_html=True)

brands = [
    "Nissan","Audi","Chevrolet","Ford","Honda","Hyundai",
    "Mahindra","Maruti","Mercedes-Benz","BMW",
    "Renault","Skoda","Tata","Toyota","Other"
]

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0
rc = st.session_state.reset_counter

brand        = st.sidebar.selectbox("Brand", brands, index=0, key=f"brand_{rc}")
year         = st.sidebar.number_input("Year", 2000, 2026, 2018, key=f"year_{rc}")
km_driven    = st.sidebar.number_input("KM Driven", 0, 300000, 40000, key=f"km_{rc}")
mileage      = st.sidebar.number_input("Mileage (km/l)", 5.0, 40.0, 18.0, key=f"mileage_{rc}")
engine       = st.sidebar.number_input("Engine (CC)", 800, 5000, 1500, key=f"engine_{rc}")
seats        = st.sidebar.number_input("Seats", 2, 10, 5, key=f"seats_{rc}")
owner_label  = st.sidebar.selectbox(
    "Owner Type",
    ["First Owner","Second Owner","Third Owner","Fourth & Above Owner"],
    index=0, key=f"owner_{rc}"
)
owner_mapping = {"First Owner":0,"Second Owner":1,"Third Owner":2,"Fourth & Above Owner":3}
owner = owner_mapping[owner_label]
fuel         = st.sidebar.selectbox("Fuel", ["Diesel","Petrol","LPG"], index=0, key=f"fuel_{rc}")
transmission = st.sidebar.selectbox("Transmission", ["Manual","Automatic"], index=0, key=f"transmission_{rc}")
seller_type  = st.sidebar.selectbox("Seller Type", ["Individual","Trustmark Dealer"], index=0, key=f"seller_{rc}")

st.sidebar.markdown(f"<hr style='border:none;border-top:1px solid {hr_color};margin:0.8rem 0 0.5rem 0;'>", unsafe_allow_html=True)
if st.sidebar.button("Reset Inputs"):
    st.session_state.reset_counter += 1
    st.rerun()

# ── Hero Section ──────────────────────────────────────────────────────────────
logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;" />' if logo_b64 else ""

st.markdown(f"""
<div class="hero-section">
    <div style="display:flex;align-items:center;gap:18px;">
        <div>{logo_img}</div>
        <div>
            <div class="hero-badge">AI-POWERED VALUATION</div>
            <h1 class="hero-title"><span style="color:#FFFFFF;">Ride</span><span class="hero-accent">Republic</span></h1>
            <p class="hero-sub">Know your car's true market value in seconds, powered by Machine Learning</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards - removed Prediction Time ──────────────────────────────────────
col1, col2, col3 = st.columns(3)
kpis = [
    ("82%", "Model Accuracy"),
    ("14+", "Car Brands"),
    ("8,000+", "Cars Trained On"),
]
for col, (val, label) in zip([col1, col2, col3], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Brand Display ─────────────────────────────────────────────────────────────
if brand in brand_logos:
    bcol1, bcol2 = st.columns([1, 5])
    with bcol1:
        st.image(brand_logos[brand], width=90)
    with bcol2:
        brand_info = str(year) + "  |  " + fuel + "  |  " + transmission + "  |  " + owner_label
        name_c = "#FFFFFF" if mode else "#1A1A2E"
        spec_c = "#6666AA" if mode else "#999999"
        st.markdown(f"""
        <div style="padding:0.8rem 0;">
            <p style="font-size:1.3rem;font-weight:700;color:{name_c};margin:0;">{brand}</p>
            <p style="font-size:0.82rem;color:{spec_c};margin:3px 0 0 0;">{brand_info}</p>
        </div>""", unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
st.write("**Valuation Engine**")
pcol, _ = st.columns([1, 2])
with pcol:
    predict_btn = st.button("Predict Resale Price", use_container_width=True)

if predict_btn:
    with st.spinner("Analyzing market data..."):
        input_df = pd.DataFrame(columns=model.feature_names_in_)
        input_df.loc[0] = 0
        input_df.at[0,'year'] = year
        input_df.at[0,'km_driven'] = km_driven
        input_df.at[0,'mileage(km/ltr/kg)'] = mileage
        input_df.at[0,'engine'] = engine
        input_df.at[0,'seats'] = seats
        input_df.at[0,'owner'] = owner
        for col_name, val in [
            (f"brand_{brand}", 1), (f"fuel_{fuel}", 1),
            (f"transmission_{transmission}", 1), (f"seller_type_{seller_type}", 1)
        ]:
            if col_name in input_df.columns:
                input_df.at[0, col_name] = val
        numeric_cols = ['year','km_driven','mileage(km/ltr/kg)','engine','seats']
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])
        y_log  = model.predict(input_df)
        price  = round(np.exp(y_log)[0], 0)
        low    = round(price * 0.9)
        high   = round(price * 1.1)
        price_lakh = price / 100000
        low_lakh   = low / 100000
        high_lakh  = high / 100000
        age        = 2026 - year
        dep_pct    = round((1 - (0.9**5)) * 100, 1)
        dep_years  = [year + i for i in range(6)]
        dep_prices = [price * (0.9 ** i) for i in range(6)]
        dep_df     = pd.DataFrame({"Year": dep_years, "Estimated Value": dep_prices})

        st.markdown("<br>", unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Estimated Resale Value</div>
                <div class="result-price">Rs.{price_lakh:.2f}L</div>
                <div class="result-sub">~ Rs. {int(price):,}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Price Range</div>
                <div class="result-price" style="font-size:1.8rem;">Rs.{low_lakh:.1f}L - Rs.{high_lakh:.1f}L</div>
                <div class="result-sub">Conservative - <span>Optimistic</span></div>
            </div>""", unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">5-Year Depreciation</div>
                <div class="result-price" style="color:#FF6B6B;font-size:2.2rem;">-{dep_pct}%</div>
                <div class="result-sub">Car Age: <span>{age} yrs</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        g1, g2 = st.columns([1, 2])
        with g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=price_lakh,
                number={'prefix': "Rs.", 'suffix': " L", 'valueformat': '.2f',
                        'font': {'size': 24, 'color': ACCENT}},
                title={'text': "Market Value (Lakhs)", 'font': {'size': 12, 'color': '#888'}},
                gauge={
                    'axis': {'range': [0, 50], 'tickcolor': '#444'},
                    'bar': {'color': ACCENT, 'thickness': 0.22},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'bordercolor': 'rgba(0,0,0,0)',
                    'steps': [
                        {'range': [0, 15], 'color': 'rgba(255,107,107,0.1)'},
                        {'range': [15, 30], 'color': 'rgba(232,184,75,0.07)'},
                        {'range': [30, 50], 'color': 'rgba(113,239,153,0.07)'},
                    ],
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=240, margin=dict(t=30, b=0, l=20, r=20),
                font={'color': '#888'}
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with g2:
            st.write("**Depreciation Forecast**")
            fig_dep = go.Figure()
            fig_dep.add_trace(go.Bar(
                y=[str(y) for y in dep_df["Year"]],
                x=dep_df["Estimated Value"] / 100000,
                orientation='h',
                marker=dict(
                    color=dep_df["Estimated Value"] / 100000,
                    colorscale=[[0,'#FF6B6B'],[0.5,ACCENT],[1,'#71ef99']],
                    showscale=False
                ),
                hovertemplate="Year: %{y}<br>Value: Rs.%{x:.2f}L<extra></extra>"
            ))
            fig_dep.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=240, margin=dict(t=10, b=10, l=10, r=20),
                xaxis=dict(title="Rs. Lakhs", color='#888', gridcolor='rgba(128,128,128,0.1)'),
                yaxis=dict(color='#888', gridcolor='rgba(0,0,0,0)'),
                font={'color': '#888'}
            )
            st.plotly_chart(fig_dep, use_container_width=True)

        # ── PDF Download ──────────────────────────────────────────────────────
        st.markdown("### Valuation Report")

        def generate_pdf(brand, year, km_driven, mileage, engine, seats,
                         owner_label, fuel, transmission, seller_type,
                         price, low, high, dep_df):
            pdf = FPDF()
            pdf.set_margins(10, 10, 10)
            pdf.add_page()
            W = 190
            pdf.set_fill_color(15, 15, 15)
            pdf.rect(0, 0, 210, 30, 'F')
            if os.path.exists("riderepublic_logo.png"):
                pdf.image("riderepublic_logo.png", x=8, y=4, w=22)
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(255, 255, 255)
            pdf.set_xy(34, 8)
            pdf.cell(100, 8, "RideRepublic")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_xy(34, 17)
            pdf.cell(100, 5, "Smart Car Pricing  |  AI-Powered Valuation")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_xy(140, 11)
            pdf.cell(60, 5, f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}", align="R")
            pdf.set_xy(10, 35)
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(W, 8, "Car Resale Valuation Report", align="C")
            pdf.ln(10)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            def section_header(title):
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_fill_color(220, 220, 220)
                pdf.set_text_color(30, 30, 30)
                pdf.cell(W, 7, f"  {title}", fill=True)
                pdf.ln(8)
            section_header("Car Details")
            details = [
                ("Brand", brand), ("Year", str(year)),
                ("KM Driven", f"{km_driven:,} km"), ("Mileage", f"{mileage} km/l"),
                ("Engine", f"{engine} CC"), ("Seats", str(seats)),
                ("Owner Type", owner_label), ("Fuel", fuel),
                ("Transmission", transmission), ("Seller Type", seller_type),
            ]
            pdf.set_font("Helvetica", "", 9)
            for i, (label, value) in enumerate(details):
                pdf.set_fill_color(248, 248, 248) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
                pdf.set_text_color(30, 30, 30)
                pdf.cell(95, 6, f"  {label}", fill=True)
                pdf.cell(95, 6, f"  {value}", fill=True)
                pdf.ln(6)
            pdf.ln(2)
            section_header("Prediction Result")
            pdf.set_fill_color(20, 20, 20)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(W, 11, f"  Estimated Resale Price:  Rs. {price/100000:.2f} Lakhs  ({int(price):,})", fill=True)
            pdf.ln(13)
            pdf.set_fill_color(220, 245, 220)
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(W, 7, f"  Expected Price Range:  Rs. {low/100000:.2f} L  -  Rs. {high/100000:.2f} L", fill=True)
            pdf.ln(9)
            section_header("Projected Depreciation (6 Years)")
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(20, 20, 20)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(95, 7, "  Year", fill=True)
            pdf.cell(95, 7, "  Estimated Value", fill=True)
            pdf.ln(7)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            for i, row in dep_df.iterrows():
                pdf.set_fill_color(248, 248, 248) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
                pdf.cell(95, 6, f"  {int(row['Year'])}", fill=True)
                pdf.cell(95, 6, f"  Rs. {row['Estimated Value']/100000:.2f} Lakhs", fill=True)
                pdf.ln(6)
            pdf.ln(2)
            section_header("Tips To Maintain Good Resale Value")
            tips = [
                "Regular Servicing: Maintain proper service records to build buyer trust.",
                "Low Mileage: Cars with lower mileage usually sell at higher prices.",
                "Clean Interior & Exterior: A well-maintained car attracts better resale offers.",
                "Accident-Free Record: Vehicles without accident history maintain higher value.",
                "Original Parts: Avoid replacing parts with non-genuine components.",
            ]
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(30, 30, 30)
            for tip in tips:
                pdf.set_x(10)
                pdf.multi_cell(W, 5, f"  * {tip}")
                pdf.set_x(10)
            pdf.set_y(-18)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(120, 120, 120)
            pdf.cell(W, 8, "RideRepublic 2026  |  AI-Powered Car Valuation  |  For reference purposes only.", align="C")
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(tmp.name)
            return tmp.name

        pdf_path = generate_pdf(brand, year, km_driven, mileage, engine, seats,
                                owner_label, fuel, transmission, seller_type,
                                price, low, high, dep_df)
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"RideRepublic_{brand}_{year}_Report.pdf",
            mime="application/pdf",
        )
        os.unlink(pdf_path)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tips ──────────────────────────────────────────────────────────────────────
st.write("**Tips To Maintain Resale Value**")
tips_data = [
    ("Regular Servicing", "Maintain proper service records to build buyer trust."),
    ("Low Mileage", "Cars with lower mileage usually sell at higher prices."),
    ("Clean Interior & Exterior", "A well-maintained car attracts better resale offers."),
    ("Accident-Free Record", "Vehicles without accident history maintain higher value."),
    ("Original Parts", "Avoid replacing parts with non-genuine components."),
]
tc1, tc2 = st.columns(2)
for i, (title, desc) in enumerate(tips_data):
    col = tc1 if i % 2 == 0 else tc2
    with col:
        st.markdown(f"""
        <div class="tip-card"><strong>{title}:</strong> {desc}</div>""",
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── About ─────────────────────────────────────────────────────────────────────
st.write("**About RideRepublic**")
ac1, ac2 = st.columns([3, 2])
with ac1:
    txt_opacity = "0.75"
    st.markdown(f"""
    <div class="about-card">
        <p style="line-height:1.8;opacity:{txt_opacity};margin:0 0 1rem 0;font-size:0.92rem;">
            RideRepublic is an AI-powered car valuation platform that estimates the resale price
            of used cars based on key vehicle attributes. Built as a final year ML project, it
            demonstrates end-to-end machine learning from data preprocessing to live deployment.
        </p>
        <p style="font-weight:700;margin:0 0 0.6rem 0;opacity:0.5;font-size:0.7rem;text-transform:uppercase;letter-spacing:1.2px;">Model Inputs</p>
        <div>
            <span class="about-tag">Year</span>
            <span class="about-tag">KM Driven</span>
            <span class="about-tag">Mileage</span>
            <span class="about-tag">Engine CC</span>
            <span class="about-tag">Fuel Type</span>
            <span class="about-tag">Transmission</span>
            <span class="about-tag">Brand</span>
            <span class="about-tag">Ownership</span>
        </div>
    </div>""", unsafe_allow_html=True)

with ac2:
    val_c  = "#E8B84B" if mode else "#1A1A2E"
    name_c = "#AAAACC" if mode else "#555555"
    st.markdown(f"""
    <div class="about-card">
        <p style="font-weight:700;margin:0 0 1rem 0;font-size:0.95rem;">Model Performance</p>
        <table class="perf-table">
            <thead><tr><th>Metric</th><th>Value</th></tr></thead>
            <tbody>
                <tr><td class="name">Train R2 Score</td><td class="val">0.83</td></tr>
                <tr><td class="name">Test R2 Score</td><td class="val">0.82</td></tr>
                <tr><td class="name">MAE</td><td class="val">Rs. 77,695</td></tr>
                <tr><td class="name">RMSE</td><td class="val">Rs. 1,06,605</td></tr>
            </tbody>
        </table>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

cta_col, _ = st.columns([1, 2])
with cta_col:
    if st.button("Open Analytics Dashboard"):
        st.switch_page("pages/analytics.py")

st.markdown("""
<div class="footer-bar">
    RideRepublic 2026 &nbsp;&nbsp; Python &nbsp;&nbsp; Scikit-Learn &nbsp;&nbsp; Streamlit &nbsp;&nbsp; Plotly &nbsp;&nbsp; FPDF2
</div>
""", unsafe_allow_html=True)
