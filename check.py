import pandas as pd

df = pd.read_csv("clean_reviews.csv")
df["date"] = pd.to_datetime(df["date"])




df = pd.read_csv("clean_reviews.csv")
df["date"] = pd.to_datetime(df["date"])

# Complaint volume over time per platform
bad = df[df["rating"] <= 2]
bad = bad.copy()
bad["week"] = bad["date"].dt.to_period("W")
print("Bad reviews by week and platform:")
print(bad.groupby(["platform", "week"]).size().unstack(fill_value=0))