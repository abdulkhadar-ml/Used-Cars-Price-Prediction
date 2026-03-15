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

if mode:
    BG = "#0D0D14"; CARD = "#111118"; BORDER = "#252535"
    TEXT = "#E2E2EE"; SUBTEXT = "#6666AA"
else:
    BG = "#F5F2ED"; CARD = "#FFFFFF"; BORDER = "#E8E2D9"
    TEXT = "#1A1A2E"; SUBTEXT = "#999999"

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
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.95rem !important; width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(232,184,75,0.35) !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(232,184,75,0.5) !important;
}
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0; margin-bottom: 2rem;
    border-bottom: 1px solid #252535;
}
.nav-logo { display: flex; align-items: center; gap: 12px; }
.nav-name { font-size: 1.3rem; font-weight: 800; color: #FFFFFF; }
.nav-name span { color: #E8B84B; }
.hero-wrap {
    text-align: center; padding: 4rem 2rem;
    background: linear-gradient(135deg, #111122 0%, #1A1A3A 100%);
    border-radius: 24px; margin-bottom: 3rem;
    border: 1px solid #2A2A45; position: relative; overflow: hidden;
}
.hero-wrap::before {
    content: ''; position: absolute; top: -50%; left: 50%; transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(232,184,75,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center;
    background: rgba(232,184,75,0.1); border: 1px solid rgba(232,184,75,0.25);
    color: #E8B84B; border-radius: 50px; padding: 6px 18px;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 1.5px;
    margin-bottom: 1.5rem; text-transform: uppercase;
}
.hero-title {
    font-size: clamp(2rem, 6vw, 3.8rem); font-weight: 800;
    color: #FFFFFF; margin: 0 0 1rem 0; line-height: 1.1; letter-spacing: -1px;
}
.hero-title span { color: #E8B84B; }
.hero-sub {
    font-size: clamp(0.95rem, 3vw, 1.2rem); color: rgba(255,255,255,0.5);
    max-width: 550px; margin: 0 auto 2.5rem auto; line-height: 1.6;
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
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.95rem !important; width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(26,26,46,0.2) !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(26,26,46,0.3) !important;
}
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0; margin-bottom: 2rem;
    border-bottom: 1px solid #E8E2D9;
}
.nav-logo { display: flex; align-items: center; gap: 12px; }
.nav-name { font-size: 1.3rem; font-weight: 800; color: #1A1A2E; }
.nav-name span { color: #E8B84B; }
.hero-wrap {
    text-align: center; padding: 4rem 2rem;
    background: linear-gradient(135deg, #111122 0%, #1A1A3A 100%);
    border-radius: 24px; margin-bottom: 3rem;
    position: relative; overflow: hidden;
}
.hero-wrap::before {
    content: ''; position: absolute; top: -50%; left: 50%; transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(232,184,75,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center;
    background: rgba(232,184,75,0.15); border: 1px solid rgba(232,184,75,0.4);
    color: #E8B84B; border-radius: 50px; padding: 6px 18px;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 1.5px;
    margin-bottom: 1.5rem; text-transform: uppercase;
}
.hero-title {
    font-size: clamp(2rem, 6vw, 3.8rem); font-weight: 800;
    color: #FFFFFF; margin: 0 0 1rem 0; line-height: 1.1; letter-spacing: -1px;
}
.hero-title span { color: #E8B84B; }
.hero-sub {
    font-size: clamp(0.95rem, 3vw, 1.2rem); color: rgba(255,255,255,0.6);
    max-width: 550px; margin: 0 auto 2.5rem auto; line-height: 1.6;
}
.features-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem; margin-bottom: 3rem;
}
.feature-card {
    background: #FFFFFF; border: 1px solid #E8E2D9;
    border-radius: 16px; padding: 1.8rem 1.5rem; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: border-color 0.2s, transform 0.2s;
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
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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

# ── Navbar ────────────────────────────────────────────────────────────────────
logo_img = ""
if logo_b64:
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />'

name_color = "#FFFFFF" if mode else "#1A1A2E"
st.markdown(
    f'<div class="nav-bar">'
    f'<div class="nav-logo">'
    f'{logo_img}'
    f'<span class="nav-name">Ride<span>Republic</span></span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Hero Section ──────────────────────────────────────────────────────────────
hero_logo = ""
if logo_b64:
    hero_logo = f'<img src="data:image/png;base64,{logo_b64}" style="width:90px;height:90px;border-radius:50%;object-fit:cover;box-shadow:0 8px 30px rgba(232,184,75,0.3);margin-bottom:1.5rem;" />'

st.markdown(
    f'<div class="hero-wrap">'
    f'{hero_logo}'
    f'<div class="hero-badge">AI-POWERED CAR VALUATION</div>'
    f'<h1 class="hero-title">Know Your Car\'s <span>True Value</span><br>Instantly</h1>'
    f'<p class="hero-sub">RideRepublic uses Machine Learning to predict the resale price of your used car in seconds. Accurate, fast and completely free.</p>'
    f'</div>',
    unsafe_allow_html=True
)

# Get Started button
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
with btn_col2:
    if st.button("Get Started - Predict Now", use_container_width=True):
        st.switch_page("app.py")

st.write("")

# ── Features Section ──────────────────────────────────────────────────────────
feat_title_color = "#FFFFFF" if mode else "#1A1A2E"
st.markdown(
    f'<h2 style="text-align:center;font-size:1.8rem;font-weight:800;color:{feat_title_color};margin-bottom:1.5rem;">Why RideRepublic?</h2>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="features-grid">'
    '<div class="feature-card">'
    '<div class="feature-icon">🤖</div>'
    '<div class="feature-title">AI Powered Prediction</div>'
    '<div class="feature-desc">Machine Learning model trained on 8,000+ real car listings for accurate price prediction</div>'
    '</div>'
    '<div class="feature-card">'
    '<div class="feature-icon">⚡</div>'
    '<div class="feature-title">Instant Results</div>'
    '<div class="feature-desc">Get your car valuation in under a second — no waiting, no signup required</div>'
    '</div>'
    '<div class="feature-card">'
    '<div class="feature-icon">📄</div>'
    '<div class="feature-title">PDF Report Download</div>'
    '<div class="feature-desc">Download a complete valuation report with depreciation forecast and tips</div>'
    '</div>'
    '<div class="feature-card">'
    '<div class="feature-icon">📊</div>'
    '<div class="feature-title">Analytics Dashboard</div>'
    '<div class="feature-desc">Explore dataset insights, price trends and model performance metrics</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── How It Works ──────────────────────────────────────────────────────────────
steps_title_color = "#FFFFFF" if mode else "#1A1A2E"
st.markdown(
    '<div class="steps-wrap">'
    f'<div class="steps-title" style="color:{steps_title_color};">How It Works</div>'
    '<div class="steps-grid">'
    '<div class="step-item">'
    '<div class="step-num">1</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Enter Car Details</div>'
    '<div class="step-desc">Fill in brand, year, fuel type, KM driven and other details</div>'
    '</div>'
    '<div class="step-item">'
    '<div class="step-num">2</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Click Predict</div>'
    '<div class="step-desc">Our AI model analyzes your inputs instantly</div>'
    '</div>'
    '<div class="step-item">'
    '<div class="step-num">3</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Get Your Price</div>'
    '<div class="step-desc">View estimated price, range and depreciation chart</div>'
    '</div>'
    '<div class="step-item">'
    '<div class="step-num">4</div>'
    f'<div class="step-title" style="color:{steps_title_color};">Download Report</div>'
    '<div class="step-desc">Save your full valuation report as PDF</div>'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Stats Section ─────────────────────────────────────────────────────────────
stat_val_color = "#E8B84B" if mode else "#1A1A2E"
stat_lbl_color = "#6666AA" if mode else "#999999"
st.markdown(
    '<div class="stats-grid">'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">82%</div><div class="stat-label" style="color:{stat_lbl_color};">Model Accuracy</div></div>'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">14+</div><div class="stat-label" style="color:{stat_lbl_color};">Car Brands</div></div>'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">8K+</div><div class="stat-label" style="color:{stat_lbl_color};">Cars Trained On</div></div>'
    f'<div class="stat-card"><div class="stat-value" style="color:{stat_val_color};">Free</div><div class="stat-label" style="color:{stat_lbl_color};">Always Free</div></div>'
    '</div>',
    unsafe_allow_html=True
)

# ── CTA Bottom ────────────────────────────────────────────────────────────────
st.write("")
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("Predict Car Price", use_container_width=True):
        st.switch_page("app.py")
with c2:
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("analytics.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-bar">'
    'RideRepublic &copy; 2026 &nbsp;&nbsp; Python &nbsp;&nbsp; Scikit-Learn &nbsp;&nbsp; Streamlit &nbsp;&nbsp; Plotly'
    '</div>',
    unsafe_allow_html=True
)