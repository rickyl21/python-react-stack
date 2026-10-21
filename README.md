# Interview template

React + Vite frontend, FastAPI + SQLite backend, one command to run both.

## Run it

```bash
npm run setup      # installs root + web deps, creates server/.venv, installs Python deps
npm run dev        # API on :3001, web on :5173
```

Open http://localhost:5173. You should see "API ok" and be able to add and delete items.

## How it fits together

- `web/` is the React app, served by Vite on port 5173.
- `server/` is the FastAPI API on port 3001 (`main.py` routes, `db.py` schema). Data is stored in `server/dev.db`. Interactive API docs: http://localhost:3001/docs
- `web/vite.config.ts` proxies `/api/*` to port 3001, so the frontend calls `fetch('/api/...')` with no CORS setup.

## Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Starts both servers with hot reload |
| `npm run typecheck` | Typechecks and builds the web app |
| `npm run reset-db` | Deletes the SQLite file; the schema is recreated on next start |

## Quick API test

```bash
curl localhost:5173/api/health
curl -X POST localhost:5173/api/items -H 'Content-Type: application/json' -d '{"name":"hello"}'
curl localhost:5173/api/items
```

## Interview workflow

1. Fill in `PLAN.md` first: questions, scope, data model, API contract.
2. Replace the `items` example in `server/db.py` and `server/main.py` with the real schema and routes.
3. Build one thin end-to-end slice, commit, then widen.
4. `CLAUDE.md` holds conventions for AI tools. Point them at `PLAN.md`.
