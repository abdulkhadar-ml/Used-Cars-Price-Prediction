import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_antd_components as sac
import base64

st.set_page_config(page_title="RideRepublic Analytics", layout="wide")

# Helper to encode logo as base64 for HTML embedding
def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

with st.sidebar:
    mode = sac.switch(label='Theme', align='start', size='md', on_label='🌙', off_label='☀️')
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.switch_page("app.py")

# Dark / Light theme
if mode:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        
        div.stButton > button {
            background-color: #1E1E1E !important;
            color: white !important;
            border: 1px solid #FF4B4B !important;
            border-radius: 10px;
            width: 100%;
        }

        div[data-testid="stNotification"] {
            background-color: #1B3022 !important;
            color: #71ef99 !important;
            border: 1px solid #2d5a3c !important;
        }

        div[data-testid="stMetricLabel"] > div {
            color: #bcbcbc !important;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        /* ============================
           LIGHT MODE BACKGROUND COLOR
           Change this hex to customize
           ============================ */
        .stApp {
            background-color: #F5F0EB;
            color: #262730;
        }

        [data-testid="stMetricValue"] {
            color: #1a1a1a !important;
        }
        [data-testid="stMetricLabel"] {
            color: #4f4f4f !important;
        }
        [data-testid="stMetricDelta"] {
            color: #09ab3b !important;
        }
        
        div.stButton > button {
            background-color: #F0F2F6 !important;
            color: #262730 !important;
            border: 1px solid #d3d3d3 !important;
        }

        div[data-testid="stNotification"] {
            background-color: #D4EDDA !important;
            color: #155724 !important;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ── Header with logo ──────────────────────────────────────────────────────────
if logo_b64:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:18px; margin-bottom:4px;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:80px; height:80px; border-radius:50%; object-fit:cover; box-shadow:0 2px 12px rgba(0,0,0,0.25);" />
            <div>
                <h1 style="margin:0; font-size:2.2rem; font-weight:800; letter-spacing:-0.5px;">RideRepublic Analytics</h1>
                <p style="margin:0; font-size:1rem; opacity:0.65;">Detailed Insights About The Dataset & Model Performance</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.title("RideRepublic Model Analytics")
    st.markdown("Detailed Insights About The Dataset & Model Performance")

st.markdown("---")

df = pd.read_csv('cleaned_car_datas.csv')

# price distribution
df['price_lakh'] = df['selling_price'] / 100000
fig = px.histogram(df, x="price_lakh", nbins=10, title="Car Price Distribution in Lakhs",
                   labels={'price_lakh':'Selling Price (Lakhs)'}, color_discrete_sequence=["#AD9612"])
st.plotly_chart(fig, width='stretch')

st.markdown('---')

# car price vs year
fig = px.scatter(df, x='year', y='price_lakh', title='Car Price (Lakhs) vs Manufacturing Year',
                 labels={'price_lakh':'Selling Price (Lakhs)', 'year':'Manufacturing Year'},
                 color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig, width='stretch')
st.markdown("---")

# km driven vs price
fig = px.scatter(df, x="km_driven", y="price_lakh", title="KM Driven vs Car Price",
                 labels={"km_driven":"KM Driven", "price_lakh":"Price (₹ Lakhs)"},
                 color_discrete_sequence=["#2ca02c"])
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# top 10 expensive car brands
brand_price = df.groupby("brand")["price_lakh"].mean().reset_index()
brand_price = brand_price.sort_values(by="price_lakh", ascending=False).head(10)

fig = px.bar(brand_price, x="brand", y="price_lakh", title="Top 10 Expensive Car Brands",
             labels={"price_lakh":"Average Price (₹ Lakhs)", "brand":"Car Brand"},
             color_discrete_sequence=["#9467BD"])
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# mileage vs car price
fig = px.scatter(df, x="mileage(km/ltr/kg)", y="price_lakh", title="Mileage vs Car Price",
                 labels={"mileage":"mileage(km/ltr/kg)", "price_lakh":"Price (₹ Lakhs)"},
                 color_discrete_sequence=["#17becf"])
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# ownership type
owner_counts = df["owner"].value_counts().reset_index()
owner_counts.columns = ["Owner Type", "Count"]

fig = px.bar(owner_counts, x="Owner Type", y="Count", title="Ownership Type Distribution",
             color_discrete_sequence=["#bcbd22"])
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# transmission type dist
fig = px.pie(df, names="transmission", title="Transmission Type Distribution",
             color_discrete_sequence=['#355C7D'])
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# fuel type dist
import plotly.express as px

fuel_counts = df["fuel"].value_counts().reset_index()
fuel_counts.columns = ["Fuel Type", "Count"]

fig = px.bar(fuel_counts, x="Fuel Type", y="Count", title="Fuel Type Distribution",
             color_discrete_sequence=["#FF7F0E"])
fig.update_traces(textposition="outside", text=fuel_counts["Count"])
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# heatmap correlation
corr_matrix = df.select_dtypes(include=['int64','float64']).corr()

fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale="RdBu",
                title="Feature Correlation Heatmap")
fig.update_layout(height=700, width=1200)
fig.update_layout(font=dict(size=25))
st.plotly_chart(fig, use_container_width=True)

# model performance
st.subheader("📈 Model Performance")

st.markdown("""
<style>
.metric-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Train R² Score", value="0.83")

with col2:
    st.metric(label="Test R² Score", value="0.82")

with col3:
    st.metric(label="MAE", value="₹ 77,695")

with col4:
    st.metric(label="RMSE", value="₹ 1,06,605")

st.markdown('</div>', unsafe_allow_html=True)
