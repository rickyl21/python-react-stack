import time

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items: list[dict] = []

class ItemIn(BaseModel):
    name: str

@app.get("/api/items")
def list_items():
    return items

@app.post("/api/items", status_code=201)
def create_item(body: ItemIn):
    item = {"id": len(items) + 1, "name": body.name, "created_at": int(time.time() * 1000)}
    items.insert(0, item)
    return item
