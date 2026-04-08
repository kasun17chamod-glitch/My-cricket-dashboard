import pandas as pd

def load_data(path):
    df = pd.read_excel(path)

    # 🔹 Convert batting columns (blank → NaN)
    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce')

    # 🔹 Convert bowling columns (blank → NaN)
    df['Overs'] = pd.to_numeric(df['Overs'], errors='coerce')
    df['Wickets'] = pd.to_numeric(df['Wickets'], errors='coerce')

    return df