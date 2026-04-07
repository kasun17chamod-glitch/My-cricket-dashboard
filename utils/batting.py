def batting_stats(df):

    total_runs = df["Runs"].sum()
    total_balls = df["Balls"].sum()
    matches = len(df)

    outs = len(df[df["Out"] == "yes"]) if "Out" in df.columns else 0

    average = total_runs / outs if outs > 0 else 0
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    return {
        "runs": total_runs,
        "balls": total_balls,
        "matches": matches,
        "average": average,
        "strike_rate": strike_rate
    }