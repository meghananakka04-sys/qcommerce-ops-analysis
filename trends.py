from pytrends.request import TrendReq
import pandas as pd
import time

# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------
pytrends = TrendReq(hl="en-IN", tz=330) # India timezone



# Search terms — what frustrated users actually type
TERMS = [
    "Blinkit",
    "Zepto",
    "Swiggy Instamart"
]


# ------------------------------------------------------------
# PULL SEARCH INTEREST OVER TIME
# ------------------------------------------------------------
def get_trends(terms, timeframe="today 3-m"):
    """
    Pulls Google search interest for given terms over timeframe.
    timeframe options: "today 3-m", "today 12-m", "today 1-m"
    """
    pytrends.build_payload(
        terms,
        cat=0,
        timeframe=timeframe,
        geo="IN"        # India only
    )
    
    df = pytrends.interest_over_time()
    
    if df.empty:
        print("No data returned — try different terms")
        return None
    
    # Drop the isPartial column
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])
    
    return df

# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
print("Pulling Google Trends data for India...")
print(f"Terms: {TERMS}")
print(f"Timeframe: last 3 months\n")

df_trends = get_trends(TERMS, timeframe="today 3-m")

if df_trends is not None:
    print("=== SEARCH INTEREST OVER TIME ===")
    print(df_trends.tail(10))
    
    print(f"\n=== SUMMARY ===")
    print(f"Date range: {df_trends.index.min()} to {df_trends.index.max()}")
    print(f"\nAverage search interest (0-100 scale):")
    print(df_trends.mean().round(1))
    
    print(f"\nPeak search interest dates:")
    for col in df_trends.columns:
        peak_date = df_trends[col].idxmax()
        peak_val = df_trends[col].max()
        print(f"  {col}: {peak_date.date()} (value: {peak_val})")
    
    # Save
    df_trends.to_csv("trends_data.csv")
    print(f"\nSaved to trends_data.csv")