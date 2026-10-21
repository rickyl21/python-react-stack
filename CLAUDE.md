# Project conventions

Full-stack app: React + Vite frontend in `web/`, FastAPI + SQLite backend in `server/`.

## Layout
- `server/main.py`: FastAPI routes, all under `/api`
- `server/db.py`: SQLite connection and schema (`CREATE TABLE IF NOT EXISTS`)
- `web/src/api.ts`: the only place that calls `fetch`; use the `api<T>()` helper
- `web/src/App.tsx`: UI
- `PLAN.md`: scope, data model, and API contract. Treat it as the source of truth.

## Rules
- Python 3.11+, type hints on every function. TypeScript strict on the frontend.
- Do not add dependencies without asking first.
- Keep it simple: no ORMs, repository layers, or state libraries unless asked.
- Use plain `def` routes, not `async def`. SQLite calls are blocking.
- Request bodies are Pydantic models. Errors must be `{"error": "..."}`
  (raise `HTTPException`); `web/src/api.ts` reads the `error` field, not `detail`.
- Use parameterized SQL (`db.execute("... WHERE id = ?", (id,))`), never f-strings.
- Call `db.commit()` after every write.
- Keep the `/api/{path:path}` 404 catch-all last among `/api` routes. Any `/{slug}` route goes after it.
- Every UI fetch handles loading and error states.
- Field names must match the API contract in `PLAN.md` exactly on both sides (JSON is snake_case).
- Make small, focused changes. Do one task per request; don't refactor unrelated code.
