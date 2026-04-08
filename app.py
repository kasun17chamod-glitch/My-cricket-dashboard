import streamlit as st
from utils.loader import load_data
from utils.batting import batting_stats
from utils.bowling import bowling_stats


# ================= UI STYLE =================
def set_background():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #020617;
            color: white;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #334155;
        }

        /* Titles */
        h1, h2, h3 {
            color: #f1f5f9;
        }

        /* Buttons */
        button {
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 8px !important;
        }

        /* Sidebar section cards */
        section[data-testid="stSidebar"] .block-container > div {
            background-color: #020617;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #1e293b;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


set_background()

# ================= LOAD DATA =================
df = load_data("data/cricket_stats.xlsx")

st.title("Cricket Stats 🏏")

# ================= FILTERS =================
st.sidebar.title("🏏 Filters")

# --- YEAR FILTER ---
with st.sidebar.container():

    st.markdown(
        "<div style='font-size:18px; font-weight:600; color:#38bdf8;'>📅 Year</div>",
        unsafe_allow_html=True
    )

    # space below title
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    year_options = sorted(df["Year"].dropna().unique())
    selected_years = []

    for year in year_options:
        if st.checkbox(str(year), value=True, key=f"year_{year}"):
            selected_years.append(year)

    df = df[df["Year"].isin(selected_years)]

    # space after section
    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

# --- MATCH TYPE FILTER ---
with st.sidebar.container():

    st.markdown(
        "<div style='font-size:18px; font-weight:600; color:#fbbf24;'>🏆 Match Type</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    type_options = sorted(df["Match_Type"].dropna().unique())
    selected_types = []

    for t in type_options:
        if st.checkbox(str(t), value=True, key=f"type_{t}"):
            selected_types.append(t)

    df = df[df["Match_Type"].isin(selected_types)]

    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    # space after section
    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
#OPPONENT FILTER

with st.sidebar.container():

    st.markdown(
        "<div style='font-size:18px; font-weight:600; color:#34d399;'>🏟️ Opponent</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    if "Opponent" in df.columns:

        opponent_options = sorted(df["Opponent"].dropna().unique())

        selected_opponents = st.multiselect(
            "Search opponent (leave empty for all)",
            options=opponent_options,
            default=[],   # 🔥 KEY CHANGE
            help="Type team name to filter. Leave empty to see all matches."
        )

        # 🔥 APPLY FILTER ONLY IF USER SELECTS
        if selected_opponents:
            df = df[df["Opponent"].isin(selected_opponents)]

# --- RESET BUTTON ---
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Filters"):
    st.experimental_rerun()

# ================= BATTING =================
st.subheader("🏏 Batting Stats")
bat = batting_stats(df)

col1, col2, col3 = st.columns(3)

col1.metric("Matches", bat["matches"])
col2.metric("Innings", bat["innings"])
col3.metric("Runs", bat["runs"])

col1.metric("Balls", bat["balls"])
col2.metric("Average", round(bat["average"], 2))
col3.metric("Strike Rate", round(bat["strike_rate"], 2))

col1, col2, col3 = st.columns(3)

col1.metric("Highest", bat["highest_score_display"])
col2.metric("50s", bat["50s"])
col3.metric("100s", bat["100s"])

col1.metric("30+", bat["30s"])
col2.metric("Catches", bat["catches"])

#DISMISSALS
st.markdown("### Dismissals")

with st.expander("⬇️ View Dismissals", expanded=False):

    if bat["dismissals"]:

        # 🔹 Sort by count (highest first)
        sorted_dismissals = sorted(
            bat["dismissals"].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for method, count in sorted_dismissals:
            col1, col2 = st.columns([3, 1])

            col1.markdown(f"**{method}**")
            col2.markdown(f"**{count}**")

    else:
        st.write("No dismissals recorded")

# ================= BOWLING =================
st.subheader("🎯 Bowling Stats")
bowl = bowling_stats(df)

col1, col2, col3 = st.columns(3)

col1.metric("Matches", len(df))
col2.metric("Innings", bowl["innings"])
col3.metric("Wickets", bowl["wickets"])

col1.metric("Overs", bowl["overs"])
col2.metric("Maidens", bowl["maidens"])
col3.metric("Economy", round(bowl["economy"], 2))

col1, col2, col3 = st.columns(3)

col1.metric("Average", round(bowl["average"], 2))
col2.metric("Strike Rate", round(bowl["strike_rate"], 2))

col1, col2, col3 = st.columns(3)

col1.metric("Best", bowl["best"])
col2.metric("3W", bowl["3w"])
col3.metric("5W", bowl["5w"])