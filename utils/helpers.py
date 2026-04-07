import pandas as pd

def overs_to_balls(overs_value):
    if pd.isna(overs_value):
        return 0

    overs_str = str(overs_value).strip()

    if "." in overs_str:
        over_part, ball_part = overs_str.split(".")
        over_part = int(over_part)
        ball_part = int(ball_part)
    else:
        over_part = int(overs_str)
        ball_part = 0

    if ball_part > 5:
        raise ValueError(f"Invalid overs value: {overs_value}")

    return over_part * 6 + ball_part


def balls_to_overs(balls):
    full_overs = balls // 6
    remaining_balls = balls % 6
    return f"{full_overs}.{remaining_balls}"