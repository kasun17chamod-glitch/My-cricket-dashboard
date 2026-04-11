import streamlit as st


def apply_styles():
    st.markdown("""
    <style>

    /* ================= MAIN APP BACKGROUND ================= */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #172554, #0f172a);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
        color: white;
    }

    /* Animated Gradient Background */
    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* ================= PAGE FADE IN ================= */
    .main {
        animation: fadeIn 0.8s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.95);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(56, 189, 248, 0.15);
    }

    /* Sidebar Hover Cards */
    section[data-testid="stSidebar"] .block-container > div {
        background-color: rgba(30, 41, 59, 0.75);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.08);
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .block-container > div:hover {
        transform: translateY(-2px);
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56,189,248,0.20);
    }

    /* ================= METRIC CARDS ================= */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 14px;
        border: 1px solid rgba(56,189,248,0.08);
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
        box-shadow: 0 10px 25px rgba(56,189,248,0.25);
    }

    /* ================= TITLES ================= */
    h1, h2, h3 {
        color: #f1f5f9;
        text-shadow: 0 0 12px rgba(56,189,248,0.25);
    }

    /* ================= BUTTONS ================= */
    button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }

    button:hover {
        transform: scale(1.04);
        box-shadow: 0 0 15px rgba(37,99,235,0.35);
    }

    /* ================= TABLES ================= */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ================= PROFILE IMAGE ================= */
    img {
        transition: all 0.3s ease;
    }

    img:hover {
        transform: scale(1.04);
    }

    </style>
    """, unsafe_allow_html=True)