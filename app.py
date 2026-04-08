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
# ================= BATTING =================
with st.container():

    st.markdown("## 🏏 Batting Stats")

    bat = batting_stats(df)

    # 🔹 Row 1
    col1, col2, col3 = st.columns(3)
    col1.metric("Matches", bat["matches"])
    col2.metric("Innings", bat["innings"])
    col3.metric("Runs", bat["runs"])

    # 🔹 Row 2
    col1, col2, col3 = st.columns(3)
    col1.metric("Balls", bat["balls"])
    col2.metric("Average", round(bat["average"], 2))
    col3.metric("Strike Rate", round(bat["strike_rate"], 2))

    # 🔹 Row 3
    col1, col2, col3 = st.columns(3)

    col1.metric("50s", bat["50s"])
    col2.metric("100s", bat["100s"])
    col3.metric("30+", bat["30s"])

    # 🔹 Row 4
    col1, col2, col3 = st.columns(3)
    col1.metric("Highest", bat["highest_score_display"])
    col2.metric("4s",  int(df["4s"].fillna(0).sum()) if "4s" in df.columns else 0)
    col3.metric("6s", int(df["6s"].fillna(0).sum() if "6s" in df.columns else 0))

    # 🔹 Row 5
    col1, col2, col3 = st.columns(3)
    col1.metric("Catches", bat["catches"])

# ================= BATTING DETAILS =================
with st.expander("⬇️ View Best Batting Match Details", expanded=False):

    batting_df = df[df["Runs"].notna()].copy()

    if not batting_df.empty:

        # -----------------------------
        # 🔥 HIGHEST SCORE MATCH
        # -----------------------------
        st.markdown("### 🏆 Highest Score Match")

        max_runs = batting_df["Runs"].max()
        highest_df = batting_df[batting_df["Runs"] == max_runs]

        st.dataframe(
            highest_df[["Year", "Match_Type", "Opponent", "Runs", "Balls", "Dismissal"]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # -----------------------------
        # 🔥 100s
        # -----------------------------
        st.markdown("### 💯 Hundreds")

        hundreds_df = batting_df[batting_df["Runs"] >= 100]

        if not hundreds_df.empty:
            st.dataframe(
                hundreds_df[["Year", "Match_Type", "Opponent", "Runs", "Balls", "Dismissal"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No hundreds")

        st.markdown("---")

        # -----------------------------
        # 🔥 50s
        # -----------------------------
        st.markdown("### 🔥 Fifties")

        fifties_df = batting_df[
            (batting_df["Runs"] >= 50) & (batting_df["Runs"] < 100)
        ]

        if not fifties_df.empty:
            st.dataframe(
                fifties_df[["Year", "Match_Type", "Opponent", "Runs", "Balls", "Dismissal"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No fifties")

        st.markdown("---")

        # -----------------------------
        # 🔥 30+
        # -----------------------------
        st.markdown("### 📈 30+ Scores")

        thirty_df = batting_df[
            (batting_df["Runs"] >= 30) & (batting_df["Runs"] < 50)
        ]

        if not thirty_df.empty:
            st.dataframe(
                thirty_df[["Year", "Match_Type", "Opponent", "Runs", "Balls", "Dismissal"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No 30+ scores")

    else:
        st.write("No batting data available")


#DISMISSALS
with st.expander("⬇️ View Dismissals", expanded=False):

    if bat["dismissals"]:

        # Sort highest first
        sorted_dismissals = sorted(
            bat["dismissals"].items(),
            key=lambda x: x[1],
            reverse=True
        )

        st.markdown("### 📊 Click a dismissal to see details")

        selected_dismissal = None

        for method, count in sorted_dismissals:
            col1, col2 = st.columns([4, 1])

            # 🔥 clickable button
            if col1.button(f"{method}", key=f"dismiss_{method}"):
                selected_dismissal = method

            col2.markdown(f"**{count}**")

        # -----------------------------
        # 🔥 SHOW MATCH DETAILS
        # -----------------------------
        if selected_dismissal:

            st.markdown("---")
            st.markdown(f"### 📝 Matches with **{selected_dismissal}**")

            # filter dataframe
            filtered_df = df[
                df["Dismissal"].str.strip().str.lower()
                == selected_dismissal.lower()
            ]

            if not filtered_df.empty:
                st.dataframe(
                    filtered_df[["Year", "Match_Type", "Opponent", "Runs", "Balls"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No records found")


# ================= BOWLING =================
with st.container():

    st.markdown("## 🎯 Bowling Stats")

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

    # 🔥 DETAILS INSIDE SAME BOX
    with st.expander("⬇️ View Best Bowling Match Details", expanded=False):

        bowling_df = df[df["Overs"].notna()].copy()

        if not bowling_df.empty:

            # -----------------------------
            # 🔥 BEST BOWLING MATCH
            # -----------------------------
            st.markdown("### 🏆 Best Bowling Performance")

            # find best row again (same logic)
            best_row = None
            best_wkts = -1
            best_runs = 9999

            for _, row in bowling_df.iterrows():
                wkts = int(row["Wickets"])
                runs = int(row["Runs_Conceded"])

                if wkts > best_wkts or (wkts == best_wkts and runs < best_runs):
                    best_wkts = wkts
                    best_runs = runs
                    best_row = row

            if best_row is not None:
                best_df = best_row.to_frame().T

                st.dataframe(
                    best_df[["Year", "Match_Type", "Opponent", "Overs", "Maidens", "Runs_Conceded", "Wickets"]],
                    use_container_width=True,
                    hide_index=True
                )

            st.markdown("---")

            # -----------------------------
            # 🔥 5 WICKETS
            # -----------------------------
            st.markdown("### 🔥 5 Wicket Matches")

            five_df = bowling_df[bowling_df["Wickets"] >= 5]

            if not five_df.empty:
                st.dataframe(
                    five_df[["Year", "Match_Type", "Opponent", "Overs", "Maidens", "Runs_Conceded", "Wickets"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No 5 wicket hauls")

            st.markdown("---")

            # -----------------------------
            # 🔥 3 WICKETS
            # -----------------------------
            st.markdown("### 📈 3 Wicket Matches")

            three_df = bowling_df[bowling_df["Wickets"] >= 3]

            if not three_df.empty:
                st.dataframe(
                    three_df[["Year", "Match_Type", "Opponent", "Overs", "Maidens", "Runs_Conceded", "Wickets"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No 3 wicket matches")

        else:
            st.write("No bowling data available")