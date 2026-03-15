import streamlit as st
import base64

st.set_page_config(
    page_title="RideRepublic - Smart Car Pricing",
    page_icon="riderepublic_logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

# ── Theme Toggle ──────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    toggle_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
    if st.sidebar.button(toggle_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

mode = st.session_state.dark_mode
ACCENT = "#E8B84B"

dark_css = """
<style>
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
.stApp {
    background-color: #0D0D14;
    color: #E2E2EE;
    font-family: -apple-system, 'Segoe UI', sans-serif;
}
section[data-testid="stSidebar"] {
    background-color: #111118 !important;
    border-right: 1px solid #252535 !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #E8B84B 0%, #D4A43A 100%) !important;
    color: #0D0D14 !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 1.15rem !important; width: 100% !important;
    padding: 1rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(232,184,75,0.35) !important;
    letter-spacing: 0.3px !important;
}
div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 28px rgba(232,184,75,0.55) !important;
}
.hero-wrap {
    background: linear-gradient(135deg, #111122 0%, #1A1A3A 100%);
    border-radius: 24px; margin-bottom: 3rem;
    border: 1px solid #2A2A45; position: relative; overflow: hidden;
    min-height: 320px;
}
.hero-left {
    padding: clamp(2rem, 5vw, 3.5rem);
    display: flex; flex-direction: column; justify-content: center;
}
.hero-right {
    display: flex; align-items: center; justify-content: center;
    padding: 2rem;
}
.hero-inner {
    display: grid; grid-template-columns: 1fr 1fr;
    align-items: center; min-height: 320px;
}
@media (max-width: 768px) {
    .hero-inner { grid-template-columns: 1fr; }
    .hero-right { display: none; }
}
.hero-badge {
    display: inline-flex; align-items: center;
    background: rgba(232,184,75,0.1); border: 1px solid rgba(232,184,75,0.25);
    color: #E8B84B; border-radius: 50px; padding: 6px 18px;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 1.5px;
    margin-bottom: 1.2rem; text-transform: uppercase; width: fit-content;
}
.hero-title {
    font-size: clamp(1.8rem, 4vw, 3.2rem); font-weight: 800;
    color: #FFFFFF; margin: 0 0 1rem 0; line-height: 1.15; letter-spacing: -0.5px;
}
.hero-title span { color: #E8B84B; }
.hero-sub {
    font-size: clamp(0.9rem, 2vw, 1.05rem); color: rgba(255,255,255,0.55);
    line-height: 1.7; margin-bottom: 0; max-width: 480px;
}
.car-img {
    width: 100%; max-width: 420px; filter: drop-shadow(0 20px 40px rgba(232,184,75,0.2));
}
.features-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem; margin-bottom: 3rem;
}
.feature-card {
    background: #111118; border: 1px solid #252535;
    border-radius: 16px; padding: 1.8rem 1.5rem; text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.feature-card:hover { border-color: #E8B84B; transform: translateY(-4px); }
.feature-icon { font-size: 2.2rem; margin-bottom: 1rem; }
.feature-title { font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: #6666AA; line-height: 1.5; }
.steps-wrap {
    background: #111118; border: 1px solid #252535;
    border-radius: 20px; padding: 2.5rem; margin-bottom: 3rem;
}
.steps-title { font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin-bottom: 2rem; text-align: center; }
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem; }
.step-item { text-align: center; }
.step-num {
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #E8B84B, #D4A43A);
    color: #0D0D14; font-weight: 800; font-size: 1.2rem;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem auto;
}
.step-title { font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem; }
.step-desc { font-size: 0.82rem; color: #6666AA; }
.stats-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1rem; margin-bottom: 3rem;
}
.stat-card {
    background: #111118; border: 1px solid #252535;
    border-radius: 14px; padding: 1.5rem; text-align: center;
}
.stat-value { font-size: 2rem; font-weight: 800; color: #E8B84B; line-height: 1; }
.stat-label { font-size: 0.75rem; color: #6666AA; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px; }
.footer-bar {
    background: #111118; border: 1px solid #252535; border-radius: 12px;
    padding: 1rem 2rem; text-align: center; color: #44445A;
    font-size: 0.78rem; margin-top: 2rem;
}
</style>
"""

light_css = """
<style>
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
.stApp {
    background-color: #F5F2ED; color: #1A1A2E;
    font-family: -apple-system, 'Segoe UI', sans-serif;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E8E2D9 !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%) !important;
    color: #FFFFFF !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 1.15rem !important; width: 100% !important;
    padding: 1rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(26,26,46,0.2) !important;
    letter-spacing: 0.3px !important;
}
div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 28px rgba(26,26,46,0.35) !important;
}
.hero-wrap {
    background: linear-gradient(135deg, #111122 0%, #1A1A3A 100%);
    border-radius: 24px; margin-bottom: 3rem;
    position: relative; overflow: hidden; min-height: 320px;
}
.hero-left {
    padding: clamp(2rem, 5vw, 3.5rem);
    display: flex; flex-direction: column; justify-content: center;
}
.hero-right {
    display: flex; align-items: center; justify-content: center; padding: 2rem;
}
.hero-inner {
    display: grid; grid-template-columns: 1fr 1fr; align-items: center; min-height: 320px;
}
@media (max-width: 768px) {
    .hero-inner { grid-template-columns: 1fr; }
    .hero-right { display: none; }
}
.hero-badge {
    display: inline-flex; align-items: center;
    background: rgba(232,184,75,0.15); border: 1px solid rgba(232,184,75,0.4);
    color: #E8B84B; border-radius: 50px; padding: 6px 18px;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 1.5px;
    margin-bottom: 1.2rem; text-transform: uppercase; width: fit-content;
}
.hero-title {
    font-size: clamp(1.8rem, 4vw, 3.2rem); font-weight: 800;
    color: #FFFFFF; margin: 0 0 1rem 0; line-height: 1.15; letter-spacing: -0.5px;
}
.hero-title span { color: #E8B84B; }
.hero-sub {
    font-size: clamp(0.9rem, 2vw, 1.05rem); color: rgba(255,255,255,0.6);
    line-height: 1.7; margin-bottom: 0; max-width: 480px;
}
.car-img { width: 100%; max-width: 420px; filter: drop-shadow(0 20px 40px rgba(26,26,46,0.3)); }
.features-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem; margin-bottom: 3rem;
}
.feature-card {
    background: #FFFFFF; border: 1px solid #E8E2D9;
    border-radius: 16px; padding: 1.8rem 1.5rem; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: border-color 0.2s, transform 0.2s;
}
.feature-card:hover { border-color: #1A1A2E; transform: translateY(-4px); }
.feature-icon { font-size: 2.2rem; margin-bottom: 1rem; }
.feature-title { font-size: 1rem; font-weight: 700; color: #1A1A2E; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: #999; line-height: 1.5; }
.steps-wrap {
    background: #FFFFFF; border: 1px solid #E8E2D9;
    border-radius: 20px; padding: 2.5rem; margin-bottom: 3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.steps-title { font-size: 1.5rem; font-weight: 800; color: #1A1A2E; margin-bottom: 2rem; text-align: center; }
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem; }
.step-item { text-align: center; }
.step-num {
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #1A1A2E, #2D2D5E);
    color: #FFFFFF; font-weight: 800; font-size: 1.2rem;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem auto;
}
.step-title { font-size: 0.95rem; font-weight: 700; color: #1A1A2E; margin-bottom: 0.4rem; }
.step-desc { font-size: 0.82rem; color: #999; }
.stats-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1rem; margin-bottom: 3rem;
}
.stat-card {
    background: #FFFFFF; border: 1px solid #E8E2D9;
    border-radius: 14px; padding: 1.5rem; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.stat-value { font-size: 2rem; font-weight: 800; color: #1A1A2E; line-height: 1; }
.stat-label { font-size: 0.75rem; color: #999; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 6px; }
.footer-bar {
    background: #FFFFFF; border: 1px solid #E8E2D9; border-radius: 12px;
    padding: 1rem 2rem; text-align: center; color: #BBB;
    font-size: 0.78rem; margin-top: 2rem;
}
</style>
"""

st.markdown(dark_css if mode else light_css, unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
logo_img = ""
if logo_b64:
    logo_img = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'style="width:70px;height:70px;border-radius:50%;object-fit:cover;'
        f'box-shadow:0 4px 20px rgba(232,184,75,0.35);margin-bottom:1.2rem;" />'
    )

# Car SVG illustration
car_svg = """
<svg viewBox="0 0 500 280" xmlns="http://www.w3.org/2000/svg" class="car-img">
  <defs>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E8B84B;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#D4A43A;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="roofGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F0C96A;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C89030;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="rgba(232,184,75,0.4)"/>
    </filter>
  </defs>
  <!-- Shadow -->
  <ellipse cx="250" cy="245" rx="180" ry="18" fill="rgba(0,0,0,0.3)"/>
  <!-- Car Body -->
  <rect x="50" y="155" width="400" height="75" rx="18" fill="url(#bodyGrad)" filter="url(#shadow)"/>
  <!-- Car Roof -->
  <path d="M 130 155 Q 145 90 195 80 L 315 80 Q 365 90 375 155 Z" fill="url(#roofGrad)"/>
  <!-- Windshield Front -->
  <path d="M 310 155 Q 355 100 360 85 L 315 80 Q 280 80 270 155 Z" fill="rgba(150,220,255,0.6)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <!-- Windshield Back -->
  <path d="M 145 155 Q 148 100 145 85 L 195 80 Q 220 80 230 155 Z" fill="rgba(150,220,255,0.6)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <!-- Windows -->
  <path d="M 235 155 L 268 83 L 313 83 L 310 155 Z" fill="rgba(150,220,255,0.5)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
  <!-- Door Lines -->
  <line x1="270" y1="155" x2="268" y2="100" stroke="rgba(180,120,10,0.5)" stroke-width="2"/>
  <!-- Front bumper -->
  <rect x="40" y="185" width="40" height="30" rx="8" fill="#C89030"/>
  <!-- Rear bumper -->
  <rect x="420" y="185" width="40" height="30" rx="8" fill="#C89030"/>
  <!-- Headlight front -->
  <ellipse cx="68" cy="185" rx="15" ry="10" fill="rgba(255,240,150,0.9)" stroke="#B8860B" stroke-width="1"/>
  <!-- Headlight rear -->
  <ellipse cx="432" cy="185" rx="15" ry="10" fill="rgba(255,100,100,0.9)" stroke="#8B0000" stroke-width="1"/>
  <!-- Front Wheel -->
  <circle cx="145" cy="228" r="38" fill="#1A1A2E" stroke="#E8B84B" stroke-width="4"/>
  <circle cx="145" cy="228" r="22" fill="#252535" stroke="#E8B84B" stroke-width="2"/>
  <circle cx="145" cy="228" r="8" fill="#E8B84B"/>
  <!-- Rear Wheel -->
  <circle cx="355" cy="228" r="38" fill="#1A1A2E" stroke="#E8B84B" stroke-width="4"/>
  <circle cx="355" cy="228" r="22" fill="#252535" stroke="#E8B84B" stroke-width="2"/>
  <circle cx="355" cy="228" r="8" fill="#E8B84B"/>
  <!-- Shine -->
  <path d="M 160 100 Q 220 88 290 92" stroke="rgba(255,255,255,0.4)" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
"""

st.markdown(
    f'<div class="hero-wrap">'
    f'<div class="hero-inner">'
    f'<div class="hero-left">'
    f'{logo_img}'
    f'<div class="hero-badge">AI-POWERED CAR VALUATION</div>'
    f'<h1 class="hero-title">Know Your Car\'s<br><span>True Value</span> Instantly</h1>'
    f'<p class="hero-sub">Predict your used car\'s resale price instantly using Machine Learning. Accurate, fast and completely free.</p>'
    f'</div>'
    f'<div class="hero-right">{car_svg}</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Get Started Button ────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([1, 3, 1])
with btn_col:
    if st.button("🚗  Get Started - Predict Now  →", use_container_width=True):
        st.switch_page("pages/app.py")

st.write("")

# ── Features Section ──────────────────────────────────────────────────────────
feat_title_color = "#FFFFFF" if mode else "#1A1A2E"
st.markdown(
    f'<h2 style="text-align:center;font-size:1.8rem;font-weight:800;'
    f'color:{feat_title_color};margin-bottom:1.5rem;">Why RideRepublic?</h2>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="features-grid">'
    '<div class="feature-card"><div class="feature-icon">🤖</div>'
    '<div class="feature-title">AI Powered Prediction</div>'
    '<div class="feature-desc">ML model trained on 8,000+ real car listings for accurate price prediction</div></div>'
    '<div class="feature-card"><div class="feature-icon">⚡</div>'
    '<div class="feature-title">Instant Results</div>'
    '<div class="feature-desc">Get your car valuation in under a second, no waiting, no signup required</div></div>'
    '<div class="feature-card"><div class="feature-icon">📄</div>'
    '<div class="feature-title">PDF Report</div>'
    '<div class="feature-desc">Download a complete valuation report with depreciation forecast and tips</div></div>'
    '<div class="feature-card"><div class="feature-icon">📊</div>'
    '<div class="feature-title">Analytics Dashboard</div>'
    '<div class="feature-desc">Explore dataset insights, price trends and model performance metrics</div></div>'
    '</div>',
    unsafe_allow_html=True
)

# ── How It Works ──────────────────────────────────────────────────────────────
steps_title_color = "#FFFFFF" if mode else "#1A1A2E"
st.markdown(
    '<div class="steps-wrap">'
    f'<div class="steps-title" style="color:{steps_title_color};">How It Works</div>'
    '<div class="steps-grid">'
    f'<div class="step-item"><div class="step-num">1</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Enter Car Details</div>'
    '<div class="step-desc">Fill in brand, year, fuel type, KM driven and other details</div></div>'
    f'<div class="step-item"><div class="step-num">2</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Click Predict</div>'
    '<div class="step-desc">Our AI model analyzes your inputs instantly</div></div>'
    f'<div class="step-item"><div class="step-num">3</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Get Your Price</div>'
    '<div class="step-desc">View estimated price, range and depreciation chart</div></div>'
    f'<div class="step-item"><div class="step-num">4</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Download Report</div>'
    '<div class="step-desc">Save your full valuation report as PDF</div></div>'
    '</div></div>',
    unsafe_allow_html=True
)

# ── Stats - only 3 cards ──────────────────────────────────────────────────────
stat_val_color = "#E8B84B" if mode else "#1A1A2E"
stat_lbl_color = "#6666AA" if mode else "#999999"
st.markdown(
    '<div class="stats-grid">'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">82%</div><div class="stat-label" style="color:{stat_lbl_color};">Model Accuracy</div></div>'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">14+</div><div class="stat-label" style="color:{stat_lbl_color};">Car Brands</div></div>'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">8K+</div><div class="stat-label" style="color:{stat_lbl_color};">Cars Trained On</div></div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-bar">'
    'RideRepublic &copy; 2026 &nbsp;&nbsp; Python &nbsp;&nbsp; Scikit-Learn &nbsp;&nbsp; Streamlit &nbsp;&nbsp; Plotly'
    '</div>',
    unsafe_allow_html=True
)
