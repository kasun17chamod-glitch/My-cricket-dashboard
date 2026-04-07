import pandas as pd

def load_data(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    if "Out" in df.columns:
        df["Out"] = df["Out"].astype(str).str.strip().str.lower()

    return df