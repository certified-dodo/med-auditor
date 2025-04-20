from chunker import chunk_text
from data import chart_data, med_records_jason
from db import insert_documents
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/process")
async def process_data():
    for single_record in chart_data:
        print(single_record)
    return {"message": "Data processed"}
