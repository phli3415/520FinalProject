"""Shared DuckDB connection. Points `artifacts` / `repos` at the data source.

Default: the public Hugging Face Parquet mirror (no download needed).
Override with GITSKILLS_SRC=/path/to/parquet/dir (same layout) or a .sqlite file.
"""
import os
import duckdb

HF = "hf://datasets/mvaccargiu/gitskills/data"


def connect():
    src = os.environ.get("GITSKILLS_SRC", HF)
    con = duckdb.connect()
    con.sql("SET TimeZone = 'UTC'")
    if src.endswith((".sqlite", ".db")):
        con.sql(f"ATTACH '{src}' AS gs (TYPE sqlite, READ_ONLY)")
        for t in ("artifacts", "repos"):
            con.sql(f"CREATE VIEW {t} AS SELECT * FROM gs.{t}")
    else:
        for t in ("artifacts", "repos"):
            con.sql(f"CREATE VIEW {t} AS SELECT * FROM '{src}/{t}/*.parquet'")
    return con
