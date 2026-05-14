# IA520 MP7 — Front-End + Postgres Handshake

## AI use (course policy)

**Allowed:** explain concepts, approaches, starter snippets, SQL suggestions, README help.

**Required:** frequent commits, this `AI_Usage.md` file, and verification (SQL output, screenshots, or runs).

**Not allowed:** submitting work you do not understand, fabricating evidence, or copying another student's repository.

## Grading: pytest vs rubric

- **pytest** in GitHub Actions is a **pass/fail gate** (does it run, are basic contracts met). It is **not** mapped to rubric point rows.
- Your **instructor assigns the 10 points** using the rubric below.

**Org Actions:** If GitHub Actions are disabled on student repositories in this organization, run the same checks locally: `docker compose up -d` then `pytest -q` (see README). The rubric still applies.


## Goal

Expose read + create flows over Postgres with safe, parameterized SQL.

## Deliverables

- Flask app implementing the HTTP contract (extend UI as required by your instructor).
- `AI_Usage.md` and screenshots in Canvas if requested.

## Verify locally

```bash
docker compose up -d
pip install -r requirements-dev.txt
export PGHOST=localhost PGPORT=5432 PGDATABASE=ia510 PGUSER=ia510_user PGPASSWORD=ia510_pass
pytest -q
docker compose down -v
```

## Rubric (10 points)

| Criteria | Excellent | Good | Satisfactory | Needs Improvement | Pts |
| --- | --- | --- | --- | --- | --- |
| Read + Create | List + insert reliably | Mostly works | Only read or only create | Not working | 6 |
| Secure DB access | Parameterized; no secrets in repo | Mostly secure | Some risky patterns | Unsafe / secrets committed | 2 |
| Setup + evidence + AI log | Clear setup, screenshots, strong log | Adequate | Minimal | Missing | 2 |

## HTTP contract (autograde + consistency)

| Method | Path | Expected |
| --- | --- | --- |
| GET | `/health` | 200 OK |
| GET | `/customers` | 200; page includes seeded customer marker (`Avery` or `avery.lopez@example.com`) |
| POST | `/orders` | JSON `{"customer_id": 1, "status": "NEW"}` → 200 or 201; row appears in `orders` |

