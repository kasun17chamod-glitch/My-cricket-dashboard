import pandas as pd
import plotly.express as px
import streamlit as st


# ==============================
# COMMON CHART STYLING
# ==============================
def style_chart(fig, line_color):

    fig.update_traces(
        line=dict(
            width=5,
            color=line_color
        ),

        marker=dict(
            size=12,
            color=line_color,
            line=dict(
                width=2,
                color="white"
            )
        ),

        fill='tozeroy',

        fillcolor=f'rgba{tuple(list(px.colors.hex_to_rgb(line_color)) + [0.15])}',

        hovertemplate=
        "<b>Year:</b> %{x}<br>" +
        "<b>Value:</b> %{y:.2f}<extra></extra>"
    )

    fig.update_layout(

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title_font=dict(
            size=20,
            color='white'
        ),

        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=14,
            font_color="white",
            bordercolor=line_color
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False
        ),

        transition=dict(
            duration=800,
            easing='cubic-in-out'
        )
    )

    fig.update_xaxes(type='category')

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

    batting_grouped = batting_df.groupby("Year").agg({
        "Runs": ["sum", "max"],
        "Balls": "sum"
    }).reset_index()

    batting_grouped.columns = [
        "Year",
        "Total_Runs",
        "High_Score",
        "Balls"
    ]

    batting_grouped["Average"] = (
        batting_grouped["Total_Runs"] /
        batting_df.groupby("Year").size().values
    )

    batting_grouped["Strike_Rate"] = (
        batting_grouped["Total_Runs"] /
        batting_grouped["Balls"].replace(0, 1) * 100
    )

    batting_grouped["Year"] = batting_grouped["Year"].astype(str)

    st.markdown("## 🏏 Batting Analytics")

    col1, col2 = st.columns(2)

    # LEFT COLUMN
    with col1:

        fig_avg = px.line(
            batting_grouped,
            x="Year",
            y="Average",
            title="Batting Average Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_avg, "#38bdf8"),
            use_container_width=True
        )

        fig_sr = px.line(
            batting_grouped,
            x="Year",
            y="Strike_Rate",
            title="Strike Rate Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_sr, "#06b6d4"),
            use_container_width=True
        )

    # RIGHT COLUMN
    with col2:

        fig_hs = px.line(
            batting_grouped,
            x="Year",
            y="High_Score",
            title="High Score Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_hs, "#3b82f6"),
            use_container_width=True
        )
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

    grouped = bowling_df.groupby("Year").agg({
        "Runs_Conceded": "sum",
        "Wickets": "sum",
        "Overs": "sum"
    }).reset_index()

    grouped["Bowling_Average"] = (
        grouped["Runs_Conceded"] /
        grouped["Wickets"].replace(0, 1)
    )

    grouped["Economy"] = (
        grouped["Runs_Conceded"] /
        grouped["Overs"].replace(0, 1)
    )

    grouped["Strike_Rate"] = (
        grouped["Overs"] * 6 /
        grouped["Wickets"].replace(0, 1)
    )

    grouped["Year"] = grouped["Year"].astype(str)

    st.markdown("## 🎯 Bowling Analytics")

    col1, col2 = st.columns(2)

    with col1:

        fig_bavg = px.line(
            grouped,
            x="Year",
            y="Bowling_Average",
            title="Bowling Average Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_bavg, "#ef4444"),
            use_container_width=True
        )

        fig_sr = px.line(
            grouped,
            x="Year",
            y="Strike_Rate",
            title="Bowling Strike Rate Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_sr, "#f97316"),
            use_container_width=True
        )

    with col2:

        fig_eco = px.line(
            grouped,
            x="Year",
            y="Economy",
            title="Economy Over Time",
            markers=True
        )

        st.plotly_chart(
            style_chart(fig_eco, "#fb923c"),
            use_container_width=True
        )