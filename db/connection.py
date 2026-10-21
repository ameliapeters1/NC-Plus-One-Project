import psycopg2
import os 
from dotenv import load_dotenv

def get_connection():
    ENV = os.getenv("ENV","development")
    load_dotenv(f".env.{ENV}")

    required_credentials = ["PGDATABASE", "PGUSER", "PGPASSWORD",
                   "PGHOST","PGPORT"]
    missing_credentials = [credential for credential in required_credentials if not os.getenv(credential)]
    
    if missing_credentials:
        raise RuntimeError(f"Credentials not set: {missing_credentials}")

    connection = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"))

    return connection

