"""Q1a preliminary: monthly new adopting repos, split by adopter type.

Input : data/repo_adoption.parquet  (from scripts/q1_build_base.py)
Output: results/q1a_monthly.csv, results/q1a_monthly.png
Sample: main Q1a sample (is_large_repo = false), UTC months.
"""
from pathlib import Path
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect()
con.sql("SET TimeZone = 'UTC'")
df = con.sql(f"""
    SELECT strftime(date_trunc('month', adopted_at), '%Y-%m') AS month,
           count(*) FILTER (WHERE adopter_type = 'existing_repo') AS existing_repo,
           count(*) FILTER (WHERE adopter_type = 'new_repo')      AS new_repo,
           count(*) FILTER (WHERE adopter_type = 'ambiguous')     AS ambiguous,
           count(*)                                               AS total
    FROM '{ROOT / "data/repo_adoption.parquet"}'
    WHERE NOT is_large_repo
    GROUP BY 1 ORDER BY 1
""").df()
df["cumulative"] = df["total"].cumsum()
(ROOT / "results").mkdir(exist_ok=True)
df.to_csv(ROOT / "results/q1a_monthly.csv", index=False)
print(df.to_string(index=False))

# --- chart (palette: dataviz default slots 1-2; gray = ambiguous) ---
INK, MUTED = "#2b2b2a", "#76756f"
series = [("existing_repo", "Existing repo added skills", "#2a78d6"),
          ("new_repo", "New repo started with skills", "#eb6834"),
          ("ambiguous", "Ambiguous dates", "#c3c2b7")]
labels = [m[2:].replace("-", "/") for m in df["month"]]  # 25/10
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
bottom = [0] * len(df)
for col, name, color in series:
    ax.bar(labels, df[col], bottom=bottom, color=color, label=name,
           width=0.72, edgecolor="white", linewidth=1.5)
    bottom = [b + v for b, v in zip(bottom, df[col])]
for i in (0, len(df) - 1, int(df["total"].idxmax())):
    ax.text(i, df["total"][i] + 150, f"{df['total'][i]:,}", ha="center",
            va="bottom", fontsize=10, color=INK)
ax.set_ylabel("Repos adopting that month", color=MUTED, fontsize=10)
ax.set_xlabel("Adoption month (YY/MM, UTC)", color=MUTED, fontsize=10)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.grid(axis="y", color="#e6e5e0", linewidth=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")
ax.tick_params(colors=MUTED, labelsize=9, length=0)
ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=INK)
fig.tight_layout()
fig.savefig(ROOT / "results/q1a_monthly.png", facecolor="white")
print("saved results/q1a_monthly.png")
