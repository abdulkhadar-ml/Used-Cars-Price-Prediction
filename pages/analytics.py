import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit_antd_components as sac
import base64

st.set_page_config(page_title="RideRepublic Analytics", page_icon="riderepublic_logo.png", layout="wide")

def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

with st.sidebar:
    mode = sac.switch(label='Theme', align='start', size='md', on_label='🌙', off_label='☀️')
    st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.2);margin:0.5rem 0;'>", unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("app.py")

ACCENT = "#E8B84B"

if mode:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"], p, div, span, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stApp {
        background-color: #0D0D14;
        background-image: radial-gradient(ellipse at 80% 0%, rgba(232,184,75,0.06) 0%, transparent 55%);
        color: #E2E2EE;
    }
    section[data-testid="stSidebar"] {
        background-color: #111118 !important;
        border-right: 1px solid #252535 !important;
    }
    [data-testid="stSidebarNav"] { display: none !important; }
    div.stButton > button {
        background: linear-gradient(135deg, #E8B84B 0%, #D4A43A 100%) !important;
        color: #0D0D14 !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 18px rgba(232,184,75,0.3) !important;
    }
    .hero-section {
        background: linear-gradient(135deg, #14142A 0%, #1C1C3A 100%);
        border: 1px solid #2A2A45;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.2rem; font-weight: 800;
        color: #FFFFFF; margin: 0; letter-spacing: -0.5px;
    }
    .hero-accent { color: #E8B84B; }
    .hero-sub { font-size: 0.92rem; color: rgba(255,255,255,0.5); margin-top: 0.3rem; }
    .hero-badge {
        display: inline-flex; align-items: center;
        background: rgba(232,184,75,0.1); border: 1px solid rgba(232,184,75,0.25);
        color: #E8B84B; border-radius: 50px; padding: 4px 14px;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 0.8rem; text-transform: uppercase;
    }
    .stat-card {
        background: #111118; border: 1px solid #252535;
        border-radius: 14px; padding: 1.2rem 1.4rem; text-align: center;
        transition: border-color 0.2s, transform 0.2s;
    }
    .stat-card:hover { border-color: #E8B84B; transform: translateY(-2px); }
    .stat-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.7rem; font-weight: 800; color: #E8B84B;
    }
    .stat-label {
        font-size: 0.72rem; color: #6666AA;
        text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;
    }
    .section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem; font-weight: 700; color: #FFFFFF;
        margin: 1.5rem 0 0.8rem 0; display: flex; align-items: center; gap: 8px;
    }
    .section-header::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, #252535, transparent);
    }
    .perf-table {
        width: 100%; border-collapse: collapse;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .perf-table th {
        background: #1E1E32; color: #6666AA;
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px;
        padding: 10px 16px; text-align: left; border-bottom: 1px solid #252535;
    }
    .perf-table td {
        padding: 14px 16px; border-bottom: 1px solid #1A1A28;
        font-size: 1.05rem; font-weight: 700; color: #E8B84B;
    }
    .perf-table .metric-name { color: #AAAACC; font-weight: 500; font-size: 0.88rem; }
    .perf-table tr:last-child td { border-bottom: none; }
    .footer-bar {
        background: #111118; border: 1px solid #252535;
        border-radius: 12px; padding: 1rem 2rem;
        text-align: center; color: #44445A; font-size: 0.78rem; margin-top: 2rem;
    }
    [data-testid="stMetricValue"] { color: #E8B84B !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
    [data-testid="stMetricLabel"] { color: #6666AA !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"], p, div, span, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stApp { background-color: #F5F2ED; color: #1A1A2E; }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E8E2D9 !important;
    }
    [data-testid="stSidebarNav"] { display: none !important; }
    div.stButton > button {
        background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important; width: 100% !important;
    }
    .hero-section {
        background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%);
        border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.2rem; font-weight: 800;
        color: #FFFFFF; margin: 0; letter-spacing: -0.5px;
    }
    .hero-accent { color: #E8B84B; }
    .hero-sub { font-size: 0.92rem; color: rgba(255,255,255,0.55); margin-top: 0.3rem; }
    .hero-badge {
        display: inline-flex; align-items: center;
        background: rgba(232,184,75,0.15); border: 1px solid rgba(232,184,75,0.4);
        color: #E8B84B; border-radius: 50px; padding: 4px 14px;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 0.8rem; text-transform: uppercase;
    }
    .stat-card {
        background: #FFFFFF; border: 1px solid #E8E2D9;
        border-radius: 14px; padding: 1.2rem 1.4rem; text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.2s;
    }
    .stat-card:hover { border-color: #1A1A2E; transform: translateY(-2px); }
    .stat-value { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.7rem; font-weight: 800; color: #1A1A2E; }
    .stat-label { font-size: 0.72rem; color: #999; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px; }
    .section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem; font-weight: 700; color: #1A1A2E;
        margin: 1.5rem 0 0.8rem 0; display: flex; align-items: center; gap: 8px;
    }
    .section-header::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, #E8E2D9, transparent);
    }
    .perf-table {
        width: 100%; border-collapse: collapse;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .perf-table th {
        background: #F5F2ED; color: #999;
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px;
        padding: 10px 16px; text-align: left; border-bottom: 1px solid #E8E2D9;
    }
    .perf-table td {
        padding: 14px 16px; border-bottom: 1px solid #F0EDE8;
        font-size: 1.05rem; font-weight: 700; color: #1A1A2E;
    }
    .perf-table .metric-name { color: #555; font-weight: 500; font-size: 0.88rem; }
    .perf-table tr:last-child td { border-bottom: none; }
    .footer-bar {
        background: #FFFFFF; border: 1px solid #E8E2D9;
        border-radius: 12px; padding: 1rem 2rem;
        text-align: center; color: #BBB; font-size: 0.78rem; margin-top: 2rem;
    }
    [data-testid="stMetricValue"] { color: #1A1A2E !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
    [data-testid="stMetricLabel"] { color: #999 !important; }
    </style>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;" />' if logo_b64 else ""

st.markdown(f"""
<div class="hero-section">
    <div style="display:flex;align-items:center;gap:16px;">
        <div>{logo_img}</div>
        <div>
            <div class="hero-badge">DATA INSIGHTS</div>
            <h1 class="hero-title">Ride<span class="hero-accent">Republic</span> Analytics</h1>
            <p class="hero-sub">Dataset analysis, distribution insights and model performance</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_csv('cleaned_car_datas.csv')
df['price_lakh'] = df['selling_price'] / 100000

chart_bg   = 'rgba(0,0,0,0)'
grid_color = 'rgba(128,128,128,0.1)'
font_color = '#888888' if mode else '#555555'
text_color = '#FFFFFF' if mode else '#1A1A2E'
font_fam   = 'Plus Jakarta Sans'

def apply_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family=font_fam, size=14, color=text_color)),
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        font=dict(color=font_color, family=font_fam),
        margin=dict(t=40, b=30, l=20, r=20),
        xaxis=dict(gridcolor=grid_color, showline=False, tickfont=dict(family=font_fam)),
        yaxis=dict(gridcolor=grid_color, showline=False, tickfont=dict(family=font_fam)),
    )
    return fig

# ── Dataset KPIs ──────────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Dataset Overview</p>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
stats = [
    (f"{len(df):,}", "Total Records"),
    (str(df['brand'].nunique() if 'brand' in df.columns else 14), "Brands"),
    (f"Rs.{df['price_lakh'].mean():.1f}L", "Avg Price"),
    (f"{int(df['year'].min())}-{int(df['year'].max())}", "Year Range"),
    (f"{int(df['km_driven'].median()/1000)}K km", "Median KM"),
]
for col, (val, label) in zip([k1,k2,k3,k4,k5], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Price Analysis ────────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Price Analysis</p>", unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

with ch1:
    fig = px.histogram(df, x="price_lakh", nbins=20,
                       labels={'price_lakh': 'Price (Rs. Lakhs)'},
                       color_discrete_sequence=[ACCENT])
    fig = apply_layout(fig, "Price Distribution")
    fig.update_traces(marker_line_color='rgba(0,0,0,0.15)', marker_line_width=0.5)
    st.plotly_chart(fig, use_container_width=True)

with ch2:
    fig = px.scatter(df, x='year', y='price_lakh',
                     labels={'price_lakh': 'Price (Rs. Lakhs)', 'year': 'Year'},
                     color_discrete_sequence=['#6C8EBF'], opacity=0.55)
    fig.update_traces(marker=dict(size=5))
    fig = apply_layout(fig, "Price vs Manufacturing Year")
    st.plotly_chart(fig, use_container_width=True)

# ── Brand & Usage ─────────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Brand & Usage</p>", unsafe_allow_html=True)
ch3, ch4 = st.columns(2)

with ch3:
    brand_price = df.groupby("brand")["price_lakh"].mean().reset_index()
    brand_price = brand_price.sort_values("price_lakh", ascending=True).tail(10)
    fig = px.bar(brand_price, x="price_lakh", y="brand", orientation='h',
                 labels={"price_lakh": "Avg Price (Rs. Lakhs)", "brand": "Brand"},
                 color="price_lakh",
                 color_continuous_scale=[[0,'#355C7D'],[0.5,'#9467BD'],[1,ACCENT]])
    fig.update_layout(coloraxis_showscale=False)
    fig = apply_layout(fig, "Top 10 Brands by Avg Price")
    st.plotly_chart(fig, use_container_width=True)

with ch4:
    fig = px.scatter(df, x="km_driven", y="price_lakh",
                     labels={"km_driven": "KM Driven", "price_lakh": "Price (Rs. Lakhs)"},
                     color_discrete_sequence=["#2ca02c"], opacity=0.5)
    fig.update_traces(marker=dict(size=5))
    fig = apply_layout(fig, "KM Driven vs Price")
    st.plotly_chart(fig, use_container_width=True)

# ── Vehicle Characteristics ───────────────────────────────────────────────────
st.markdown("<p class='section-header'>Vehicle Characteristics</p>", unsafe_allow_html=True)
ch5, ch6, ch7 = st.columns(3)

with ch5:
    fuel_counts = df["fuel"].value_counts().reset_index()
    fuel_counts.columns = ["Fuel Type", "Count"]
    fig = px.pie(fuel_counts, names="Fuel Type", values="Count",
                 color_discrete_sequence=[ACCENT, '#355C7D', '#FF6B6B'], hole=0.45)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(family=font_fam))
    fig = apply_layout(fig, "Fuel Type Distribution")
    st.plotly_chart(fig, use_container_width=True)

with ch6:
    fig = px.pie(df, names="transmission",
                 color_discrete_sequence=['#1A1A2E', ACCENT], hole=0.45)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(family=font_fam))
    fig = apply_layout(fig, "Transmission Distribution")
    st.plotly_chart(fig, use_container_width=True)

with ch7:
    owner_counts = df["owner"].value_counts().reset_index()
    owner_counts.columns = ["Owner Type", "Count"]
    fig = px.bar(owner_counts, x="Owner Type", y="Count",
                 color_discrete_sequence=[ACCENT])
    fig.update_traces(marker_line_width=0)
    fig = apply_layout(fig, "Ownership Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ── Advanced Analysis ─────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Advanced Analysis</p>", unsafe_allow_html=True)
ch8, ch9 = st.columns(2)

with ch8:
    fig = px.scatter(df, x="mileage(km/ltr/kg)", y="price_lakh",
                     labels={"mileage(km/ltr/kg)": "Mileage (km/l)", "price_lakh": "Price (Rs. Lakhs)"},
                     color_discrete_sequence=["#17becf"], opacity=0.55)
    fig.update_traces(marker=dict(size=5))
    fig = apply_layout(fig, "Mileage vs Price")
    st.plotly_chart(fig, use_container_width=True)

with ch9:
    corr = df.select_dtypes(include=['int64','float64']).corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu", aspect="auto")
    fig.update_layout(
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        font=dict(color=font_color, size=10, family=font_fam),
        margin=dict(t=30, b=10, l=10, r=10),
        title=dict(text="Feature Correlation Heatmap",
                   font=dict(family=font_fam, size=14, color=text_color))
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Model Performance ─────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Model Performance</p>", unsafe_allow_html=True)

td_color = "#E8B84B" if mode else "#1A1A2E"
name_color = "#AAAACC" if mode else "#555555"
border_c = "#1A1A28" if mode else "#F0EDE8"
th_bg = "#1E1E32" if mode else "#F5F2ED"
card_bg = "#111118" if mode else "#FFFFFF"
card_border = "#252535" if mode else "#E8E2D9"

st.markdown(f"""
<div style="background:{card_bg};border:1px solid {card_border};border-radius:16px;padding:1.8rem;">
    <table class="perf-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Interpretation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="metric-name">Train R2 Score</td>
                <td style="color:{td_color};">0.83</td>
                <td class="metric-name">83% variance explained on training data</td>
            </tr>
            <tr>
                <td class="metric-name">Test R2 Score</td>
                <td style="color:{td_color};">0.82</td>
                <td class="metric-name">82% variance explained on unseen data</td>
            </tr>
            <tr>
                <td class="metric-name">MAE</td>
                <td style="color:{td_color};">Rs. 77,695</td>
                <td class="metric-name">Average prediction error</td>
            </tr>
            <tr>
                <td class="metric-name">RMSE</td>
                <td style="color:{td_color};">Rs. 1,06,605</td>
                <td class="metric-name">Root mean squared error</td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    RideRepublic Analytics 2026 &nbsp;&nbsp; Python &nbsp;&nbsp;
    Scikit-Learn &nbsp;&nbsp; Streamlit &nbsp;&nbsp; Plotly
</div>
""", unsafe_allow_html=True)
