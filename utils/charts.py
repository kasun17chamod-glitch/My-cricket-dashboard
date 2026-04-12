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
# YEAR DIVIDER LINES
# ==============================
def add_year_dividers(fig, df):

    for i in range(1, len(df)):

        if df.iloc[i]["Year"] != df.iloc[i - 1]["Year"]:

            fig.add_vline(
                x=df.iloc[i]["Match No"] - 0.5,

                line_width=2,

                line_dash="dash",

                line_color="rgba(255,255,255,0.25)"
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

    # ---------------- AVG ----------------
    fig_avg = px.line(
        batting_df,
        x="Match No",
        y="Average",
        hover_data=["Year", "Opponent"],
        title="Batting Average Progression",
        markers=True
    )

    fig_avg = style_chart(fig_avg, "#38bdf8")
    fig_avg = add_year_dividers(fig_avg, batting_df)

    st.plotly_chart(fig_avg, use_container_width=True)

    # ---------------- SR ----------------
    fig_sr = px.line(
        batting_df,
        x="Match No",
        y="Strike Rate",
        hover_data=["Year", "Opponent"],
        title="Strike Rate Progression",
        markers=True
    )

    fig_sr = style_chart(fig_sr, "#06b6d4")
    fig_sr = add_year_dividers(fig_sr, batting_df)

    st.plotly_chart(fig_sr, use_container_width=True)

    # ---------------- HS ----------------
    fig_hs = px.line(
        batting_df,
        x="Match No",
        y="High Score",
        hover_data=["Year", "Opponent"],
        title="High Score Progression",
        markers=True
    )

    fig_hs = style_chart(fig_hs, "#3b82f6")
    fig_hs = add_year_dividers(fig_hs, batting_df)

    st.plotly_chart(fig_hs, use_container_width=True)


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

    # ---------------- AVG ----------------
    fig_avg = px.line(
        bowling_df,
        x="Match No",
        y="Bowling Average",
        hover_data=["Year", "Opponent"],
        title="Bowling Average Progression",
        markers=True
    )

    fig_avg = style_chart(fig_avg, "#ef4444")
    fig_avg = add_year_dividers(fig_avg, bowling_df)

    st.plotly_chart(fig_avg, use_container_width=True)

    # ---------------- SR ----------------
    fig_sr = px.line(
        bowling_df,
        x="Match No",
        y="Strike Rate",
        hover_data=["Year", "Opponent"],
        title="Bowling Strike Rate Progression",
        markers=True
    )

    fig_sr = style_chart(fig_sr, "#f97316")
    fig_sr = add_year_dividers(fig_sr, bowling_df)

    st.plotly_chart(fig_sr, use_container_width=True)

    # ---------------- ECO ----------------
    fig_eco = px.line(
        bowling_df,
        x="Match No",
        y="Economy",
        hover_data=["Year", "Opponent"],
        title="Economy Progression",
        markers=True
    )

    fig_eco = style_chart(fig_eco, "#fb923c")
    fig_eco = add_year_dividers(fig_eco, bowling_df)

    st.plotly_chart(fig_eco, use_container_width=True)