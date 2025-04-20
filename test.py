import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


try:
    response = (
        supabase.table("characters")
        .insert(
            [
                {"id": 1, "name": "Frodo"},
                {"id": 2, "name": "Sam"},
            ]
        )
        .execute()
    )
    print(response)
except Exception as exception:
    print(exception)
