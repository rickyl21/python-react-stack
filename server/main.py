import logging
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from db import db

app = FastAPI()
log = logging.getLogger("uvicorn.error")


# Every error leaves the API as {"error": "..."} so web/src/api.ts can show it.
@app.exception_handler(StarletteHTTPException)
async def http_error(_req: Request, exc: StarletteHTTPException):
    return JSONResponse({"error": str(exc.detail)}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_error(_req: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    field = ".".join(str(p) for p in first["loc"] if p != "body")
    return JSONResponse({"error": f"{field}: {first['msg']}"}, status_code=400)


@app.exception_handler(Exception)
async def unhandled_error(_req: Request, exc: Exception):
    log.exception("unhandled error", exc_info=exc)
    return JSONResponse({"error": "internal error"}, status_code=500)


@app.get("/api/health")
def health():
    return {"ok": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


# Example resource: delete or rename once you know the real problem.
class ItemIn(BaseModel):
    name: str


@app.get("/api/items")
def list_items():
    return [dict(r) for r in db.execute("SELECT * FROM items ORDER BY id DESC")]


@app.post("/api/items", status_code=201)
def create_item(body: ItemIn):
    name = body.name.strip()
    if not name:
        raise HTTPException(400, "name is required")
    cur = db.execute(
        "INSERT INTO items (name, created_at) VALUES (?, ?)",
        (name, int(time.time() * 1000)),
    )
    db.commit()
    row = db.execute("SELECT * FROM items WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    cur = db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, "not found")


# Unknown /api routes return JSON, not a default page.
# Keep this LAST among /api routes. Put any /{slug} route after it.
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def api_not_found(path: str):
    raise HTTPException(404, "not found")
