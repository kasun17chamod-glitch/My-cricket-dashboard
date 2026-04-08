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
st.subheader("🏏 Batting Stats")
bat = batting_stats(df)

col1, col2, col3 = st.columns(3)

col1.metric("Matches", bat["matches"])
col2.metric("Innings", bat["innings"])
col3.metric("Runs", bat["runs"])

col1.metric("Balls", bat["balls"])
col2.metric("Average", round(bat["average"], 2))
col3.metric("Strike Rate", round(bat["strike_rate"], 2))

#st.markdown("### Additional Stats")

col1, col2, col3 = st.columns(3)

col1.metric("Highest", bat["highest_score_display"])
col2.metric("50s", bat["50s"])
col3.metric("100s", bat["100s"])

col1.metric("30+", bat["30s"])
col2.metric("Catches", bat["catches"])

st.markdown("### Dismissals")

if bat["dismissals"]:
    for method, count in bat["dismissals"].items():
        st.write(f"{method} - {count}")
else:
    st.write("No dismissals recorded")

st.markdown("---")

# ================= BOWLING =================-

st.subheader("🎯 Bowling Stats")
bowl = bowling_stats(df)

col1, col2, col3 = st.columns(3)

col1.metric("Matches", len(df))   # total matches
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

# commit test