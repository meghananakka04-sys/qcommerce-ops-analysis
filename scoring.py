import pandas as pd

# ------------------------------------------------------------
# OPS HEALTH SCORE
# Each platform gets a 0-100 score based on 4 factors
# Lower complaints = higher score
# ------------------------------------------------------------

df = pd.read_csv("clean_reviews.csv")

platforms = ["Blinkit", "Zepto", "Swiggy"]

# ------------------------------------------------------------
# FACTOR 1: Average rating (weight: 40%)
# Scale 1-5 to 0-100
# ------------------------------------------------------------
avg_rating = df.groupby("platform")["rating"].mean()
rating_score = ((avg_rating - 1) / 4) * 100

# ------------------------------------------------------------
# FACTOR 2: % positive reviews (weight: 30%)
# ------------------------------------------------------------
sentiment_pct = df.groupby(["platform", "sentiment"]).size().unstack(fill_value=0)
sentiment_pct = sentiment_pct.div(sentiment_pct.sum(axis=1), axis=0) * 100
positive_score = sentiment_pct["positive"]

# ------------------------------------------------------------
# FACTOR 3: Complaint category intensity (weight: 20%)
# How many bad reviews mention operational failures
# ------------------------------------------------------------
keywords = {
    "late_delivery"   : ["late", "delay", "slow", "hours", "waiting", "wait"],
    "order_cancelled" : ["cancel", "cancelled", "cancellation"],
    "wrong_item"      : ["wrong", "missing", "not delivered", "incomplete"],
    "refund_issue"    : ["refund", "money", "charged", "payment"],
    "app_issue"       : ["app", "crash", "bug", "error", "glitch"]
}

bad = df[df["rating"] <= 2].copy()
for category, words in keywords.items():
    bad[category] = bad["review"].str.lower().str.contains("|".join(words), na=False)

# Total complaint mentions per platform
complaint_counts = bad.groupby("platform")[list(keywords.keys())].sum().sum(axis=1)
total_bad = bad.groupby("platform").size()
complaint_rate = (complaint_counts / total_bad) * 100

# Invert — lower complaint rate = higher score
complaint_score = 100 - complaint_rate
complaint_score = complaint_score.clip(lower=0)

# ------------------------------------------------------------
# FACTOR 4: Review length penalty (weight: 10%)
# Longer negative reviews = more frustrated users
# ------------------------------------------------------------
neg_length = df[df["sentiment"] == "negative"].groupby("platform")["review_length"].mean()
max_len = neg_length.max()
length_score = 100 - ((neg_length / max_len) * 100)

# ------------------------------------------------------------
# COMBINE INTO FINAL SCORE
# ------------------------------------------------------------
scores = pd.DataFrame({
    "rating_score"    : rating_score,
    "positive_score"  : positive_score,
    "complaint_score" : complaint_score,
    "length_score"    : length_score
})

scores["ops_health_score"] = (
    scores["rating_score"]    * 0.40 +
    scores["positive_score"]  * 0.30 +
    scores["complaint_score"] * 0.20 +
    scores["length_score"]    * 0.10
).round(1)

print("=== OPS HEALTH SCORECARD ===\n")
print(scores[["rating_score", "positive_score", "complaint_score", "length_score", "ops_health_score"]].round(1))
print(f"\n=== FINAL RANKING ===")
print(scores["ops_health_score"].sort_values(ascending=False).round(1))