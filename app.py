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

# Page configuration
st.set_page_config(page_title="RideRepublic: Check Resale Value Quickly", page_icon="riderepublic_logo.png", layout="wide")

# Helper to encode logo as base64 for HTML embedding
def get_logo_base64(path="riderepublic_logo.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    mode = sac.switch(label='Theme', align='start', size='md', on_label='🌙', off_label='☀️')

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

        /* Download button - dark mode */
        [data-testid="stDownloadButton"] button {
            background-color: #1E1E1E !important;
            color: white !important;
            border: 1px solid #FF4B4B !important;
            border-radius: 10px !important;
            width: 100% !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background-color: #FF4B4B !important;
            color: white !important;
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

        /* Download button - light mode */
        [data-testid="stDownloadButton"] button {
            background-color: #F0F2F6 !important;
            color: #262730 !important;
            border: 1px solid #d3d3d3 !important;
            border-radius: 10px !important;
            width: 100% !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background-color: #262730 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Brand logos
brand_logos = {
    "BMW":"bmw.png",
    "Audi":"audi.png",
    "Chevrolet":"chevrolet.webp",
    "Ford":"ford.jpeg",
    "Honda":"honda.png",
    "Hyundai":"hyundai.png",
    "Mahindra":"mahindra1.jpeg",
    "Maruti":"maruti.jpeg",
    "Mercedes-Benz":"mercedes-benz.png",
    "Nissan":"nissan.png",
    "Renault":"renault.png",
    "Skoda":"skoda.jpg",
    "Tata":"tata.webp",
    "Toyota":"toyota.png"
}

# ── Header with logo ──────────────────────────────────────────────────────────
if logo_b64:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:18px; margin-bottom:4px;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:80px; height:80px; border-radius:50%; object-fit:cover; box-shadow:0 2px 12px rgba(0,0,0,0.25);" />
            <div>
                <h1 style="margin:0; font-size:2.2rem; font-weight:800; letter-spacing:-0.5px;">RideRepublic</h1>
                <p style="margin:0; font-size:1rem; opacity:0.65;">Smart Car Pricing · AI-Powered Valuation</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.title("🚗 RideRepublic")

st.markdown("### Predict Your Car's Resale Value Instantly")
st.markdown("---")

# ── Sidebar inputs ────────────────────────────────────────────────────────────
st.sidebar.header("Enter Car Details")

brands = [
"Nissan","Audi","Chevrolet","Ford","Honda","Hyundai",
"Mahindra","Maruti","Mercedes-Benz","BMW",
"Renault","Skoda","Tata","Toyota","Other"
]

# Reset counter trick — increment to force all widgets back to defaults
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

owner_mapping = {
    "First Owner":0,
    "Second Owner":1,
    "Third Owner":2,
    "Fourth & Above Owner":3
}
owner = owner_mapping[owner_label]

fuel         = st.sidebar.selectbox("Fuel", ["Diesel","Petrol","LPG"], index=0, key=f"fuel_{rc}")
transmission = st.sidebar.selectbox("Transmission", ["Manual","Automatic"], index=0, key=f"transmission_{rc}")
seller_type  = st.sidebar.selectbox("Seller Type", ["Individual","Trustmark Dealer"], index=0, key=f"seller_{rc}")

# ── Reset button at the very bottom of sidebar ────────────────────────────────
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Inputs"):
    st.session_state.reset_counter += 1
    st.rerun()

# ── PDF Generator ─────────────────────────────────────────────────────────────
def generate_pdf(brand, year, km_driven, mileage, engine, seats,
                 owner_label, fuel, transmission, seller_type,
                 price, low, high, dep_df):

    pdf = FPDF()
    pdf.set_margins(10, 10, 10)
    pdf.add_page()

    W = 190  # usable width

    # ── Header bar ──
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

    # ── Title ──
    pdf.set_xy(10, 35)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(W, 8, "Car Resale Valuation Report", align="C")
    pdf.ln(10)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    # ── Section helper ──
    def section_header(title):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(220, 220, 220)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(W, 7, f"  {title}", fill=True)
        pdf.ln(8)

    # ── Car Details ──
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
        if i % 2 == 0:
            pdf.set_fill_color(248, 248, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(95, 6, f"  {label}", fill=True)
        pdf.cell(95, 6, f"  {value}", fill=True)
        pdf.ln(6)

    pdf.ln(2)

    # ── Prediction Result ──
    section_header("Prediction Result")

    price_lakh = price / 100000
    low_lakh   = low / 100000
    high_lakh  = high / 100000

    pdf.set_fill_color(20, 20, 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(W, 11, f"  Estimated Resale Price:  Rs. {price_lakh:.2f} Lakhs  ({int(price):,})", fill=True)
    pdf.ln(13)

    pdf.set_fill_color(220, 245, 220)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(W, 7, f"  Expected Price Range:  Rs. {low_lakh:.2f} L  -  Rs. {high_lakh:.2f} L", fill=True)
    pdf.ln(9)

    # ── Depreciation Table ──
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
        if i % 2 == 0:
            pdf.set_fill_color(248, 248, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(95, 6, f"  {int(row['Year'])}", fill=True)
        pdf.cell(95, 6, f"  Rs. {row['Estimated Value']/100000:.2f} Lakhs", fill=True)
        pdf.ln(6)

    pdf.ln(2)

    # ── Tips ──
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
        x = pdf.get_x()
        pdf.set_x(10)
        pdf.multi_cell(W, 5, f"  * {tip}")
        pdf.set_x(10)

    # ── Footer ──
    pdf.set_y(-18)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(W, 8, "RideRepublic © 2026  |  AI-Powered Car Valuation  |  For reference purposes only.", align="C")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name

# ── Show brand logo ───────────────────────────────────────────────────────────
if brand in brand_logos:
    st.image(brand_logos[brand], width=190)

st.subheader("Prediction Result")

if st.button("Predict Price 🚀"):

    with st.spinner("Analyzing car data..."):

        input_df = pd.DataFrame(columns=model.feature_names_in_)
        input_df.loc[0] = 0

        input_df.at[0,'year'] = year
        input_df.at[0,'km_driven'] = km_driven
        input_df.at[0,'mileage(km/ltr/kg)'] = mileage
        input_df.at[0,'engine'] = engine
        input_df.at[0,'seats'] = seats
        input_df.at[0,'owner'] = owner

        brand_col        = f"brand_{brand}"
        fuel_col         = f"fuel_{fuel}"
        transmission_col = f"transmission_{transmission}"
        seller_col       = f"seller_type_{seller_type}"

        if brand_col in input_df.columns:
            input_df.at[0, brand_col] = 1
        if fuel_col in input_df.columns:
            input_df.at[0, fuel_col] = 1
        if transmission_col in input_df.columns:
            input_df.at[0, transmission_col] = 1
        if seller_col in input_df.columns:
            input_df.at[0, seller_col] = 1

        numeric_cols = ['year','km_driven','mileage(km/ltr/kg)','engine','seats']
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        y_log    = model.predict(input_df)
        y_actual = np.exp(y_log)
        price    = round(y_actual[0], 0)

        # Depreciation
        years_list  = []
        prices_list = []
        for i in range(6):
            years_list.append(year + i)
            prices_list.append(price * (0.9 ** i))

        dep_df = pd.DataFrame({"Year": years_list, "Estimated Value": prices_list})

        low  = round(price * 0.9)
        high = round(price * 1.1)

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"💰 Estimated Price: ₹ {price}")
            st.metric("Expected Price Range", f"₹{low} - ₹{high}")

        with col2:
            price_in_lakhs = price / 100000
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=price_in_lakhs,
                number={'prefix': "₹", 'suffix': " L", 'valueformat': '.2f'},
                title={'text': "Car Value (Lakhs)"},
                gauge={'axis': {'range': [0, 50]}, 'bar': {'color': "green"}}
            ))
            st.plotly_chart(fig, use_container_width=True)

        # Depreciation chart
        st.markdown("---")
        st.subheader("📉 Estimated Car Depreciation")

        fig_dep = go.Figure()
        fig_dep.add_trace(go.Bar(
            y=dep_df["Year"],
            x=dep_df["Estimated Value"] / 100000,
            orientation='h',
            name="Depreciation",
            hovertemplate="Year: %{y}<br>Price: ₹%{x:.2f} Lakhs"
        ))
        fig_dep.update_layout(
            title="Projected Car Resale Value Trend",
            xaxis_title="Price (₹ Lakhs)",
            yaxis_title="Year",
            font={'color': "white" if mode else "black"}
        )
        st.plotly_chart(fig_dep, use_container_width=True)

        # ── PDF Download ──────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("📄 Download Valuation Report")

        pdf_path = generate_pdf(
            brand, year, km_driven, mileage, engine, seats,
            owner_label, fuel, transmission, seller_type,
            price, low, high, dep_df
        )

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name=f"RideRepublic_{brand}_{year}_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        os.unlink(pdf_path)

st.markdown("---")

st.subheader('Tips To Maintain a Good Resale Value')

st.write("""
• **Regular Servicing:** Maintain proper service records to build buyer trust.  
• **Low Mileage:** Cars with lower mileage usually sell at higher prices.  
• **Clean Interior & Exterior:** A well-maintained car attracts better resale offers.  
• **Accident-Free Record:** Vehicles without accident history maintain higher value.  
• **Original Parts:** Avoid replacing parts with non-genuine components.
""")

st.markdown("---")

st.subheader("About This Model")

st.write("""
RideRepublic is an AI-powered car valuation platform that estimates the resale price of used cars based on key vehicle attributes.

The machine learning model analyzes:

• Manufacturing year  
• Kilometers driven  
• Mileage  
• Engine capacity  
• Fuel type  
• Transmission  
• Brand  
• Ownership history  
         
RideRepublic © 2026
""")

st.markdown("---")

st.subheader("📊 Explore Model Analytics")

st.write("View detailed graphs, dataset insights, and model performance.")

if st.button('Open Analytics Dashboard 📈'):
    st.switch_page("pages/analytics.py")

st.markdown("---")

st.caption("Technology Stack: Python • Scikit-Learn • Streamlit • Plotly")
