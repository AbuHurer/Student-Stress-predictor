import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load CSV
df = pd.read_csv("combined_stress_cleaned.csv")

# Load model
model = joblib.load("random_forest_stress.pkl")

# Only numeric columns for sliders
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

st.set_page_config(page_title="Student Stress Prediction", layout="centered")

# Inject your custom CSS
st.markdown(
    """
    <style>
    /* ---------- Page background & base ---------- */
    :root{
      --bg1: #0f1724;    /* deep navy */
      --bg2: #081021;    /* darker */
      --card: rgba(255,255,255,0.04);
      --glass: rgba(255,255,255,0.03);
      --accent1: #6dd3f5; /* cyan */
      --accent2: #a78bfa; /* purple */
      --accent3: #ffb86b; /* warm */
      --muted: rgba(255,255,255,0.6);
    }

    html, body, [data-testid="stAppViewContainer"]{
      background: radial-gradient(1200px 600px at 10% 10%, rgba(120,90,255,0.06), transparent 5%),
                  radial-gradient(900px 500px at 90% 90%, rgba(100,220,255,0.03), transparent 10%),
                  linear-gradient(180deg,var(--bg1), var(--bg2));
      color: #e6eef8;
      font-family: Inter, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* ---------- Main container ---------- */
    main .block-container {
      padding: 2rem 2rem 3rem 2rem;
      max-width: 1000px;
    }

    /* ---------- Header / Title ---------- */
    .app-header {
      display:flex;
      align-items:center;
      gap:16px;
      margin-bottom: 1rem;
    }
    .app-logo {
      width:64px;
      height:64px;
      border-radius:12px;
      background: linear-gradient(135deg,var(--accent1),var(--accent2));
      box-shadow: 0 8px 30px rgba(90,70,255,0.15), inset 0 -6px 20px rgba(255,255,255,0.03);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      color:#06223a;
      font-size:22px;
    }
    .app-title {
      font-size:28px;
      font-weight:700;
      letter-spacing: -0.5px;
      color: white;
    }

    /* ---------- Panels (glass cards) ---------- */
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.04);
      border-radius: 14px;
      padding: 18px;
      box-shadow: 0 6px 30px rgba(2,6,23,0.6);
      margin-bottom: 1rem;
    }

    /* ---------- Sidebar styling ---------- */
    [data-testid="stSidebar"] .css-1d391kg {
      background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));
      border-right: 1px solid rgba(255,255,255,0.02);
    }

    /* Inputs (number inputs & sliders) */
    .stNumberInput, input[type="number"] {
      border-radius: 10px !important;
      background: rgba(255,255,255,0.02) !important;
      padding: 10px !important;
      color: #e6eef8 !important;
      border: 1px solid rgba(255,255,255,0.04) !important;
    }

    /* Button style */
    .stButton>button {
      background: linear-gradient(90deg,var(--accent1), var(--accent2));
      color: #04233a;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 12px;
      border: none;
      box-shadow: 0 8px 24px rgba(110,88,255,0.14);
    }
    .stButton>button:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 32px rgba(110,88,255,0.18);
    }

    /* ---------- Probability bars ---------- */
    .prob-row {
      display: flex;
      align-items:center;
      gap: 12px;
      margin: 6px 0;
    }
    .prob-label {
      min-width: 160px;
      font-weight:600;
      color: var(--muted);
      font-size: 14px;
    }
    .prob-bar {
      height: 14px;
      width: 100%;
      background: rgba(255,255,255,0.04);
      border-radius: 999px;
      overflow: hidden;
      box-shadow: inset 0 -2px 8px rgba(0,0,0,0.6);
    }
    .prob-fill {
      height: 100%;
      border-radius: 999px;
      transition: width 600ms ease;
      box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }
    .prob-val {
      min-width: 56px;
      text-align: right;
      font-weight:700;
      color: #e7f6ff;
    }

    .fill-0 { background: linear-gradient(90deg, rgba(109,211,245,1), rgba(167,139,250,0.95)); }
    .fill-1 { background: linear-gradient(90deg, rgba(255,184,107,1), rgba(255,120,120,0.95)); }
    .fill-2 { background: linear-gradient(90deg, rgba(150,255,200,1), rgba(110,220,255,0.95)); }

    .small-muted { color: rgba(230,238,248,0.62); font-size:13px; }
    .center { display:flex; align-items:center; justify-content:center; }

    @media (max-width:640px){
      .app-title { font-size:20px; }
      .prob-label { min-width: 110px; font-size:13px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.markdown('<div class="app-header"><div class="app-logo">😵</div><div class="app-title">🎯 Student Stress Prediction</div></div>', unsafe_allow_html=True)

# Collect slider inputs
input_data = {}
for col in numeric_cols:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    default_val = float(df[col].mean())
    input_data[col] = st.slider(col, min_val, max_val, default_val)

input_df = pd.DataFrame([input_data])

# Predict
if st.button("Predict Stress Level"):
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    stress_labels = ["Type 1 +EUStress", "Type 2 +EUStress", "Type 3 -DIStress"]

    st.markdown(f"<div class='card center'><h3>Predicted: {stress_labels[int(prediction)]}</h3></div>", unsafe_allow_html=True)

    # Show probability bars
    for i, label in enumerate(stress_labels):
        prob_percent = probabilities[i] * 100
        st.markdown(
            f"""
            <div class="prob-row">
                <div class="prob-label">{label}</div>
                <div class="prob-bar">
                    <div class="prob-fill fill-{i}" style="width:{prob_percent}%;"></div>
                </div>
                <div class="prob-val">{prob_percent:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
