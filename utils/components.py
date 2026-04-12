import streamlit as st


def animated_metric(label, value, color="#38bdf8"):
    st.markdown(f"""
        <div style="
            background: rgba(30,41,59,0.65);
            padding: 18px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(56,189,248,0.10);
            animation: fadeMetric 0.8s ease;
            margin-bottom:10px;
        ">
            <div style="
                font-size: 14px;
                color: #94a3b8;
                margin-bottom:8px;
            ">
                {label}
            </div>

            <div style="
                font-size: 30px;
                font-weight: bold;
                color: {color};
            ">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)