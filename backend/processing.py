from chunker import chunk_text
from data import med_records_jason
import db as chroma


def insert_medical_records():
    """This inserts mock medical records data into chroma db as embedding"""
    chunks = chunk_text(med_records_jason)
    print(chunks)
    chroma.insert_documents(
        [
            {"id": str(i), "text": chunk, "metadata": {"source": "jason"}}
            for i, chunk in enumerate(chunks)
        ]
    )
