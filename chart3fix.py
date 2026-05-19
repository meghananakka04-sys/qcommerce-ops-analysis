import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

df = pd.read_csv("clean_reviews.csv")

platforms = ["Blinkit", "Swiggy", "Zepto"]
bar_colors = ["#F4C430", "#FC8019", "#8B5CF6"]

keywords = {
    "Late delivery"   : ["late", "delay", "slow", "hours", "waiting", "wait"],
    "Order cancelled" : ["cancel", "cancelled", "cancellation"],
    "Wrong item"      : ["wrong", "missing", "not delivered", "incomplete"],
    "Refund issue"    : ["refund", "money", "charged", "payment"],
    "App issue"       : ["app", "crash", "bug", "error", "glitch"]
}

bad = df[df["rating"] <= 2].copy()
for category, words in keywords.items():
    bad[category] = bad["review"].str.lower().str.contains("|".join(words), na=False)
complaint_counts = bad.groupby("platform")[list(keywords.keys())].sum()

fig, ax = plt.subplots(figsize=(10, 6))
complaint_data = complaint_counts.loc[platforms]
x = range(len(keywords))
width = 0.25

for i, platform in enumerate(platforms):
    offset = (i - 1) * width
    vals = [complaint_data.loc[platform, cat] for cat in keywords.keys()]
    bars = ax.bar([xi + offset for xi in x], vals, width=width,
                  label=platform, color=bar_colors[i])
    for bar, val in zip(bars, vals):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                    str(int(val)), ha="center", va="bottom", fontsize=7)

ax.set_title("Complaint Categories by Platform", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Number of mentions", fontsize=11)
ax.set_xticks(list(x))
ax.set_xticklabels(list(keywords.keys()), fontsize=11)
ax.legend(fontsize=11)
ax.set_ylim(0, complaint_data.values.max() + 15)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("chart3_complaints.png", dpi=150)
plt.close()
print("Chart 3 saved")