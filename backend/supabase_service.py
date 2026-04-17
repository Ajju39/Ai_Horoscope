import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_horoscope(record: dict):
    response = supabase.table("horoscope_history").insert(record).execute()
    return response.data


def get_history_by_user_id(user_id: str, limit: int = 10):
    response = (
        supabase.table("horoscope_history")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data