import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")