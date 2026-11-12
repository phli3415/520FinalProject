-- Q1 base table: one row per repo that adopted skills under .claude/skills/.
-- Implements the Q1 analysis plan, section 3 (data processing).
-- Expects views/tables named `artifacts` and `repos` (see scripts/db.py).
-- Expected result: 52,068 rows; 51,410 with is_large_repo = false.
SET TimeZone = 'UTC';

CREATE OR REPLACE TABLE repo_adoption AS
WITH canonical AS (
  SELECT repo_full_name,
         count(*)                                    AS canonical_files,
         count(first_commit_at)                      AS canonical_files_with_history,
         CAST(min(first_commit_at) AS TIMESTAMPTZ)   AS adopted_at
  FROM artifacts
  WHERE location_class = 'canonical'
  GROUP BY 1
  HAVING count(first_commit_at) > 0
), totals AS (
  SELECT repo_full_name, count(*) AS total_files
  FROM artifacts
  GROUP BY 1
)
SELECT c.*, t.total_files, r.language, r.stars, r.forks, r.license,
       CAST(r.created_at AS TIMESTAMPTZ)                         AS repo_created_at,
       c.canonical_files = c.canonical_files_with_history        AS full_history,
       t.total_files > 100                                       AS is_large_repo,
       CASE
         WHEN c.adopted_at <  CAST(r.created_at AS TIMESTAMPTZ) - INTERVAL 1 DAY THEN 'ambiguous'
         WHEN c.adopted_at <= CAST(r.created_at AS TIMESTAMPTZ) + INTERVAL 7 DAY THEN 'new_repo'
         ELSE 'existing_repo'
       END AS adopter_type,
       CASE
         WHEN c.adopted_at < '2026-02-01' THEN 'early'
         WHEN c.adopted_at < '2026-04-01' THEN 'middle'
         ELSE 'late'
       END AS period
FROM canonical c
JOIN totals t USING (repo_full_name)
JOIN repos  r ON r.full_name = c.repo_full_name
WHERE r.created_at IS NOT NULL
  AND c.adopted_at >= '2025-10-01'
  AND c.adopted_at <  '2026-07-01';
