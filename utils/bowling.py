from utils.helpers import overs_to_balls, balls_to_overs

def bowling_stats(df):

    if not all(col in df.columns for col in ["Overs", "Runs_Conceded", "Maidens", "Wickets"]):
        return None

    df["Balls_Bowled"] = df["Overs"].apply(overs_to_balls)

    total_balls = df["Balls_Bowled"].sum()
    total_overs = balls_to_overs(total_balls)

    runs = df["Runs_Conceded"].sum()
    wickets = df["Wickets"].sum()
    maidens = df["Maidens"].sum()

    average = runs / wickets if wickets > 0 else 0
    strike_rate = total_balls / wickets if wickets > 0 else 0
    economy = runs / (total_balls / 6) if total_balls > 0 else 0

    return {
        "overs": total_overs,
        "runs": runs,
        "wickets": wickets,
        "maidens": maidens,
        "average": average,
        "strike_rate": strike_rate,
        "economy": economy
    }