# Quick Commerce Ops Intelligence — Blinkit vs Zepto vs Swiggy

## Problem Statement
Quick commerce platforms like Blinkit, Zepto, and Swiggy Instamart promise 10-minute delivery but consumer-reported failures are frequent and publicly visible. This project quantifies delivery ops performance across platforms using real user review data and Google search trends to identify where operations are failing and why.

## Data Sources
- **Google Play Store reviews** — 1,500 reviews scraped using `google-play-scraper` (500 per platform)
- **Google Trends** — Search interest data for India over 3 months via `pytrends`

## Methodology
1. Pulled 500 reviews each for Blinkit, Zepto, and Swiggy from Google Play Store
2. Cleaned and structured data — sentiment labeling, review length analysis
3. Keyword-based complaint categorization across 5 failure types
4. Built a composite Ops Health Score (0–100) across 4 weighted factors
5. Pulled Google Trends data to analyze search interest patterns

## Key Findings

### 1. Platform Ratings
| Platform | Avg Rating | 1-Star % | 5-Star % |
|----------|-----------|----------|----------|
| Blinkit  | 4.18      | 12.6%    | 68.4%    |
| Swiggy   | 3.48      | 34.6%    | 62.4%    |
| Zepto    | 3.19      | 41.6%    | 54.2%    |

### 2. Complaint Categories (1-2 star reviews only)
| Category         | Blinkit | Swiggy | Zepto |
|-----------------|---------|--------|-------|
| App issues       | 18      | 65     | 83    |
| Late delivery    | 6       | 36     | 38    |
| Refund issues    | 11      | 30     | 31    |
| Order cancelled  | 4       | 33     | 20    |
| Wrong item       | 3       | 16     | 19    |

### 3. Review Length Signal
Negative reviews are significantly longer than positive ones across all platforms:
- Zepto: 174 chars (negative) vs 26 chars (positive) — **6.7x longer**
- Swiggy: 160 chars (negative) vs 12 chars (positive) — **13x longer**
- Blinkit: 93 chars (negative) vs 21 chars (positive) — **4.4x longer**

Longer negative reviews indicate users are articulating specific, detailed complaints — not just brief reactions.

### 4. Ops Health Score
| Platform | Score |
|----------|-------|
| Blinkit  | 69.7  |
| Swiggy   | 44.3  |
| Zepto    | 40.7  |

Score is a weighted composite of: avg rating (40%), positive sentiment % (30%), complaint intensity (20%), review length penalty (10%).

## Operational Recommendations
1. **Zepto** should prioritize app stability fixes — 83 app issue mentions in bad reviews, 4.6x worse than Blinkit. This is a fixable engineering problem with direct impact on ops performance.
2. **Swiggy** has the highest order cancellation rate — 33 mentions vs Blinkit's 4. Root cause likely lies in dark store inventory management or rider allocation logic.
3. **Blinkit** leads across all metrics but its 18 app issue mentions signal early-stage technical debt worth monitoring.

## Limitations
- Reviews reflect a single point in time (May 2026) — longitudinal data would enable trend analysis
- Keyword-based complaint categorization may miss nuanced complaints
- Google Play reviews skew toward extreme sentiment (very happy or very unhappy users)

## Tech Stack
- Python, pandas, matplotlib, openpyxl
- google-play-scraper, pytrends
- SQLite, Excel

## Files
| File | Description |
|------|-------------|
| `data_pull.py` | Pulls reviews from Google Play Store |
| `clean.py` | Cleans and structures raw data |
| `check.py` | Exploratory analysis and findings |
| `scoring.py` | Ops health score calculation |
| `trends.py` | Google Trends data pull |
| `report.py` | Generates charts and Excel report |

## Output
- `qcommerce_ops_report.xlsx` — Full report with 5 sheets
- `chart1_ratings.png` — Platform ratings comparison
- `chart2_sentiment.png` — Sentiment distribution
- `chart3_complaints.png` — Complaint categories
- `chart4_ops_score.png` — Ops health scorecard