from fastapi import FastAPI
from data import med_records_jason
from chunker import chunk_text
from db import insert_documents

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/process")
async def read_item(item_id: int, q: str = None):
    # insert_documents(chunks, [str(i) for i in range(len(chunks))])
    return {"item_id": item_id, "q": q}
