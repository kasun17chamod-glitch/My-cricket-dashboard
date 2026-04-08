import pandas as pd
from utils.helpers import overs_to_balls, balls_to_overs

def bowling_stats(df):

    if not all(col in df.columns for col in ["Overs", "Runs_Conceded", "Wickets", "Maidens"]):
        return None

    # 🔹 Only rows where player actually bowled
    bowling_df = df[df["Overs"].notna()].copy()

    # 🔥 Clean numeric columns (VERY IMPORTANT)
    bowling_df["Wickets"] = pd.to_numeric(bowling_df["Wickets"], errors="coerce").fillna(0)
    bowling_df["Runs_Conceded"] = pd.to_numeric(bowling_df["Runs_Conceded"], errors="coerce").fillna(0)
    bowling_df["Maidens"] = pd.to_numeric(bowling_df["Maidens"], errors="coerce").fillna(0)

    # Convert overs → balls
    bowling_df["Balls_Bowled"] = bowling_df["Overs"].apply(overs_to_balls)

    total_balls = bowling_df["Balls_Bowled"].sum()
    total_overs = balls_to_overs(total_balls)

    runs = bowling_df["Runs_Conceded"].sum()
    wickets = int(bowling_df["Wickets"].sum())
    maidens = int(bowling_df["Maidens"].sum())

    innings = len(bowling_df)

    # ----------------------------
    # 🔥 BEST BOWLING
    # ----------------------------
    best_wickets = 0
    best_runs = 9999

    if innings > 0:
        for _, row in bowling_df.iterrows():
            wkts = int(row["Wickets"])
            runs_conceded = int(row["Runs_Conceded"])

            if wkts > best_wickets:
                best_wickets = wkts
                best_runs = runs_conceded
            elif wkts == best_wickets and runs_conceded < best_runs:
                best_runs = runs_conceded

    best_figure = f"{best_wickets}/{best_runs}" if innings > 0 else "0/0"

    # ----------------------------
    # 🔥 3W & 5W
    # ----------------------------
    three_wkts = len(bowling_df[bowling_df["Wickets"] >= 3])
    five_wkts = len(bowling_df[bowling_df["Wickets"] >= 5])

    # ----------------------------
    # 🔥 METRICS
    # ----------------------------
    average = runs / wickets if wickets > 0 else 0
    strike_rate = total_balls / wickets if wickets > 0 else 0
    economy = runs / (total_balls / 6) if total_balls > 0 else 0

    return {
        "overs": total_overs,
        "runs": runs,
        "wickets": wickets,
        "maidens": maidens,
        "innings": innings,
        "average": average,
        "strike_rate": strike_rate,
        "economy": economy,

        # 🔥 NEW
        "best": best_figure,
        "3w": three_wkts,
        "5w": five_wkts
    }
# commit test