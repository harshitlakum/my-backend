# Task API — FastAPI + SQLite (Local & Free)

A minimal, production-shaped backend you can run **locally** with **zero paid services**.  
It ships a FastAPI app, SQLite via SQLModel, pagination + validation, and a small test suite.

---

## Stack
- **FastAPI** (OpenAPI/Swagger at `/docs`)
- **SQLModel** + **SQLite** (`app.db` in project root)
- **Pytest** + **httpx (ASGITransport)** for fast, isolated tests

---

## Features
- Healthcheck: `GET /health`
- Tasks CRUD: `POST/GET/PATCH/DELETE /tasks/`
- Input validation (title length **1–120**)
- Pagination: `GET /tasks/?offset=&limit=` (defaults: `offset=0`, `limit=50`, max `limit=200`)
- UTC timestamps with timezone awareness
- Lifespan startup that auto-creates tables (no Alembic needed)
- Tests use a shared in-memory SQLite (**StaticPool**) for speed & isolation

> **Note:** Routes are defined with a trailing slash (e.g., `/tasks/`).  
> Without it, FastAPI returns a `307` redirect—either use the slash or `curl -L`.

---

## Project Structure
```

my-backend/
├─ app/
│  ├─ main.py            # FastAPI app (lifespan creates tables)
│  ├─ db.py              # SQLite engine + session + init_db()
│  ├─ models/
│  │  └─ task.py         # SQLModel Task (UTC timestamps)
│  ├─ routers/
│  │  └─ tasks.py        # CRUD + pagination
│  └─ schemas/
│     └─ task.py         # Pydantic DTOs with validation
├─ tests/
│  ├─ conftest.py        # add project root to sys.path for tests
│  ├─ test_health.py     # health endpoint
│  └─ test_tasks.py      # CRUD E2E with StaticPool in-memory DB
├─ requirements.txt
├─ .gitignore
└─ README.md

````

---

## Quick Start (Local)
```bash
# create/activate your virtualenv (example)
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# run API
uvicorn app.main:app --reload --port 8000
````

Open:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Health → [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) → `{"status":"ok"}`

---

## Endpoints

### Health

* `GET /health` → `{"status":"ok"}`

### Tasks

* `POST /tasks/` → create a task
  Body: `{ "title": "Read paper" }`
* `GET /tasks/?offset=0&limit=50` → list tasks (paginated)
* `PATCH /tasks/{id}` → update fields, e.g. `{ "done": true }`
* `DELETE /tasks/{id}` → delete a task

**Validation**

* `title`: string, **1–120** chars → otherwise `422`

**Pagination**

* `offset ≥ 0`
* `1 ≤ limit ≤ 200`

---

## cURL Examples

```bash
# Create
curl -s -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"T1"}'

# List (first page)
curl -s "http://127.0.0.1:8000/tasks/?offset=0&limit=10"

# Update
curl -s -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete
curl -s -X DELETE http://127.0.0.1:8000/tasks/1
```

---

## Running Tests (Local & Free)

```bash
pytest
```

* Uses **httpx.ASGITransport** (no network needed).
* Shared in-memory SQLite (**StaticPool**) with `SQLModel.metadata.create_all()` / `drop_all()` per test session.

---

## Implementation Notes

* Timezone-aware UTC timestamps: `datetime.now(timezone.utc)`
* FastAPI **lifespan** handles DB table creation on startup
* Trailing slash on routers to avoid `307` redirects
* Ready to extend to Postgres + Docker + CI later (all free)

---

## Next Steps (Optional, Still Free)

* Add Docker Compose with Postgres for a production-like stack
* GitHub Actions to run tests on every push
* JWT auth, rate limiting, logging/metrics

---

## License

MIT 


