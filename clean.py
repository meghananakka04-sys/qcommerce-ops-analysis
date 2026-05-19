import pandas as pd

# Load raw data
df = pd.read_csv("raw_reviews.csv")

print("=== BEFORE CLEANING ===")
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"\nMissing values:")
print(df.isnull().sum())
print(f"\nData types:")
print(df.dtypes)

# ------------------------------------------------------------
# CLEANING STEPS
# ------------------------------------------------------------

# 1. Drop rows where review text is missing
df = df.dropna(subset=["review"])

# 2. Drop rows where rating is missing
df = df.dropna(subset=["rating"])

# 3. Convert date to proper datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 4. Drop rows where date couldn't be parsed
df = df.dropna(subset=["date"])

# 5. Strip whitespace from text columns
df["review"] = df["review"].str.strip()
df["user"] = df["user"].str.strip()
df["platform"] = df["platform"].str.strip()

# 6. Convert rating to integer
df["rating"] = df["rating"].astype(int)

# 7. Add a review length column — useful for analysis
df["review_length"] = df["review"].str.len()

# 8. Add a label — positive (4-5 stars) vs negative (1-2) vs neutral (3)
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating <= 2:
        return "negative"
    else:
        return "neutral"

df["sentiment"] = df["rating"].apply(label_sentiment)

# 9. Reset index
df = df.reset_index(drop=True)

# ------------------------------------------------------------
# AFTER CLEANING
# ------------------------------------------------------------
print("\n=== AFTER CLEANING ===")
print(f"Total rows: {len(df)}")
print(f"\nMissing values:")
print(df.isnull().sum())
print(f"\nSentiment distribution:")
print(df.groupby(["platform", "sentiment"]).size().unstack(fill_value=0))
print(f"\nAvg review length by platform:")
print(df.groupby("platform")["review_length"].mean().round(0))

# Save cleaned data
df.to_csv("clean_reviews.csv", index=False)
print(f"\nSaved to clean_reviews.csv")