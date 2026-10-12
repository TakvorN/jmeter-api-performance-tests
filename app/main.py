import asyncio

from fastapi import FastAPI, HTTPException

app = FastAPI()

ITEMS = {
    1: {"id": 1, "name": "Keyboard"},
    2: {"id": 2, "name": "Mouse"},
    3: {"id": 3, "name": "Monitor"},
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = ITEMS.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

@app.get("/slow")
async def slow(delay_ms: int = 100):
    await asyncio.sleep(delay_ms / 1000)

    return {
        "status": "ok",
        "delay_ms": delay_ms,
    }