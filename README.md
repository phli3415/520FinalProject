# GitSkills: adoption and purpose of agent skills (CS520 / MSR 2027 Mining Challenge)

Team ai_slop_busters. Dataset: GitSkills (Zenodo 10.5281/zenodo.21875637;
Parquet mirror `huggingface.co/datasets/mvaccargiu/gitskills`).

- **Q1a** How quickly does the skill format spread across repositories?
- **Q1b** Which projects adopt first (language, popularity, age, activity)?
- **Q2** What do developers codify in skills, and in which contexts?

## Setup

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

By default the scripts query the public Hugging Face Parquet mirror directly
(no 44 GB download; DuckDB reads only the needed columns). To use a local copy:

```bash
export GITSKILLS_SRC=/path/to/gitskills.sqlite   # or a Parquet dir with the same layout
```

## Run

```bash
cd scripts
../.venv/bin/python q1_build_base.py   # builds data/repo_adoption.parquet (~10 s)
../.venv/bin/python q1a_curve.py       # results/q1a_monthly.csv + .png
```

Expected from `q1_build_base.py`: 52,068 repos; 51,410 in the Q1a sample; 11,323 in the Q1b sample.

## Layout

```
queries/   SQL (one file per derived table)
scripts/   Python: db connection, builders, analyses, plots
results/   small outputs (CSV, PNG) that slides/paper cite
data/      local caches, git-ignored
```

All dates are bucketed in UTC (`SET TimeZone = 'UTC'`).
