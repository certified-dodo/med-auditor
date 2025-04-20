from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


from backend.frontend_discrepancy_checker import check_chart_entry
from backend.data import chart_data


@app.get("/process")
async def process_data():
    corrected_records = []
    for single_record in chart_data[0:1]:
        corrected_record = check_chart_entry(single_record)
        corrected_records.append(corrected_record)
    print(corrected_records)
    return {"message": corrected_records}
