"""Build the Q1 repo_adoption table and cache it to data/repo_adoption.parquet."""
from pathlib import Path
from db import connect

ROOT = Path(__file__).resolve().parents[1]
con = connect()
con.sql((ROOT / "queries/q1_repo_adoption.sql").read_text())
out = ROOT / "data/repo_adoption.parquet"
con.sql(f"COPY repo_adoption TO '{out}' (FORMAT parquet)")
print(con.sql("""SELECT count(*) AS repos,
                        count(*) FILTER (WHERE NOT is_large_repo) AS main_q1a,
                        count(*) FILTER (WHERE NOT is_large_repo AND repo_created_at < '2025-10-01') AS q1b
                 FROM repo_adoption""").df().to_string(index=False))
print("saved", out)
