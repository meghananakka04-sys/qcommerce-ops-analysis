from google_play_scraper import reviews, Sort
import pandas as pd

def pull_reviews(app_name, app_id, count=500):
    print(f"Pulling reviews for {app_name}...")
    
    result, _ = reviews(
        app_id,
        lang="en",
        country="in",
        sort=Sort.NEWEST,
        count=count
    )
    
    desired = ["userName", "score", "content", "at"]
    rows = []
    for r in result:
        if isinstance(r, dict):
            rows.append({k: r.get(k) for k in desired})
        else:
            rows.append({k: None for k in desired})

    df = pd.DataFrame(rows, columns=desired)
    df.columns = ["user", "rating", "review", "date"]
    df["platform"] = app_name
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    
    print(f"  Got {len(df)} reviews")
    return df

# Pull only Zepto
zepto_df = pull_reviews("Zepto", "com.zeptoconsumerapp", count=500)

# Append to existing CSV
existing_df = pd.read_csv("raw_reviews.csv")
final_df = pd.concat([existing_df, zepto_df], ignore_index=True)
final_df.to_csv("raw_reviews.csv", index=False)

print(f"\nTotal reviews now in CSV: {len(final_df)}")