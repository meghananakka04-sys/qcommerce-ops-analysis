import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
df = pd.read_csv("clean_reviews.csv")

platforms = ["Blinkit", "Swiggy", "Zepto"]

keywords = {
    "App issues"      : ["app", "crash", "bug", "error", "glitch"],
    "Late delivery"   : ["late", "delay", "slow", "hours", "waiting", "wait"],
    "Refund issues"   : ["refund", "money", "charged", "payment"],
    "Order cancelled" : ["cancel", "cancelled", "cancellation"],
    "Wrong item"      : ["wrong", "missing", "not delivered", "incomplete"]
}

bad = df[df["rating"] <= 2].copy()
for category, words in keywords.items():
    bad[category] = bad["review"].str.lower().str.contains("|".join(words), na=False)

complaint_counts = bad.groupby("platform")[list(keywords.keys())].sum()

# ------------------------------------------------------------
# WEIGHTED RESOURCE ALLOCATION MODEL
# ------------------------------------------------------------
print("=" * 60)
print("COMPLAINT-WEIGHTED RESOURCE ALLOCATION MODEL")
print("=" * 60)

allocation = {}

for platform in platforms:
    counts = complaint_counts.loc[platform]
    total = counts.sum()
    weights = (counts / total * 100).round(1)
    ranks = weights.rank(ascending=False).astype(int)
    
    platform_df = pd.DataFrame({
        "Complaint count" : counts,
        "Allocation %"    : weights,
        "Priority rank"   : ranks
    }).sort_values("Allocation %", ascending=False)
    
    allocation[platform] = platform_df
    
    print(f"\n{platform} — Total complaint mentions: {total}")
    print(platform_df.to_string())

# ------------------------------------------------------------
# CROSS PLATFORM PRIORITY MATRIX
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("CROSS-PLATFORM PRIORITY MATRIX")
print("=" * 60)

allocation_pct = pd.DataFrame({
    platform: (complaint_counts.loc[platform] / complaint_counts.loc[platform].sum() * 100).round(1)
    for platform in platforms
})

print("\nResource allocation % by problem area:")
print(allocation_pct.to_string())

# ------------------------------------------------------------
# URGENCY SCORE
# Which platform needs most urgent intervention overall
# Based on total complaint volume relative to review count
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("PLATFORM URGENCY SCORE")
print("=" * 60)

total_reviews = df.groupby("platform").size()
total_complaints = complaint_counts.sum(axis=1)
urgency = (total_complaints / total_reviews * 100).round(1)
urgency = urgency.sort_values(ascending=False)

print("\nUrgency score (complaint mentions per 100 reviews):")
for platform in urgency.index:
    print(f"  {platform}: {urgency[platform]} complaint mentions per 100 reviews")

# ------------------------------------------------------------
# VISUALIZE — STACKED BAR ALLOCATION CHART
# ------------------------------------------------------------
colors_map = {
    "App issues"      : "#8B5CF6",
    "Late delivery"   : "#EF4444",
    "Refund issues"   : "#F59E0B",
    "Order cancelled" : "#3B82F6",
    "Wrong item"      : "#10B981"
}

fig, ax = plt.subplots(figsize=(12, 6))
bottom = [0] * len(platforms)

for category in keywords.keys():
    vals = [allocation_pct.loc[category, p] for p in platforms]
    bars = ax.bar(platforms, vals, bottom=bottom,
                  label=category, color=colors_map[category], width=0.5)
    for bar, val, bot in zip(bars, vals, bottom):
        if val > 5:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bot + val/2,
                    f"{val}%",
                    ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
    bottom = [b + v for b, v in zip(bottom, vals)]

ax.set_title("Recommended Ops Resource Allocation by Platform (%)",
             fontsize=13, fontweight="bold", pad=15)
ax.set_ylabel("Resource allocation %", fontsize=11)
ax.set_ylim(0, 110)
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9, borderaxespad=0)
ax.grid(axis="y", alpha=0.2)
plt.tight_layout()
plt.savefig("chart5_allocation.png", dpi=150)
plt.close()
print("\nChart saved: chart5_allocation.png")

