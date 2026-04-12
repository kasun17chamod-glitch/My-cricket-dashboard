import pandas as pd
import plotly.express as px
import streamlit as st


# ==============================
# COMMON CHART STYLE
# ==============================
def style_chart(fig, line_color):

    fig.update_traces(
        line=dict(
            width=5,
            color=line_color
        ),

        marker=dict(
            size=10,
            color=line_color,
            line=dict(
                width=2,
                color="white"
            )
        ),

        fill='tozeroy',

        hovertemplate=
        "<b>Match:</b> %{x}<br>" +
        "<b>Value:</b> %{y:.2f}<extra></extra>"
    )

    fig.update_layout(

        height=450,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title_font=dict(
            size=20
        ),

        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=14,
            font_color="white"
        ),

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)'
        )
    )

    return fig


# ==============================
# YEAR DIVIDERS + LABELS
# ==============================
def add_year_dividers(fig, df):

    split_positions = []
    year_ranges = []

    start_match = df.iloc[0]["Match No"]
    current_year = df.iloc[0]["Year"]

    for i in range(1, len(df)):

        if df.iloc[i]["Year"] != df.iloc[i - 1]["Year"]:

            split_x = df.iloc[i]["Match No"] - 0.5
            split_positions.append(split_x)

            year_ranges.append((
                current_year,
                start_match,
                df.iloc[i - 1]["Match No"]
            ))

            start_match = df.iloc[i]["Match No"]
            current_year = df.iloc[i]["Year"]

    year_ranges.append((
        current_year,
        start_match,
        df.iloc[len(df)-1]["Match No"]
    ))

    # Divider lines
    for split_x in split_positions:

        fig.add_vline(
            x=split_x,
            line_width=2,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)"
        )

    # Labels
    for year, start, end in year_ranges:

        midpoint = (start + end) / 2

        fig.add_annotation(
            x=midpoint,
            y=1.05,
            yref="paper",

            text=str(year),

            showarrow=False,

            font=dict(
                size=14,
                color="rgba(255,255,255,0.65)"
            )
        )

    return fig


# ==============================
# BATTING CHARTS
# ==============================
def render_batting_charts(df):

    batting_df = df[df["Runs"].notna()].copy()

    batting_df["Runs"] = pd.to_numeric(
        batting_df["Runs"],
        errors="coerce"
    ).fillna(0)

    batting_df["Balls"] = pd.to_numeric(
        batting_df["Balls"],
        errors="coerce"
    ).fillna(0)

    batting_df = batting_df.reset_index(drop=True)

    batting_df["Match No"] = batting_df.index + 1

    batting_df["Cumulative_Runs"] = batting_df["Runs"].cumsum()

    batting_df["Out_Flag"] = (
        batting_df["Out"]
        .astype(str)
        .str.lower()
        .eq("yes")
        .astype(int)
    )

    batting_df["Cumulative_Outs"] = batting_df["Out_Flag"].cumsum()

    batting_df["Average"] = (
        batting_df["Cumulative_Runs"] /
        batting_df["Cumulative_Outs"].replace(0, 1)
    )

    batting_df["Strike Rate"] = (
        batting_df["Cumulative_Runs"] /
        batting_df["Balls"].cumsum().replace(0, 1) * 100
    )

    batting_df["High Score"] = batting_df["Runs"].cummax()

    st.markdown("## 🏏 Batting Analytics")

    for title, y_col, color in [
        ("Batting Average Progression", "Average", "#38bdf8"),
        ("Strike Rate Progression", "Strike Rate", "#06b6d4"),
        ("High Score Progression", "High Score", "#3b82f6")
    ]:

        fig = px.line(
            batting_df,
            x="Match No",
            y=y_col,
            hover_data=["Year", "Opponent"],
            title=title,
            markers=True
        )

        fig = style_chart(fig, color)
        fig = add_year_dividers(fig, batting_df)

        st.plotly_chart(fig, use_container_width=True)


# ==============================
# BOWLING CHARTS
# ==============================
def render_bowling_charts(df):

    bowling_df = df[df["Overs"].notna()].copy()

    bowling_df["Runs_Conceded"] = pd.to_numeric(
        bowling_df["Runs_Conceded"],
        errors="coerce"
    ).fillna(0)

    bowling_df["Wickets"] = pd.to_numeric(
        bowling_df["Wickets"],
        errors="coerce"
    ).fillna(0)

    bowling_df["Overs"] = pd.to_numeric(
        bowling_df["Overs"],
        errors="coerce"
    ).fillna(0)

    bowling_df = bowling_df.reset_index(drop=True)

    bowling_df["Match No"] = bowling_df.index + 1

    bowling_df["Cum_Runs"] = bowling_df["Runs_Conceded"].cumsum()

    bowling_df["Cum_Wickets"] = bowling_df["Wickets"].cumsum()

    bowling_df["Cum_Overs"] = bowling_df["Overs"].cumsum()

    bowling_df["Bowling Average"] = (
        bowling_df["Cum_Runs"] /
        bowling_df["Cum_Wickets"].replace(0, 1)
    )

    bowling_df["Economy"] = (
        bowling_df["Cum_Runs"] /
        bowling_df["Cum_Overs"].replace(0, 1)
    )

    bowling_df["Strike Rate"] = (
        bowling_df["Cum_Overs"] * 6 /
        bowling_df["Cum_Wickets"].replace(0, 1)
    )

    st.markdown("## 🎯 Bowling Analytics")

    for title, y_col, color in [
        ("Bowling Average Progression", "Bowling Average", "#ef4444"),
        ("Bowling Strike Rate Progression", "Strike Rate", "#f97316"),
        ("Economy Progression", "Economy", "#fb923c")
    ]:

        fig = px.line(
            bowling_df,
            x="Match No",
            y=y_col,
            hover_data=["Year", "Opponent"],
            title=title,
            markers=True
        )

        fig = style_chart(fig, color)
        fig = add_year_dividers(fig, bowling_df)

        st.plotly_chart(fig, use_container_width=True)