from chunker import chunk_text
from data import med_records_jason
import db as chroma


def process_data():
    chunks = chunk_text(med_records_jason)
    chroma.insert_documents(
        [
            {"id": str(i), "text": chunk, "metadata": {"source": "jason"}}
            for i, chunk in enumerate(chunks)
        ]
    )


process_data()
