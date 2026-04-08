import pandas as pd

def batting_stats(df):

    # Only rows where player actually batted
    batting_df = df[df["Runs"].notna()]

    matches = len(df)
    innings = len(batting_df)

    total_runs = batting_df["Runs"].sum()
    total_balls = batting_df["Balls"].sum()

    # Outs (only count when Out == "yes")
    outs = len(batting_df[batting_df["Out"].str.lower() == "yes"]) if "Out" in df.columns else 0

    average = total_runs / outs if outs > 0 else 0
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    highest_score = 0
    highest_score_display = "0"

    if innings > 0 and not batting_df["Runs"].isna().all():
        max_runs = batting_df["Runs"].max()

        highest_rows = batting_df[batting_df["Runs"] == max_runs]

        # Prefer not out innings
        not_out_rows = highest_rows[highest_rows["Out"].str.lower() != "yes"]

        if not not_out_rows.empty:
            highest_row = not_out_rows.iloc[0]
            highest_score_display = f"{int(max_runs)}*"
        else:
            highest_row = highest_rows.iloc[0]
            highest_score_display = str(int(max_runs))

        highest_score = int(max_runs)

    # 30+, 50s, 100s
    thirties = len(batting_df[(batting_df["Runs"] >= 30) & (batting_df["Runs"] < 50)])
    fifties = len(batting_df[(batting_df["Runs"] >= 50) & (batting_df["Runs"] < 100)])
    hundreds = len(batting_df[batting_df["Runs"] >= 100])

    # Catches
    catches = df["Catch"].fillna(0).sum() if "Catch" in df.columns else 0

    # Dismissal types
    dismissal_counts = {}

    if "Dismissal" in df.columns:
        clean_df = df[df["Dismissal"].notna()].copy()

        clean_df["Dismissal"] = clean_df["Dismissal"].str.strip().str.lower()

        # Standardize properly
        clean_df["Dismissal"] = clean_df["Dismissal"].replace({
            "lbw": "LBW",
            "runout": "Run Out",
            "run out": "Run Out",
            "stump": "Stumped",
            "stumped": "Stumped",
            "bowled": "Bowled",
            "caught": "Caught",
            "hit wkt": "Hit Wicket",
            "caught b": "Caught B"

        })

        dismissal_counts = clean_df["Dismissal"].value_counts().to_dict()

    return {
        "runs": total_runs,
        "balls": total_balls,
        "matches": matches,
        "innings": innings,
        "average": average,
        "strike_rate": strike_rate,


        "highest_score": highest_score,
        "highest_score_display": highest_score_display,
        "30s": thirties,
        "50s": fifties,
        "100s": hundreds,
        "catches": catches,
        "dismissals": dismissal_counts
    }