import streamlit as st
from utils.loader import load_data
from utils.batting import batting_stats
from utils.bowling import bowling_stats

# Load data
df = load_data("data/cricket_stats.xlsx")

st.title("🏏 My Cricket Dashboard")

# ================= FILTERS =================
st.sidebar.header("Filters")

if "Year" in df.columns:
    year_filter = st.sidebar.multiselect(
        "Select Year",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )
    df = df[df["Year"].isin(year_filter)]

if "Match_Type" in df.columns:
    type_filter = st.sidebar.multiselect(
        "Match Type",
        options=df["Match_Type"].unique(),
        default=df["Match_Type"].unique()
    )
    df = df[df["Match_Type"].isin(type_filter)]

# ================= BATTING =================
bat = batting_stats(df)

st.header("Batting Stats")

col1, col2 = st.columns(2)

col1.metric("Runs", bat["runs"])
col1.metric("Matches", bat["matches"])
col1.metric("Average", round(bat["average"], 2))

col2.metric("Balls", bat["balls"])
col2.metric("Strike Rate", round(bat["strike_rate"], 2))

# ================= BOWLING =================
bowl = bowling_stats(df)

if bowl:
    st.header("Bowling Stats")

    col3, col4 = st.columns(2)

    col3.metric("Overs", bowl["overs"])
    col3.metric("Runs", bowl["runs"])
    col3.metric("Wickets", bowl["wickets"])

    col4.metric("Maidens", bowl["maidens"])
    col4.metric("Average", round(bowl["average"], 2))
    col4.metric("Economy", round(bowl["economy"], 2))